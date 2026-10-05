#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from lib import jsonc  # noqa: E402
from lib.common import load_policy, repo_root  # noqa: E402


class PenulisIlmiahTests(unittest.TestCase):
    def test_skill_structure_and_frontmatter(self):
        skill_dir = ROOT / "skills" / "penulis-ilmiah"
        skill_md = skill_dir / "SKILL.md"
        self.assertTrue(skill_md.is_file())

        text = skill_md.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"))
        parts = text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3)

        fm_text = parts[1]
        self.assertIn("name: penulis-ilmiah", fm_text)
        self.assertIn("compatibility: opencode", fm_text)
        self.assertIn("license: MIT", fm_text)
        self.assertIn("lang: id", fm_text)
        self.assertIn("mcp: penulis-ilmiah", fm_text)

        # Boundaries & rules
        self.assertIn("academic", text)
        self.assertIn("humanizer", text)
        self.assertIn("smartdoc", text)
        self.assertIn("research", text)
        self.assertIn("fail-closed", text.lower())

    def test_references_and_kata_baku_catalog(self):
        ref_dir = ROOT / "skills" / "penulis-ilmiah" / "references"
        self.assertTrue((ref_dir / "README.md").is_file())
        self.assertTrue((ref_dir / "kata_baku.md").is_file())
        self.assertTrue((ref_dir / "gaya_tulisan.md").is_file())
        self.assertTrue((ref_dir / "gaya_sitasi.md").is_file())
        self.assertTrue((ref_dir / "frasa_terlarang.md").is_file())
        self.assertTrue((ref_dir / "eyd" / "README.md").is_file())
        self.assertTrue((ref_dir / "eyd" / "04_kata_depan.md").is_file())
        self.assertTrue((ref_dir / "eyd" / "05_imbuhan_kata_turunan.md").is_file())
        self.assertTrue((ref_dir / "eyd" / "10_tanda_baca.md").is_file())

        # Validate kata_baku.md has >= 100 entries
        kb_text = (ref_dir / "kata_baku.md").read_text(encoding="utf-8")
        entries = 0
        for line in kb_text.splitlines():
            line = line.strip()
            if line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
                cols = [c.strip() for c in line.split("|")]
                if len(cols) >= 6 and cols[2] and cols[3]:
                    entries += 1
        self.assertGreaterEqual(entries, 100, f"Expected >= 100 kata baku entries, found {entries}")

    def test_mcp_package_files(self):
        mcp_dir = ROOT / "mcp" / "penulis-ilmiah"
        self.assertTrue((mcp_dir / "package.json").is_file())
        self.assertTrue((mcp_dir / "tsconfig.json").is_file())
        self.assertTrue((mcp_dir / "README.md").is_file())
        self.assertTrue((mcp_dir / ".env.example").is_file())
        self.assertTrue((mcp_dir / "src" / "index.ts").is_file())
        self.assertTrue((mcp_dir / "src" / "tools" / "cek_ejaan.ts").is_file())
        self.assertTrue((mcp_dir / "src" / "tools" / "cek_baku.ts").is_file())
        self.assertTrue((mcp_dir / "src" / "tools" / "cari_rujukan.ts").is_file())
        self.assertTrue((mcp_dir / "src" / "tools" / "verifikasi_rujukan.ts").is_file())
        self.assertTrue((mcp_dir / "src" / "tools" / "format_sitasi.ts").is_file())

        pkg = json.loads((mcp_dir / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(pkg["name"], "penulis-ilmiah-mcp")
        self.assertIn("@modelcontextprotocol/sdk", pkg["dependencies"])
        self.assertIn("citation-js", pkg["dependencies"])
        self.assertIn("zod", pkg["dependencies"])

    def test_mcp_tools_execution(self):
        mcp_dir = ROOT / "mcp" / "penulis-ilmiah"
        # Script running inside node to test tools unit behavior
        script = """
import { cekEjaan } from "./dist/tools/cek_ejaan.js";
import { cekBaku } from "./dist/tools/cek_baku.js";
import { verifikasiRujukan } from "./dist/tools/verifikasi_rujukan.js";
import { formatSitasi } from "./dist/tools/format_sitasi.js";

async function testAll() {
  const e1 = await cekEjaan({ teks: "Mahasiswa belajar dikantor setiap sore.", pakai_hunspell: false, bahasa: "id" });
  if (e1.ok || e1.temuan.length === 0 || e1.temuan[0].saran[0] !== "di kantor") {
    throw new Error("E1 failed: " + JSON.stringify(e1));
  }

  const e4 = await cekEjaan({ teks: "Naskah di tulis ulang oleh editor.", pakai_hunspell: false, bahasa: "id" });
  if (e4.ok || e4.temuan.length === 0 || e4.temuan[0].saran[0] !== "ditulis") {
    throw new Error("E4 failed: " + JSON.stringify(e4));
  }

  const b1 = await cekBaku({ teks: "Aktipitas analisa perlu metoda yang tepat.", fallback_kbbi: false, max_lookup: 20 });
  const b1Words = b1.temuan.map(t => t.kata.toLowerCase());
  if (!b1Words.includes("aktipitas") || !b1Words.includes("analisa") || !b1Words.includes("metoda")) {
    throw new Error("B1 failed: " + JSON.stringify(b1));
  }

  const vFake = await verifikasiRujukan({ doi: "10.9999/fake.doi.12345.never.exists", ambang_judul: 0.85 });
  if (vFake.status !== "TIDAK_DITEMUKAN") {
    throw new Error("vFake status should be TIDAK_DITEMUKAN, got " + vFake.status);
  }

  const fFail = await formatSitasi({
    gaya: "apa7",
    item: { doi: "10.9999/fake.doi.12345.never.exists", judul: "Nonexistent Paper" },
    wajib_terverifikasi: true
  });
  if (!("error" in fFail) || fFail.error.code !== "REF_NOT_VERIFIED") {
    throw new Error("fFail should reject non-verified reference with REF_NOT_VERIFIED");
  }

  console.log("NODE_TESTS_PASS");
}

testAll().catch(err => {
  console.error(err);
  process.exit(1);
});
"""
        proc = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=mcp_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        self.assertEqual(proc.returncode, 0, f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        self.assertIn("NODE_TESTS_PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
