from __future__ import annotations
import json, pathlib, subprocess, sys, tempfile, unittest
GENERATOR = pathlib.Path(__file__).resolve().parents[1] / "generate_controller_update_manifest.py"
class CompanionManifestTest(unittest.TestCase):
    def test_writes_and_protects_a_public_companion_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary); apk = directory / "x360-companion-0.1.0.apk"; apk.write_bytes(b"controller"); output = directory / "controller-update-manifest.json"
            command = [sys.executable, str(GENERATOR), "--apk", str(apk), "--version", "0.1.0", "--version-code", "11002", "--release-tag", "v0.6.3", "--download-url", "https://example.test/controller.apk", "--page-url", "https://example.test/release", "--output", str(output)]
            subprocess.run(command, check=True)
            manifest = json.loads(output.read_text(encoding="utf-8")); self.assertEqual("emu.x360mobile.controller", manifest["packageName"]); self.assertEqual("v0.6.3", manifest["latest"]["releaseTag"])
            apk.write_bytes(b"different"); result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode); self.assertIn("immutable", result.stderr)
if __name__ == "__main__": unittest.main()
