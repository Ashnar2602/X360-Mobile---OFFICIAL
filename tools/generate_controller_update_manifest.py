#!/usr/bin/env python3
"""Generate the independent X360 Companion update feed."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re
from datetime import datetime, timezone

VERSION = re.compile(r"^\d+\.\d+\.\d+(?:[-.][0-9A-Za-z.-]+)?$")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apk", required=True, type=pathlib.Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-code", required=True, type=int)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--download-url", required=True)
    parser.add_argument("--page-url", required=True)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    if not VERSION.fullmatch(args.version) or args.version_code <= 0:
        raise SystemExit("Invalid Companion version or versionCode")
    if not args.apk.is_file() or not args.download_url.startswith("https://"):
        raise SystemExit("Companion APK and HTTPS download URL are required")
    digest = hashlib.sha256(args.apk.read_bytes()).hexdigest()
    if args.output.is_file():
        latest = json.loads(args.output.read_text(encoding="utf-8")).get("latest", {})
        if latest.get("version") == args.version:
            if latest.get("apk", {}).get("sha256") != digest:
                raise SystemExit("A published Companion version is immutable")
            return
        if int(latest.get("versionCode", 0)) >= args.version_code:
            raise SystemExit("Companion versionCode must increase")
    output = {"schema": 1, "product": "x360-companion", "packageName": "emu.x360mobile.controller", "latest": {"version": args.version, "versionCode": args.version_code, "channel": "public", "prerelease": False, "releaseTag": args.release_tag, "pageUrl": args.page_url, "publishedAt": datetime.now(timezone.utc).isoformat(), "apk": {"url": args.download_url, "size": args.apk.stat().st_size, "sha256": digest}}}
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)

if __name__ == "__main__":
    main()
