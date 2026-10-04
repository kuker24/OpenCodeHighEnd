#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from lib.common import load_policy  # noqa: E402

SKILL = ROOT / "skills" / "install-anti-slop"
FM = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)

EXPECTED_RULES = (
    "no-array-filter-map.ts",
    "no-chained-type-assertions.ts",
    "no-conditional-empty-object-spread.ts",
    "no-known-value-widening.ts",
    "no-module-mocking.ts",
    "no-object-parameters.ts",
    "no-reduce-accumulator-copy.ts",
    "no-reflect-apply.ts",
    "no-reflect-get.ts",
    "no-runtime-typeof.ts",
    "no-shape-in-symbol-names.ts",
    "no-unknown-parameters.ts",
    "no-unknown-returns.ts",
    "no-unknown-type-aliases.ts",
    "no-unsafe-dictionary-type.ts",
    "no-widen-then-assert.ts",
    "require-readable-spacing.ts",
    "require-safety-comment-for-type-assertion.ts",
)

EXPECTED_EFFECT_RULES = (
    "no-manual-effect-error-tag.ts",
    "no-manual-tag-comparison.ts",
    "no-manual-tagged-construction.ts",
    "no-service-constructor-imports.ts",
    "prefer-effect-match.ts",
)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


class AntiSlopContractTests(unittest.TestCase):
    def test_policy_model_invoked(self):
        allow, skills, model, manual = load_policy(ROOT)
        self.assertIn("install-anti-slop", allow)
        self.assertEqual(skills["install-anti-slop"]["invocation"], "model")
        self.assertIn("install-anti-slop", model)
        self.assertNotIn("install-anti-slop", manual)
        self.assertFalse((ROOT / "commands" / "install-anti-slop.md").exists())
        self.assertFalse((ROOT / "manual-skills" / "install-anti-slop").exists())

    def test_frontmatter_and_separation_from_unslop(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        fm = FM.match(text)
        self.assertIsNotNone(fm)
        assert fm is not None
        block = fm.group(1)
        self.assertIn("name: install-anti-slop", block)
        self.assertIn("compatibility: opencode", block)
        self.assertIn("license: MIT", block)
        self.assertIn("prose editing (use /unslop)", block)
        self.assertLessEqual(text.count("\n"), 200)

    def test_blob_identity_manifest(self):
        manifest_path = ROOT / "tests" / "fixtures" / "anti-slop-c44ef22-manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest), 38)
        assets = SKILL / "assets" / "anti-slop"
        live_files = {p.relative_to(assets).as_posix() for p in assets.rglob("*") if p.is_file()}
        self.assertEqual(live_files, set(manifest.keys()))
        for rel_path, expected_sha in manifest.items():
            file_path = assets / rel_path
            computed_sha = git_blob_sha(file_path.read_bytes())
            self.assertEqual(computed_sha, expected_sha, f"Blob mismatch for {rel_path}")

    def test_rule_counts_and_registrations(self):
        assets = SKILL / "assets" / "anti-slop"
        rule_files = sorted(p.name for p in (assets / "rules").glob("*.ts"))
        self.assertEqual(len(rule_files), 18)
        self.assertEqual(tuple(rule_files), EXPECTED_RULES)

        effect_files = sorted(p.name for p in (assets / "effect" / "rules").glob("*.ts"))
        self.assertEqual(len(effect_files), 5)
        self.assertEqual(tuple(effect_files), EXPECTED_EFFECT_RULES)

        index_ts = (assets / "index.ts").read_text(encoding="utf-8")
        effect_index_ts = (assets / "effect" / "index.ts").read_text(encoding="utf-8")
        for r in EXPECTED_RULES:
            name = r[:-3]
            self.assertIn(f'"{name}":', index_ts)
        for r in EXPECTED_EFFECT_RULES:
            name = r[:-3]
            self.assertIn(f'"{name}":', effect_index_ts)

    def test_license_and_sources_inventory(self):
        audit = json.loads((ROOT / "vendor" / "license-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["skills"]["install-anti-slop"]["license"], "MIT")
        self.assertEqual(audit["skills"]["install-anti-slop"]["redistribution"], "mit")
        lic = ROOT / "vendor" / "licenses" / "DMMULROY-ANTI-SLOP-MIT.txt"
        self.assertTrue(lic.is_file())
        text = lic.read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Dillon Mulroy", text)

        # eslint-stylistic license checks
        stylistic_lic = ROOT / "vendor" / "licenses" / "ESLINT-STYLISTIC-MIT.txt"
        self.assertTrue(stylistic_lic.is_file())
        st_text = stylistic_lic.read_text(encoding="utf-8")
        self.assertIn("Copyright OpenJS Foundation and other contributors", st_text)
        self.assertIn("Copyright (c) 2023-PRESENT ESLint Stylistic contributors", st_text)

        upstream_lic = SKILL / "assets" / "anti-slop" / "vendor" / "eslint-stylistic" / "LICENSE"
        self.assertTrue(upstream_lic.is_file())
        self.assertEqual(stylistic_lic.read_text(encoding="utf-8"), upstream_lic.read_text(encoding="utf-8"))

        tp = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("eslint-stylistic", tp)

        sources = json.loads((ROOT / "vendor" / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual(
            sources["sources"]["anti-slop"]["commit"],
            "c44ef22ca116d0ba62a3ff663a0bd13a3f3fa40b",
        )
        self.assertEqual(sources["sources"]["anti-slop"]["version"], "0.1.2+c44ef22")
        self.assertEqual(
            sources["sources"]["eslint-stylistic"]["commit"],
            "435c3ea0fd26a5fef9042c4b36b6e165fbbf8d08",
        )

    def test_install_and_update_reference_blobs(self):
        install_mjs = SKILL / "scripts" / "install.mjs"
        self.assertEqual(git_blob_sha(install_mjs.read_bytes()), "db1f155bd15c065ddb6024042dea7ca4992551b2")

        update_md = SKILL / "references" / "update.md"
        self.assertEqual(git_blob_sha(update_md.read_bytes()), "b2e7f6751a7a97406b768ed5bf950d883c17e9a6")

    def test_manage_script_audit_mode_zero_mutations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manage_script = SKILL / "scripts" / "manage.mjs"
            res = subprocess.run(
                ["node", str(manage_script), "audit", "--json"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(res.stdout)
            self.assertEqual(data["mode"], "audit")
            self.assertEqual(data["mutations"], 0)
            self.assertTrue(data["clean"])
            self.assertEqual(list(Path(tmpdir).iterdir()), [])

    def test_manage_script_install_recommended_update_and_remove(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manage_script = SKILL / "scripts" / "manage.mjs"
            # 1. Install recommended
            res = subprocess.run(
                ["node", str(manage_script), "install", "--profile", "recommended"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Installed anti-slop plugin (recommended)", res.stdout)
            copied_entry = Path(tmpdir) / "tools" / "oxlint" / "anti-slop" / "index.ts"
            self.assertTrue(copied_entry.is_file())
            config_ts = Path(tmpdir) / "oxlint.config.ts"
            self.assertTrue(config_ts.is_file())
            content = config_ts.read_text(encoding="utf-8")
            self.assertIn("anti-slop/no-chained-type-assertions", content)
            self.assertIn("anti-slop/no-widen-then-assert", content)

            # 2. Re-install without force refuses overwrite
            res_refuse = subprocess.run(
                ["node", str(manage_script), "install", "--profile", "recommended"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(res_refuse.returncode, 0)
            self.assertIn("Refusing to overwrite", res_refuse.stderr)

            # 3. Update without --force is non-destructive dry-run (zero mutations)
            mtime_before = copied_entry.stat().st_mtime_ns
            res_dry_update = subprocess.run(
                ["node", str(manage_script), "update", "--json"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            dry_data = json.loads(res_dry_update.stdout)
            self.assertEqual(dry_data["mode"], "update")
            self.assertTrue(dry_data["dryRun"])
            self.assertEqual(dry_data["mutations"], 0)
            self.assertEqual(copied_entry.stat().st_mtime_ns, mtime_before)

            # 4. Update with --force succeeds and overwrites/applies
            res_update = subprocess.run(
                ["node", str(manage_script), "update", "--force", "--profile", "recommended"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Installed anti-slop plugin (recommended)", res_update.stdout)

            # 5. Remove
            res_remove = subprocess.run(
                ["node", str(manage_script), "remove"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Removed anti-slop", res_remove.stdout)
            self.assertFalse(copied_entry.exists())
            self.assertFalse(config_ts.exists())

    def test_manage_script_strict_and_effect_options(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manage_script = SKILL / "scripts" / "manage.mjs"
            res = subprocess.run(
                ["node", str(manage_script), "install", "--profile", "strict", "--with-effect"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Installed anti-slop plugin (strict)", res.stdout)
            config_ts = Path(tmpdir) / "oxlint.config.ts"
            content = config_ts.read_text(encoding="utf-8")
            self.assertIn("anti-slop/no-module-mocking", content)
            self.assertIn("anti-slop/no-array-filter-map", content)
            self.assertIn("anti-slop/no-reduce-accumulator-copy", content)
            self.assertIn("anti-slop/require-readable-spacing", content)
            self.assertIn("oxc/no-accumulating-spread", content)
            self.assertIn("anti-slop-effect/no-service-constructor-imports", content)
            self.assertIn("anti-slop-effect/no-manual-effect-error-tag", content)
            self.assertIn("anti-slop-effect/no-manual-tag-comparison", content)
            self.assertIn("anti-slop-effect/no-manual-tagged-construction", content)
            self.assertIn("anti-slop-effect/prefer-effect-match", content)


if __name__ == "__main__":
    unittest.main()
