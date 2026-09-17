#!/usr/bin/env python3
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from lib import jsonc  # noqa: E402
from lib.install import merge_opencode_config  # noqa: E402


class JsoncMergeTests(unittest.TestCase):
    def setUp(self):
        self.prev_home = os.environ.get("HOME")

    def tearDown(self):
        if self.prev_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self.prev_home

    def test_strip_comments(self):
        data = jsonc.loads('{ // c\n "a": 1, /* x */ "b": 2, }')
        self.assertEqual(data["a"], 1)
        self.assertEqual(data["b"], 2)

    def test_preserves_foreign_and_provider(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            os.environ["HOME"] = str(home)
            cfg = home / ".config" / "opencode"
            cfg.mkdir(parents=True)
            src = (ROOT / "tests" / "fixtures" / "opencode.jsonc").read_text(encoding="utf-8")
            (cfg / "opencode.jsonc").write_text(src, encoding="utf-8")
            merge_opencode_config(Path("/tmp/codebase-memory-mcp"))
            data = jsonc.load_path(cfg / "opencode.jsonc")
            self.assertEqual(data["model"], "keep-me-model")
            self.assertEqual(data["small_model"], "keep-me-small")
            self.assertIn("example", data["provider"])
            self.assertEqual(data["permission"]["bash"], "ask")
            self.assertEqual(data["mcp"]["foreign-weather"]["url"], "https://example.invalid/mcp")
            servers = data["mcp"]["servers"]
            self.assertIn("codebase-memory-mcp", servers)
            self.assertIn("context7", servers)
            self.assertIn("shadcn", servers)
            self.assertEqual(servers["context7"]["type"], "remote")
            self.assertIs(servers["context7"]["disabled"], False)
            self.assertIsInstance(data["skills"], list)
            self.assertIn("~/.config/opencode/skills", data["skills"])
            self.assertNotIn("compaction", data)
            self.assertNotIn("lsp", data)

    def test_comment_preserving_mcp_upsert(self):
        raw = """{
  // keep this comment
  "model": "keep-me-model",
  "mcp": {
    "foreign-weather": {
      "type": "remote",
      "url": "https://example.invalid/mcp",
      "enabled": true
    }
  }
}
"""
        self.assertTrue(jsonc.contains_comments(raw))
        merged = jsonc.upsert_mcp_servers(
            raw,
            {
                "context7": {
                    "type": "remote",
                    "url": "https://mcp.context7.com/mcp",
                    "disabled": False,
                }
            },
        )
        self.assertIn("keep this comment", merged)
        self.assertIn("foreign-weather", merged)
        data = jsonc.loads(merged)
        self.assertEqual(data["model"], "keep-me-model")
        self.assertIn("context7", data["mcp"]["servers"])
        self.assertIn("foreign-weather", data["mcp"])
        self.assertEqual(data["mcp"]["servers"]["context7"]["type"], "remote")


if __name__ == "__main__":
    unittest.main()
