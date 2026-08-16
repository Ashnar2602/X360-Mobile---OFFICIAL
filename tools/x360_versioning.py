#!/usr/bin/env python3
"""Canonical X360 Mobile release-version parser and validator."""

from __future__ import annotations

import argparse
import dataclasses
import json
import re


CHANNEL_RANK = {"alpha": 0, "preview": 1, "rc": 2, "public": 3}
CHANNEL_STAGE = {"alpha": 0, "preview": 1, "rc": 2, "public": 9}
MAINTENANCE_KINDS = {"revision", "hotfix", "repack"}
ANDROID_VERSION_CODE_MAX = 2_100_000_000
BASE_RE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>.*)$")
COMPACT_RE = re.compile(r"^(alpha|preview|rc|public)(\d+)?$", re.IGNORECASE)
NUMERIC_RE = re.compile(r"^(?:0|[1-9]\d*)$")
BUILD_METADATA_RE = re.compile(r"^[0-9A-Za-z.-]+$")
LEGACY_RE = re.compile(
    r"^v?\d+\.\d+\.\d+"
    r"(?:[-.]?(?:preview|rc|public)(?:[.-]?\d+)?)?"
    r"(?:\+[0-9A-Za-z.-]+)?$",
    re.IGNORECASE,
)


@dataclasses.dataclass(frozen=True)
class ParsedVersion:
    major: int
    minor: int
    patch: int
    channel: str
    channel_sequence: int = 0
    maintenance_kind: str = "none"
    maintenance_sequence: int = 0

    @property
    def prerelease(self) -> bool:
        return self.channel != "public"

    @property
    def order_key(self) -> tuple[int, int, int, int, int, int]:
        return (
            self.major,
            self.minor,
            self.patch,
            CHANNEL_RANK[self.channel],
            self.channel_sequence,
            self.maintenance_sequence,
        )

    @property
    def canonical(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        if self.channel == "public" and self.maintenance_kind == "none":
            return base
        channel = (
            "public"
            if self.channel == "public"
            else f"{self.channel}.{self.channel_sequence}"
        )
        maintenance = (
            ""
            if self.maintenance_kind == "none"
            else f".{self.maintenance_kind}.{self.maintenance_sequence}"
        )
        return f"{base}-{channel}{maintenance}"


def _numeric(value: str, label: str) -> int:
    if not NUMERIC_RE.fullmatch(value):
        raise ValueError(f"Invalid {label}: {value}")
    return int(value)


def parse_version(value: str) -> ParsedVersion:
    raw = value.strip()
    if raw.lower().startswith("v"):
        raw = raw[1:]
    if "+" in raw:
        raw, metadata = raw.split("+", 1)
        if not BUILD_METADATA_RE.fullmatch(metadata):
            raise ValueError(f"Invalid build metadata: {metadata}")
    match = BASE_RE.fullmatch(raw)
    if not match:
        raise ValueError(f"Unsupported X360 Mobile version: {value}")
    major = _numeric(match.group("major"), "major version")
    minor = _numeric(match.group("minor"), "minor version")
    patch = _numeric(match.group("patch"), "patch version")
    if minor > 99 or patch > 99:
        raise ValueError("Minor and patch components must be between 0 and 99")

    suffix = match.group("suffix")
    if not suffix:
        return ParsedVersion(major, minor, patch, "public")
    if suffix[0] in "-.":
        qualifier = suffix[1:]
    elif COMPACT_RE.fullmatch(suffix):
        qualifier = suffix
    else:
        raise ValueError(f"Invalid version suffix: {suffix}")

    compact = COMPACT_RE.fullmatch(qualifier)
    if compact:
        tokens = [compact.group(1)]
        if compact.group(2):
            tokens.append(compact.group(2))
    else:
        tokens = re.split(r"[.-]", qualifier)
    if not tokens or any(not token for token in tokens):
        raise ValueError(f"Invalid version suffix: {suffix}")

    channel = tokens[0].lower()
    if channel not in CHANNEL_RANK:
        raise ValueError(f"Unsupported release channel: {channel}")
    index = 1
    channel_sequence = 0
    maintenance_kind = "none"
    maintenance_sequence = 0
    if channel != "public":
        if index < len(tokens) and NUMERIC_RE.fullmatch(tokens[index]):
            channel_sequence = _numeric(tokens[index], "channel sequence")
            index += 1
    elif index < len(tokens) and NUMERIC_RE.fullmatch(tokens[index]):
        maintenance_kind = "revision"
        maintenance_sequence = _numeric(tokens[index], "maintenance sequence")
        index += 1

    if index < len(tokens):
        if maintenance_kind != "none":
            raise ValueError("Legacy public.N cannot have another maintenance suffix")
        maintenance_kind = tokens[index].lower()
        index += 1
        if maintenance_kind not in MAINTENANCE_KINDS:
            raise ValueError(f"Unsupported maintenance kind: {maintenance_kind}")
        if index >= len(tokens):
            raise ValueError("Maintenance sequence is required")
        maintenance_sequence = _numeric(tokens[index], "maintenance sequence")
        index += 1
        if maintenance_sequence <= 0:
            raise ValueError("Maintenance sequence must be positive")
    if index != len(tokens):
        raise ValueError(f"Unexpected version identifier: {tokens[index]}")
    return ParsedVersion(
        major,
        minor,
        patch,
        channel,
        channel_sequence,
        maintenance_kind,
        maintenance_sequence,
    )


def is_legacy_compatible(value: str) -> bool:
    return bool(LEGACY_RE.fullmatch(value.strip()))


def validate_version_code(version: ParsedVersion, version_code: int) -> int:
    if version_code <= 0 or version_code > ANDROID_VERSION_CODE_MAX:
        raise ValueError("versionCode is outside Android's supported range")
    base = (
        version.major * 100_000_000
        + version.minor * 1_000_000
        + version.patch * 10_000
        + CHANNEL_STAGE[version.channel] * 1_000
    )
    publication_sequence = version_code - base
    if publication_sequence not in range(0, 1000):
        raise ValueError(
            f"versionCode {version_code} does not match {version.canonical}"
        )
    if version.channel == "public" and version.maintenance_kind == "none":
        if publication_sequence != 0:
            raise ValueError("The initial Public release must use publication sequence 0")
    elif version.channel == "public":
        if publication_sequence != version.maintenance_sequence:
            raise ValueError(
                "Public maintenance sequence must match the versionCode sequence"
            )
    elif version.channel_sequence <= 0:
        raise ValueError("Alpha, Preview, and RC releases require a positive sequence")
    elif version.maintenance_kind == "none":
        if publication_sequence != version.channel_sequence:
            raise ValueError("Channel sequence must match the versionCode sequence")
    elif publication_sequence <= version.channel_sequence:
        raise ValueError(
            "A prerelease maintenance build needs a later publication sequence"
        )
    return publication_sequence


def describe(value: str, version_code: int | None = None) -> dict[str, object]:
    parsed = parse_version(value)
    result: dict[str, object] = {
        "canonical": parsed.canonical,
        "channel": parsed.channel,
        "channelSequence": parsed.channel_sequence,
        "maintenanceKind": parsed.maintenance_kind,
        "maintenanceSequence": parsed.maintenance_sequence,
        "prerelease": parsed.prerelease,
        "legacyCompatible": is_legacy_compatible(value),
    }
    if version_code is not None:
        result["publicationSequence"] = validate_version_code(parsed, version_code)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("describe", "normalize"))
    parser.add_argument("version")
    parser.add_argument("version_code", nargs="?", type=int)
    args = parser.parse_args()
    if args.command == "normalize":
        print(parse_version(args.version).canonical)
    else:
        print(json.dumps(describe(args.version, args.version_code), sort_keys=True))


if __name__ == "__main__":
    main()
