#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "found-this-design"


class FoundThisDesignPathTests(unittest.TestCase):
    def test_no_legacy_or_machine_specific_paths(self):
        forbidden = [
            "bestfriend/config/design-bank.json",
            "LAB GITHUB/Design",
            "LOCAL_KNOWN_BANK",
        ]
        for path in SKILL_DIR.rglob("*"):
            if not path.is_file() or path.suffix in (".png", ".jpg", ".webp", ".mp4"):
                continue
            text = path.read_text(encoding="utf-8")
            for term in forbidden:
                self.assertNotIn(
                    term,
                    text,
                    f"Forbidden path reference '{term}' found in {path.relative_to(ROOT)}",
                )

    def test_highend_config_path_wired(self):
        lib_mjs = (SKILL_DIR / "scripts" / "lib.mjs").read_text(encoding="utf-8")
        self.assertIn(".config/opencode/highend/config/design-bank.json", lib_mjs)

        banks_md = (SKILL_DIR / "references" / "banks.md").read_text(encoding="utf-8")
        self.assertIn("~/.config/opencode/highend/config/design-bank.json", banks_md)
        self.assertIn("~/.local/share/opencode-highend/design-bank", banks_md)

    def test_node_module_loads_cleanly(self):
        res = subprocess.run(
            [
                "node",
                "--input-type=module",
                "-e",
                'import { resolveBankRoot, DEFAULT_BANK } from "./skills/found-this-design/scripts/lib.mjs"; if (typeof resolveBankRoot !== "function") process.exit(1);',
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"lib.mjs failed to import: {res.stderr}")


if __name__ == "__main__":
    unittest.main()
