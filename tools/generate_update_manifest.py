#!/usr/bin/env python3
"""Generate the minimal public X360 Mobile update manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone


VERSION_RE = re.compile(
    r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:-?(?P<channel>preview|rc|public)(?:[.-]?(?P<sequence>\d+))?)?$",
    re.IGNORECASE,
)
CHANNEL_RANK = {"preview": 0, "rc": 1, "public": 2}


def version_key(version: str) -> tuple[int, int, int, int, int]:
    match = VERSION_RE.fullmatch(version)
    if not match:
        raise ValueError(f"Unsupported version in manifest: {version}")
    channel = (match.group("channel") or "public").lower()
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
        CHANNEL_RANK[channel],
        int(match.group("sequence") or 0),
    )


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


def main() -> None:
    args = parse_args()
    match = VERSION_RE.fullmatch(args.version)
    if not match:
        raise SystemExit(f"Unsupported X360 Mobile version: {args.version}")
    channel = (match.group("channel") or "public").lower()
    prerelease = channel != "public"
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
    release = {
        "version": args.version.removeprefix("v"),
        "versionCode": args.version_code,
        "channel": channel,
        "prerelease": prerelease,
        "pageUrl": args.page_url,
        "notes": notes.strip(),
        "publishedAt": datetime.now(timezone.utc).isoformat(),
        "apk": {
            "url": args.download_url,
            "size": args.apk.stat().st_size,
            "sha256": digest.hexdigest(),
        },
    }

    manifest = {"schema": 1, "releases": []}
    if args.output.is_file():
        manifest = json.loads(args.output.read_text(encoding="utf-8"))
        if manifest.get("schema") != 1 or not isinstance(manifest.get("releases"), list):
            raise SystemExit("Existing manifest has an unsupported schema")
    existing_versions = [
        item for item in manifest["releases"]
        if item.get("version") != release["version"]
    ]
    if existing_versions:
        latest = max(existing_versions, key=lambda item: version_key(item["version"]))
        if version_key(release["version"]) <= version_key(latest["version"]):
            raise SystemExit(
                f"Version {release['version']} is not newer than {latest['version']}"
            )
        highest_version_code = max(int(item.get("versionCode", 0)) for item in existing_versions)
        if args.version_code <= highest_version_code:
            raise SystemExit(
                f"versionCode {args.version_code} is not greater than {highest_version_code}"
            )
    candidates = [
        item for item in manifest["releases"]
        if item.get("version") != release["version"]
    ]
    candidates.append(release)
    public = [item for item in candidates if not item.get("prerelease", False)]
    prereleases = [item for item in candidates if item.get("prerelease", False)]
    manifest["releases"] = [
        item for item in (
            max(public, key=lambda item: version_key(item["version"]), default=None),
            max(prereleases, key=lambda item: version_key(item["version"]), default=None),
        )
        if item is not None
    ]
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(args.output)


if __name__ == "__main__":
    main()
