#!/usr/bin/env python3
"""Generate the public X360 Mobile update manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone

from x360_versioning import (
    is_legacy_compatible,
    parse_version,
    validate_version_code,
)


POLICY_COMMENT_RE = re.compile(
    r"<!--\s*x360-update\s*:\s*(\{.*?\})\s*-->",
    re.IGNORECASE | re.DOTALL,
)
POLICY_FIELDS = {
    "mandatory",
    "security",
    "blockedVersionCodes",
    "supersedes",
    "rolloutPercentage",
    "minSourceVersionCode",
    "maxSourceVersionCode",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apk", required=True, type=pathlib.Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-code", required=True, type=int)
    parser.add_argument("--download-url", required=True)
    parser.add_argument("--page-url", required=True)
    parser.add_argument("--notes-file", type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    return parser.parse_args()


def parse_release_policy(notes: str) -> tuple[str, dict[str, object]]:
    matches = list(POLICY_COMMENT_RE.finditer(notes))
    if len(matches) > 1:
        raise ValueError("Release notes contain multiple x360-update policies")
    raw: dict[str, object] = {}
    if matches:
        loaded = json.loads(matches[0].group(1))
        if not isinstance(loaded, dict):
            raise ValueError("x360-update policy must be a JSON object")
        unknown = set(loaded) - POLICY_FIELDS
        if unknown:
            raise ValueError(f"Unknown x360-update policy fields: {sorted(unknown)}")
        raw = loaded
        notes = POLICY_COMMENT_RE.sub("", notes).strip()

    mandatory = raw.get("mandatory", False)
    security = raw.get("security", False)
    if type(mandatory) is not bool or type(security) is not bool:
        raise ValueError("mandatory and security must be JSON booleans")

    def integer(name: str, default: int) -> int:
        value = raw.get(name, default)
        if type(value) is not int:
            raise ValueError(f"{name} must be an integer")
        return value

    rollout = integer("rolloutPercentage", 100)
    minimum = integer("minSourceVersionCode", 0)
    maximum = integer("maxSourceVersionCode", 0)
    if rollout not in range(0, 101):
        raise ValueError("rolloutPercentage must be between 0 and 100")
    if minimum < 0 or maximum < 0 or (minimum and maximum and minimum > maximum):
        raise ValueError("Invalid source versionCode range")

    blocked = raw.get("blockedVersionCodes", [])
    if not isinstance(blocked, list) or any(type(code) is not int or code <= 0 for code in blocked):
        raise ValueError("blockedVersionCodes must contain positive integers")
    blocked = sorted(set(blocked))
    supersedes = raw.get("supersedes", "")
    if not isinstance(supersedes, str):
        raise ValueError("supersedes must be a version string")
    supersedes = supersedes.strip().removeprefix("v")
    if supersedes:
        parse_version(supersedes)

    return notes, {
        "mandatory": mandatory,
        "security": security,
        "blockedVersionCodes": blocked,
        "supersedes": supersedes,
        "rolloutPercentage": rollout,
        "minSourceVersionCode": minimum,
        "maxSourceVersionCode": maximum,
    }


def release_order(item: dict[str, object]) -> tuple[int, ...]:
    version_code = int(item.get("versionCode", 0))
    if version_code > 0:
        return (1, version_code)
    return (0, *parse_version(str(item["version"])).order_key)


def retain_feed_releases(releases: list[dict[str, object]]) -> list[dict[str, object]]:
    selected: dict[str, dict[str, object]] = {}
    groups = (
        [item for item in releases if not bool(item.get("prerelease", False))],
        [item for item in releases if bool(item.get("prerelease", False))],
        [
            item for item in releases
            if not bool(item.get("prerelease", False))
            and is_legacy_compatible(str(item.get("version", "")))
        ],
        [
            item for item in releases
            if bool(item.get("prerelease", False))
            and is_legacy_compatible(str(item.get("version", "")))
        ],
    )
    for group in groups:
        if group:
            newest = max(group, key=release_order)
            selected[str(newest["version"])] = newest
    return sorted(selected.values(), key=release_order, reverse=True)


def main() -> None:
    args = parse_args()
    version_text = args.version.removeprefix("v")
    parsed = parse_version(version_text)
    publication_sequence = validate_version_code(parsed, args.version_code)
    if args.version_code <= 0:
        raise SystemExit("versionCode must be positive")
    if not args.download_url.startswith("https://"):
        raise SystemExit("APK download URL must use HTTPS")
    if not args.page_url.startswith("https://"):
        raise SystemExit("Release page URL must use HTTPS")
    if not args.apk.is_file():
        raise SystemExit(f"APK not found: {args.apk}")

    digest = hashlib.sha256()
    with args.apk.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    notes = args.notes_file.read_text(encoding="utf-8") if args.notes_file else ""
    try:
        notes, policy = parse_release_policy(notes)
    except (ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"Invalid x360-update policy: {error}") from error

    release: dict[str, object] = {
        "version": version_text,
        "versionCode": args.version_code,
        "channel": parsed.channel,
        "channelSequence": parsed.channel_sequence,
        "maintenanceKind": parsed.maintenance_kind,
        "maintenanceSequence": parsed.maintenance_sequence,
        "publicationSequence": publication_sequence,
        "prerelease": parsed.prerelease,
        **policy,
        "pageUrl": args.page_url,
        "notes": notes,
        "publishedAt": datetime.now(timezone.utc).isoformat(),
        "apk": {
            "url": args.download_url,
            "size": args.apk.stat().st_size,
            "sha256": digest.hexdigest(),
        },
    }

    manifest: dict[str, object] = {"schema": 2, "highestVersionCode": 0, "releases": []}
    if args.output.is_file():
        manifest = json.loads(args.output.read_text(encoding="utf-8"))
        if manifest.get("schema", 1) not in (1, 2) or not isinstance(
            manifest.get("releases"), list
        ):
            raise SystemExit("Existing manifest has an unsupported schema")
    releases = list(manifest["releases"])
    same_version = next(
        (item for item in releases if item.get("version") == version_text),
        None,
    )
    if same_version is not None:
        same_apk = same_version.get("apk", {})
        if (
            int(same_version.get("versionCode", 0)) != args.version_code
            or same_apk.get("url") != args.download_url
            or int(same_apk.get("size", 0)) != args.apk.stat().st_size
            or same_apk.get("sha256") != digest.hexdigest()
        ):
            raise SystemExit(
                f"Version {version_text} is immutable and already references another APK"
            )
        print(f"Version {version_text} is already present with the same APK")
        return

    highest_version_code = max(
        [int(manifest.get("highestVersionCode", 0))]
        + [int(item.get("versionCode", 0)) for item in releases]
    )
    if args.version_code <= highest_version_code:
        raise SystemExit(
            f"versionCode {args.version_code} is not greater than {highest_version_code}"
        )
    if args.version_code in policy["blockedVersionCodes"]:
        raise SystemExit("A release cannot block its own versionCode")

    releases.append(release)
    manifest = {
        "schema": 2,
        "highestVersionCode": args.version_code,
        "releases": retain_feed_releases(releases),
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(args.output)


if __name__ == "__main__":
    main()
