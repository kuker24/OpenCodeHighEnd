#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from lib.common import load_policy, product_version  # noqa: E402

SNAPSHOT = {
    "browser-act",
    "chrome-devtools-axi",
    "emil-design-eng",
    "found-this-design",
    "full-audit-keamanan",
    "full-performance-audit",
    "gh-axi",
    "scroll-world",
    "visual-studio",
}


class LicenseAuditTests(unittest.TestCase):
    def test_every_skill_is_audited(self):
        allow, _, _, _ = load_policy(ROOT)
        audit = json.loads((ROOT / "vendor" / "license-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(set(allow), set(audit["skills"]))
        unknown = {k for k, v in audit["skills"].items() if v.get("redistribution") == "unknown"}
        self.assertEqual(unknown, set())
        for name in SNAPSHOT:
            self.assertEqual(audit["skills"][name]["license"], "MIT")
            self.assertEqual(audit["skills"][name]["redistribution"], "mit")
        grok = ROOT / "vendor" / "licenses" / "GROKBESTFRIEND-MIT.txt"
        self.assertTrue(grok.is_file())
        self.assertIn("GrokBestFriend contributors", grok.read_text(encoding="utf-8"))

    def test_sources_license_files_exist(self):
        sources = json.loads((ROOT / "vendor" / "sources.json").read_text(encoding="utf-8"))["sources"]
        pinned = []
        for name, spec in sources.items():
            rel = spec.get("licenseFile")
            if not rel:
                continue
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"{name} licenseFile missing: {rel}")
            text = path.read_text(encoding="utf-8")
            self.assertGreater(len(text.strip()), 40, rel)
            pinned.append(rel)
        self.assertIn("vendor/licenses/IMPECCABLE-APACHE2.txt", pinned)
        self.assertIn("vendor/licenses/EMILKOWALSKI-MIT.txt", pinned)
        apache = (ROOT / "vendor/licenses/IMPECCABLE-APACHE2.txt").read_text(encoding="utf-8")
        mit = (ROOT / "vendor/licenses/EMILKOWALSKI-MIT.txt").read_text(encoding="utf-8")
        self.assertIn("Copyright 2025 Paul Bakaus", apache)
        self.assertIn("Copyright (c) 2026 Emil Kowalski", mit)

    def test_provenance_version_matches_product(self):
        prov = json.loads((ROOT / "vendor" / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(prov["productVersion"], product_version())
        names = {c["component"] for c in prov["components"]}
        self.assertNotIn("other-user-skills", names)
        self.assertTrue(SNAPSHOT <= names)


if __name__ == "__main__":
    unittest.main()
