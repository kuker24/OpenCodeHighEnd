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
from lib.install import detect_opencode, merge_opencode_config, owned_mcp_spec  # noqa: E402


class V2SchemaTests(unittest.TestCase):
    def test_owned_mcp_is_v2(self):
        spec = owned_mcp_spec(Path("/tmp/codebase-memory-mcp"))
        self.assertEqual(set(spec), {"codebase-memory-mcp", "context7", "shadcn"})
        for name, entry in spec.items():
            self.assertIn(entry.get("type"), ("local", "remote"), name)
            self.assertIn("disabled", entry)
            self.assertNotIn("enabled", entry)

    def test_shadcn_mcp_invocation_and_pin(self):
        spec = owned_mcp_spec(Path("/tmp/codebase-memory-mcp"))
        self.assertIn("shadcn", spec)
        shadcn = spec["shadcn"]
        self.assertEqual(shadcn["type"], "local")
        self.assertEqual(shadcn["command"], ["npx", "-y", "shadcn@4.21.0", "mcp"])
        self.assertIn("mcp", shadcn["command"])
        self.assertFalse(shadcn["disabled"])

        sources = jsonc.load_path(ROOT / "vendor" / "sources.json")["sources"]["shadcn"]
        self.assertEqual(sources["version"], "4.21.0")
        self.assertEqual(sources["via"], "npx")

    def test_installer_rejects_opencode_1(self):
        prev = os.environ.get("OPENCODE_HE_MOCK_OPENCODE")
        with tempfile.TemporaryDirectory() as td:
            mock = Path(td) / "opencode"
            mock.write_text("#!/bin/sh\necho 1.18.31\n", encoding="utf-8")
            mock.chmod(0o755)
            os.environ["OPENCODE_HE_MOCK_OPENCODE"] = str(mock)
            from io import StringIO
            from unittest.mock import patch
            buf = StringIO()
            with patch("sys.stderr", buf), self.assertRaises(SystemExit) as ctx:
                detect_opencode()
            self.assertEqual(ctx.exception.code, 1)
            self.assertIn("UNSUPPORTED_OPENCODE_VERSION", buf.getvalue())
            self.assertIn("OpenCode 2.x", buf.getvalue())
        if prev is None:
            os.environ.pop("OPENCODE_HE_MOCK_OPENCODE", None)
        else:
            os.environ["OPENCODE_HE_MOCK_OPENCODE"] = prev

    def test_merge_writes_servers_and_skills_array(self):
        prev_home = os.environ.get("HOME")
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            os.environ["HOME"] = str(home)
            cfg = home / ".config" / "opencode"
            cfg.mkdir(parents=True)
            (cfg / "opencode.jsonc").write_text(
                '{\n  // keep\n  "model": "keep-me-model",\n  "mcp": {\n    "foreign-weather": {\n      "type": "remote",\n      "url": "https://example.invalid/mcp"\n    }\n  }\n}\n',
                encoding="utf-8",
            )
            merge_opencode_config(Path("/tmp/codebase-memory-mcp"))
            data = jsonc.load_path(cfg / "opencode.jsonc")
            self.assertIsInstance(data["skills"], list)
            self.assertIn("~/.config/opencode/skills", data["skills"])
            servers = data["mcp"]["servers"]
            self.assertEqual(servers["shadcn"]["type"], "local")
            self.assertIs(servers["shadcn"]["disabled"], False)
            self.assertEqual(data["mcp"]["foreign-weather"]["url"], "https://example.invalid/mcp")
            self.assertNotIn("lsp", data)
        if prev_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = prev_home


if __name__ == "__main__":
    unittest.main()
