#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from lib.common import load_policy  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FM = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
KEY_RE = re.compile(r"^([a-z][a-z0-9_-]*):\s*(.*)$")
TOKEN_RE = re.compile(r"[a-z0-9]+")
FOREIGN_PATH_RE = re.compile(r"~/\.claude\b")

OVERLAP_WARN = 0.50
OVERLAP_FAIL = 0.75


def frontmatter(path: Path) -> dict[str, str]:
    fm = FM.match(path.read_text(encoding="utf-8"))
    if fm is None:
        return {}
    out: dict[str, str] = {}
    for line in fm.group(1).splitlines():
        m = KEY_RE.match(line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def skill_files() -> list[tuple[str, Path]]:
    found = []
    for base in ("skills", "manual-skills"):
        for path in sorted((ROOT / base).glob("*/SKILL.md")):
            found.append((path.parent.name, path))
    return found


def normalize_license(value: str) -> str:
    text = value.strip().strip('"').strip("'").strip()
    return text.replace("Apache 2.0", "Apache-2.0")


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class SkillPolicyTests(unittest.TestCase):
    def test_counts(self):
        allow, skills, model, manual = load_policy(ROOT)
        self.assertEqual(len(allow), 66)
        self.assertEqual(len(model), 51)
        self.assertEqual(len(manual), 15)
        self.assertEqual(set(allow), set(skills))
        for name in ("supabase-ops", "mongodb-ops", "vercel-ops", "business-motion-film", "ninerouter", "markitdown", "id-demo-video", "json-render", "deck-design", "pageindex", "penulis-ilmiah"):
            self.assertIn(name, allow)
            self.assertIn(name, model)
        self.assertIn("demo-video", manual)

    def test_model_skills_exist(self):
        _, _, model, manual = load_policy(ROOT)
        for name in model:
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(skill.is_file(), name)
            self.assertTrue(NAME_RE.match(name), name)
            text = skill.read_text(encoding="utf-8")
            fm = FM.match(text)
            self.assertIsNotNone(fm, name)
            assert fm is not None
            self.assertNotIn("disable-model-invocation", fm.group(1))
            self.assertNotIn("user-invocable", fm.group(1))
            self.assertTrue((ROOT / "manual-skills" / name).exists() is False)

    def test_manual_not_in_discovery(self):
        _, _, _, manual = load_policy(ROOT)
        for name in manual:
            self.assertTrue((ROOT / "manual-skills" / name / "SKILL.md").is_file(), name)
            self.assertTrue((ROOT / "commands" / f"{name}.md").is_file(), name)
            self.assertFalse((ROOT / "skills" / name).exists(), name)

    def test_rules(self):
        names = {p.name for p in (ROOT / "rules").glob("*.md")}
        self.assertEqual(len(names), 6)
        self.assertNotIn("04-context-guard.md", names)

    def test_policy_matches_measured_tree(self):
        allow, _, model, manual = load_policy(ROOT)
        on_disk_model = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        on_disk_manual = {p.parent.name for p in (ROOT / "manual-skills").glob("*/SKILL.md")}
        on_disk_commands = {p.stem for p in (ROOT / "commands").glob("*.md")}
        self.assertEqual(on_disk_model, set(model))
        self.assertEqual(on_disk_manual, set(manual))
        self.assertEqual(on_disk_commands, set(manual))
        self.assertEqual(len(allow), len(on_disk_model) + len(on_disk_manual))

    def test_no_model_manual_name_collision(self):
        _, _, model, manual = load_policy(ROOT)
        self.assertEqual(set(model) & set(manual), set())
        commands = {p.stem for p in (ROOT / "commands").glob("*.md")}
        self.assertEqual(set(model) & commands, set())


class SkillFrontmatterTests(unittest.TestCase):
    def test_required_keys(self):
        for name, path in skill_files():
            with self.subTest(skill=name):
                fm = frontmatter(path)
                self.assertTrue(fm, name)
                self.assertEqual(fm.get("name"), name)
                self.assertEqual(fm.get("compatibility"), "opencode")
                self.assertTrue((fm.get("description") or "").strip())

    def test_license_evidence(self):
        # A missing frontmatter license is not a grant: vendor/license-audit.json
        # is the evidence source. Frontmatter, when present, must not contradict it.
        audit = json.loads(
            (ROOT / "vendor" / "license-audit.json").read_text(encoding="utf-8")
        )["skills"]
        for name, path in skill_files():
            with self.subTest(skill=name):
                self.assertIn(name, audit, name)
                approved = audit[name]["license"]
                self.assertIn(approved, {"MIT", "Apache-2.0"}, name)
                self.assertTrue(str(audit[name].get("evidence", "")).strip(), name)
                declared = frontmatter(path).get("license")
                if declared:
                    self.assertEqual(normalize_license(declared), approved, name)

    def test_description_overlap(self):
        rows = []
        for name, path in skill_files():
            desc = frontmatter(path).get("description", "")
            rows.append((name, set(TOKEN_RE.findall(desc.lower()))))
        failures = []
        for (left, a), (right, b) in itertools.combinations(rows, 2):
            score = jaccard(a, b)
            if score >= OVERLAP_FAIL:
                failures.append(f"{left} ~ {right} = {score:.2f}")
        self.assertEqual(failures, [], f"description overlap >= {OVERLAP_FAIL}: {failures}")

    def test_no_foreign_runtime_path(self):
        for name, path in skill_files():
            with self.subTest(skill=name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(FOREIGN_PATH_RE.search(text), name)

    def test_research_skill_boundaries(self):
        skill_path = ROOT / "skills" / "research" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        text = skill_path.read_text(encoding="utf-8")
        fm = frontmatter(skill_path)
        desc = fm.get("description", "")
        self.assertIn("web or social data gathering", desc)
        self.assertIn("web-data.md", text)
        self.assertIn("playwright-qa", text)

        ref_path = ROOT / "skills" / "research" / "references" / "web-data.md"
        self.assertTrue(ref_path.is_file())
        ref_text = ref_path.read_text(encoding="utf-8")
        self.assertIn("Backend Selection Ladder", ref_text)
        self.assertIn("Ethical and Safety Boundaries", ref_text)
        self.assertIn("scrapling", ref_text.lower())
        self.assertIn("agent-reach", ref_text.lower())

        # Ensure research description has low overlap with all skills (< 0.50)
        desc_tokens = set(TOKEN_RE.findall(desc.lower()))
        for name, other_path in skill_files():
            if name == "research":
                continue
            other_desc = frontmatter(other_path).get("description", "")
            other_tokens = set(TOKEN_RE.findall(other_desc.lower()))
            score = jaccard(desc_tokens, other_tokens)
            self.assertLess(score, OVERLAP_WARN, f"Overlap between research and {name} is {score:.2f} >= {OVERLAP_WARN}")


class SkillRefreshTests(unittest.TestCase):
    def test_hyperframes_refresh(self):
        comp = (ROOT / "skills" / "hyperframes" / "references" / "composition.md").read_text(encoding="utf-8")
        self.assertIn("data-composition-id", comp)
        self.assertIn("data-width", comp)
        self.assertIn("data-height", comp)
        self.assertIn("data-start", comp)
        self.assertIn("data-duration", comp)
        self.assertNotIn("window.renderFrame", comp)

        render = (ROOT / "skills" / "hyperframes" / "references" / "render.md").read_text(encoding="utf-8")
        self.assertIn("npx hyperframes render", render)
        self.assertIn("Node.js ≥22", render)
        self.assertIn("NOT_CONFIGURED", render)

        brag = (ROOT / "skills" / "hyperframes" / "references" / "brag.md").read_text(encoding="utf-8")
        self.assertIn("data-composition-id", brag)
        self.assertIn("npx hyperframes render . -o brag-output/brag.mp4 -f 60 -q delivery", brag)
        self.assertNotIn("-W 1920", brag)
        self.assertNotIn("-H 1080", brag)
        self.assertNotIn("-d 18", brag)

        skill = (ROOT / "skills" / "hyperframes" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/prompt-patterns.md", skill)
        self.assertIn("npx skills add heygen-com/hyperframes", skill)
        self.assertIn("npx hyperframes skills update", skill)

        notice = (ROOT / "skills" / "hyperframes" / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("v0.8.119", notice)
        self.assertIn("3a0299e851ce", notice)
        self.assertIn("v0.8.122", notice)
        self.assertIn("6037d228441e", notice)

    def test_prompt_patterns_reference(self):
        pat_path = ROOT / "skills" / "hyperframes" / "references" / "prompt-patterns.md"
        self.assertTrue(pat_path.is_file())
        lines = pat_path.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 90)
        content = "\n".join(lines)
        self.assertIn("POINTER_ONLY", content)
        self.assertIn("awesome-opus5-5-videos", content)
        self.assertIn("3d54892e2ae5b0e8d337171e6508bba4cec01ab8", content)
        self.assertNotIn("utm_", content)

        routing = (ROOT / "rules" / "00-routing.md").read_text(encoding="utf-8")
        self.assertIn("prompt-patterns.md", routing)
        self.assertIn("Deterministic HTML composition rendered to video: `/hyperframes`", routing)

    def test_matt_cluster_glossary_migration(self):
        self.assertTrue((ROOT / "skills" / "domain-modeling" / "GLOSSARY-FORMAT.md").is_file())
        self.assertFalse((ROOT / "skills" / "domain-modeling" / "CONTEXT-FORMAT.md").exists())

        dm_skill = (ROOT / "skills" / "domain-modeling" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("GLOSSARY.md", dm_skill)
        self.assertIn("GLOSSARY-MAP.md", dm_skill)
        self.assertIn("Legacy fallback", dm_skill)
        self.assertIn("CONTEXT.md", dm_skill)

        gwd_skill = (ROOT / "skills" / "grill-with-docs" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("GLOSSARY.md", gwd_skill)
        self.assertIn("Legacy fallback", gwd_skill)
        self.assertIn("CONTEXT.md", gwd_skill)

        for rel in [
            "skills/codebase-design/DESIGN-IT-TWICE.md",
            "skills/tdd/SKILL.md",
            "skills/diagnosing-bugs/SKILL.md",
            "manual-skills/improve-codebase-architecture/SKILL.md",
            "manual-skills/why/SKILL.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("GLOSSARY.md", text, f"Expected GLOSSARY.md in {rel}")

    def test_dead_references_removed(self):
        for rel in ["skills/visual-studio/SKILL.md", "skills/scroll-world/SKILL.md"]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("game-asset-core", text, f"Found game-asset-core in {rel}")
            self.assertIn("NOT_APPLICABLE", text, f"Expected NOT_APPLICABLE in {rel}")

    def test_humanizer_refresh(self):
        notice = (ROOT / "skills" / "humanizer" / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("3.1.0", notice)
        self.assertIn("225a6f39ac85", notice)

        patterns = (ROOT / "skills" / "humanizer" / "references" / "patterns.md").read_text(encoding="utf-8")
        self.assertIn("Writing about the document instead of its subject", patterns)
        self.assertIn("Re-explaining context the reader already knows", patterns)


if __name__ == "__main__":
    unittest.main()
