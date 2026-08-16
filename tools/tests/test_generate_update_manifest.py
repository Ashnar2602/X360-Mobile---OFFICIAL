from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


TOOLS = pathlib.Path(__file__).resolve().parents[1]
GENERATOR = TOOLS / "generate_update_manifest.py"


class GenerateUpdateManifestTest(unittest.TestCase):
    def run_generator(
        self,
        directory: pathlib.Path,
        version: str,
        version_code: int,
        apk_bytes: bytes,
        notes: str = "Release notes",
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        apk = directory / f"x360-mobile-{version}.apk"
        apk.write_bytes(apk_bytes)
        notes_file = directory / "notes.md"
        notes_file.write_text(notes, encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--apk",
                str(apk),
                "--version",
                version,
                "--version-code",
                str(version_code),
                "--download-url",
                f"https://example.test/{apk.name}",
                "--page-url",
                f"https://example.test/releases/{version}",
                "--notes-file",
                str(notes_file),
                "--output",
                str(directory / "update-manifest.json"),
            ],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_preserves_legacy_bridge_and_emits_policy(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = pathlib.Path(raw_directory)
            self.run_generator(directory, "0.6.2", 6029000, b"public")
            policy = """
Release notes

<!-- x360-update: {"mandatory":true,"security":true,"blockedVersionCodes":[6019001],"supersedes":"0.6.2","rolloutPercentage":25,"minSourceVersionCode":6019000,"maxSourceVersionCode":6029000} -->
""".strip()
            self.run_generator(
                directory,
                "0.6.2-public.hotfix.1",
                6029001,
                b"hotfix",
                policy,
            )
            manifest = json.loads((directory / "update-manifest.json").read_text())
            self.assertEqual(2, manifest["schema"])
            self.assertEqual(6029001, manifest["highestVersionCode"])
            self.assertEqual(
                ["0.6.2-public.hotfix.1", "0.6.2"],
                [item["version"] for item in manifest["releases"]],
            )
            latest = manifest["releases"][0]
            self.assertEqual("hotfix", latest["maintenanceKind"])
            self.assertEqual(1, latest["maintenanceSequence"])
            self.assertTrue(latest["mandatory"])
            self.assertTrue(latest["security"])
            self.assertEqual([6019001], latest["blockedVersionCodes"])
            self.assertNotIn("x360-update", latest["notes"])

    def test_replaces_latest_complex_release_but_keeps_bridge(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = pathlib.Path(raw_directory)
            self.run_generator(directory, "0.6.2", 6029000, b"public")
            self.run_generator(
                directory, "0.6.2-public.hotfix.1", 6029001, b"hotfix"
            )
            self.run_generator(
                directory, "0.6.2-public.revision.2", 6029002, b"revision"
            )
            manifest = json.loads((directory / "update-manifest.json").read_text())
            self.assertEqual(
                ["0.6.2-public.revision.2", "0.6.2"],
                [item["version"] for item in manifest["releases"]],
            )

    def test_refuses_replacing_an_existing_version_with_another_apk(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = pathlib.Path(raw_directory)
            self.run_generator(directory, "0.6.2", 6029000, b"first")
            result = self.run_generator(
                directory, "0.6.2", 6029000, b"different", check=False
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("immutable", result.stderr)

    def test_rejects_unknown_policy_and_self_blocking_release(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = pathlib.Path(raw_directory)
            unknown = self.run_generator(
                directory,
                "0.6.2",
                6029000,
                b"public",
                '<!-- x360-update: {"unexpected":true} -->',
                check=False,
            )
            self.assertNotEqual(0, unknown.returncode)
            self.assertIn("Unknown", unknown.stderr)

            blocked = self.run_generator(
                directory,
                "0.6.2",
                6029000,
                b"public",
                '<!-- x360-update: {"blockedVersionCodes":[6029000]} -->',
                check=False,
            )
            self.assertNotEqual(0, blocked.returncode)
            self.assertIn("block its own", blocked.stderr)


if __name__ == "__main__":
    unittest.main()
