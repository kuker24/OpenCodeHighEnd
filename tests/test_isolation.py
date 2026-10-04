#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = (
    "~/.claude/",
    "$HOME/.claude/",
    "claude-gbf",
    "CLAUDE_CODE_",
    "CLAUDE_DESIGN_BANK",
    "grokbestfriend-claude",
    "claude mcp",
)
SKIP_NAMES = {"THIRD_PARTY_NOTICES.md", "provenance.json", "sources.json", "README.md", "CHANGELOG.md", "security.md"}
SKIP_PARTS = {"docs", "licenses", ".git", "tests", ".scratch"}
SKIP_FILES = {("lib", "install.py"), ("lib", "doctor.py")}


class IsolationTests(unittest.TestCase):
    def test_no_active_claude_runtime(self):
        hits = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(p in SKIP_PARTS for p in path.parts):
                continue
            if path.name in SKIP_NAMES:
                continue
            if tuple(path.parts[-2:]) in SKIP_FILES:
                continue
            if path.suffix not in {".md", ".json", ".jsonc", ".mjs", ".js", ".py", ".sh", ""}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for pat in ACTIVE:
                if pat in text:
                    hits.append(f"{path.relative_to(ROOT)}: {pat}")
                    break
        self.assertEqual(hits, [])

    def test_no_personal_path(self):
        hits = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(p in {".git", ".scratch"} for p in path.parts):
                continue
            if path.suffix not in {".md", ".json", ".jsonc", ".mjs", ".js", ".py", ".sh", ".yml", ""}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            needle = "/" + "home" + "/" + "fahmiagent"
            if needle in text:
                hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])

    def test_no_zero_host_bindings(self):
        # 0.0.0.0 must never be configured as a target host or bind address in code or configs
        install_py = (ROOT / "lib" / "install.py").read_text(encoding="utf-8")
        self.assertNotIn("0.0.0.0", install_py)

        mcp_policy = (ROOT / "vendor" / "mcp-policy.json").read_text(encoding="utf-8")
        self.assertNotIn("0.0.0.0", mcp_policy)

        mcp_wanted = (ROOT / "vendor" / "mcp-wanted.json").read_text(encoding="utf-8")
        self.assertNotIn("0.0.0.0", mcp_wanted)

        sources = (ROOT / "vendor" / "sources.json").read_text(encoding="utf-8")
        self.assertNotIn("0.0.0.0", sources)

        # In lib/, 0.0.0.0 can only appear in doctor.py defensive checks
        for p in (ROOT / "lib").rglob("*.py"):
            text = p.read_text(encoding="utf-8")
            if "0.0.0.0" in text:
                self.assertEqual(p.name, "doctor.py", f"Unexpected 0.0.0.0 in {p}")
                self.assertIn("forbidden", text)


if __name__ == "__main__":
    unittest.main()
