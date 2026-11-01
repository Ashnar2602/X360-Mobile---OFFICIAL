"""Offline migration tests: synthetic APK bytes, no network or publication."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from x360_versioning import describe, parse_version, validate_version_code


class EdgeVersionCodeTest(unittest.TestCase):
    def test_new_public_commit_build(self):
        value = describe("0.6.4+f706ba7c5", 60411100)
        self.assertEqual("0.6.4", value["canonical"])
        self.assertEqual("public", value["channel"])
        self.assertFalse(value["prerelease"])
        self.assertTrue(value["legacyCompatible"])
        self.assertEqual(11100, value["publicationSequence"])

    def test_numbered_alpha_preview_rc_commit_builds(self):
        for channel in ("alpha", "preview", "rc"):
            with self.subTest(channel=channel):
                value = describe(f"0.6.4-{channel}.1+f706ba7c5", 60411100)
                self.assertEqual(channel, value["channel"])
                self.assertEqual(1, value["channelSequence"])
                self.assertEqual(11100, value["publicationSequence"])
                self.assertTrue(value["prerelease"])

    def test_legacy_codes_and_maintenance_mismatch_are_unchanged(self):
        self.assertEqual(0, validate_version_code(parse_version("0.6.3"), 6039000))
        self.assertEqual(0, validate_version_code(parse_version("0.6.4+f706ba7c5"), 6049000))
        with self.assertRaises(ValueError):
            validate_version_code(parse_version("0.6.2-public.hotfix.2"), 6029001)

    def test_new_count_boundaries(self):
        for count in (1, 99999):
            self.assertEqual(count, validate_version_code(parse_version("0.6.4"), 60400000 + count))

    def test_wrong_base_zero_overflow_and_android_limit_are_rejected(self):
        for version, code in (("0.6.5", 60411100), ("0.6.4", 60400000),
                              ("0.6.4", 60500000), ("0.6.4", 0),
                              ("0.6.4", -1), ("0.6.4", 2100000001)):
            with self.subTest(version=version, code=code), self.assertRaises(ValueError):
                validate_version_code(parse_version(version), code)

    def test_unsequenced_prereleases_and_beta_are_not_promoted(self):
        for version in ("0.6.4-alpha", "0.6.4-rc.0", "0.6.4-preview"):
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, "positive sequence"):
                validate_version_code(parse_version(version), 60411100)
        with self.assertRaises(ValueError):
            parse_version("0.6.4-beta.1+f706ba7c5")

    def test_cli_uses_the_same_validator(self):
        result = subprocess.run([sys.executable, "-B", str(TOOLS / "x360_versioning.py"),
                                 "describe", "0.6.4-rc.1+f706ba7c5", "60411100"],
                                capture_output=True, text=True, check=True)
        self.assertEqual(11100, json.loads(result.stdout)["publicationSequence"])

    def generate(self, directory, version, code, payload=b"synthetic", policy=""):
        apk = directory / f"x360-mobile-{version}.apk"
        apk.write_bytes(payload)
        notes = directory / "notes.md"
        notes.write_text("Synthetic release\n" + policy, encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(TOOLS / "generate_update_manifest.py"),
                               "--apk", str(apk), "--version", version, "--version-code", str(code),
                               "--download-url", f"https://example.test/{apk.name}",
                               "--page-url", f"https://example.test/releases/v{version}",
                               "--notes-file", str(notes), "--output", str(directory / "update-manifest.json")],
                              capture_output=True, text=True)

    def test_legacy_public_to_new_core_feed_migration(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertEqual(0, self.generate(directory, "0.6.3", 6039000).returncode)
            result = self.generate(directory, "0.6.4+f706ba7c5", 60411100)
            self.assertEqual(0, result.returncode, result.stderr)
            feed = json.loads((directory / "update-manifest.json").read_text())
            self.assertEqual(60411100, feed["highestVersionCode"])
            self.assertEqual("public", feed["releases"][0]["channel"])
            self.assertEqual(11100, feed["releases"][0]["publicationSequence"])

    def test_prerelease_retains_the_public_bridge(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertEqual(0, self.generate(directory, "0.6.3", 6039000).returncode)
            result = self.generate(directory, "0.6.4-rc.1+f706ba7c5", 60411100)
            self.assertEqual(0, result.returncode, result.stderr)
            versions = [v["version"] for v in json.loads((directory / "update-manifest.json").read_text())["releases"]]
            self.assertEqual(["0.6.4-rc.1+f706ba7c5", "0.6.3"], versions)

    def test_lower_or_equal_new_code_cannot_mutate_the_feed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertEqual(0, self.generate(directory, "0.6.4+f706ba7c5", 60411100).returncode)
            output = directory / "update-manifest.json"
            original = output.read_bytes()
            for code in (60411099, 60411100):
                result = self.generate(directory, "0.6.4-public.hotfix.1+f706ba7c5", code)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("not greater", result.stderr)
                self.assertEqual(original, output.read_bytes())

    def test_identical_retry_is_noop_and_changed_apk_is_immutable(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            version = "0.6.4+f706ba7c5"
            self.assertEqual(0, self.generate(directory, version, 60411100).returncode)
            output = directory / "update-manifest.json"
            original = output.read_bytes()
            self.assertEqual(0, self.generate(directory, version, 60411100).returncode)
            self.assertEqual(original, output.read_bytes())
            result = self.generate(directory, version, 60411100, b"changed")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("immutable", result.stderr)
            self.assertEqual(original, output.read_bytes())

    def test_invalid_source_policy_or_self_block_never_creates_a_feed(self):
        for policy in ('<!-- x360-update: {"blockedVersionCodes":[60411100]} -->',
                       '<!-- x360-update: {"minSourceVersionCode":60411100,"maxSourceVersionCode":6039000} -->'):
            with self.subTest(policy=policy), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                result = self.generate(directory, "0.6.4+f706ba7c5", 60411100, policy=policy)
                self.assertNotEqual(0, result.returncode)
                self.assertFalse((directory / "update-manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
