from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest


TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from x360_versioning import (  # noqa: E402
    describe,
    is_legacy_compatible,
    parse_version,
    validate_version_code,
)


class X360VersioningTest(unittest.TestCase):
    def test_normalizes_legacy_and_structured_versions(self) -> None:
        self.assertEqual("0.6.1-rc.2", parse_version("v0.6.1rc2").canonical)
        self.assertEqual(
            "0.6.1-public.revision.1",
            parse_version("0.6.1-public.1").canonical,
        )
        hotfix = parse_version("0.6.2-public.hotfix.3")
        self.assertEqual("public", hotfix.channel)
        self.assertEqual("hotfix", hotfix.maintenance_kind)
        self.assertEqual(3, hotfix.maintenance_sequence)
        self.assertFalse(hotfix.prerelease)

    def test_orders_channels_and_shared_maintenance_sequence(self) -> None:
        self.assertLess(
            parse_version("0.6.2-alpha.9").order_key,
            parse_version("0.6.2-preview.1").order_key,
        )
        self.assertLess(
            parse_version("0.6.2-preview.9").order_key,
            parse_version("0.6.2-rc.1").order_key,
        )
        self.assertLess(
            parse_version("0.6.2-public.hotfix.1").order_key,
            parse_version("0.6.2-public.revision.2").order_key,
        )

    def test_validates_android_version_code_layout(self) -> None:
        self.assertEqual(1, validate_version_code(parse_version("0.6.2-alpha.1"), 6020001))
        self.assertEqual(2, validate_version_code(parse_version("0.6.2-rc.2"), 6022002))
        self.assertEqual(0, validate_version_code(parse_version("0.6.2"), 6029000))
        self.assertEqual(
            3,
            validate_version_code(parse_version("0.6.2-public.repack.3"), 6029003),
        )
        with self.assertRaises(ValueError):
            validate_version_code(parse_version("0.6.2-public.hotfix.2"), 6029001)

    def test_rejects_prerelease_without_positive_sequence(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive sequence"):
            validate_version_code(parse_version("0.6.2-alpha"), 6020000)

    def test_marks_only_old_grammar_as_bridge_compatible(self) -> None:
        self.assertTrue(is_legacy_compatible("0.6.2"))
        self.assertTrue(is_legacy_compatible("0.6.2-public.1"))
        self.assertFalse(is_legacy_compatible("0.6.2-alpha.1"))
        self.assertFalse(is_legacy_compatible("0.6.2-public.hotfix.1"))

    def test_cli_description_is_machine_readable(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "x360_versioning.py"),
                "describe",
                "0.6.2-public.hotfix.1",
                "6029001",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        value = json.loads(result.stdout)
        self.assertEqual("public", value["channel"])
        self.assertEqual("hotfix", value["maintenanceKind"])
        self.assertEqual(1, value["publicationSequence"])
        self.assertFalse(value["prerelease"])


if __name__ == "__main__":
    unittest.main()
