#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
import io
import json
import os
import shutil
from contextlib import redirect_stdout

from lib import jsonc  # noqa: E402
from lib.doctor import cmd_doctor, owned_agents_block, parse_mcp_list  # noqa: E402
from lib.install import (  # noqa: E402
    cmd_crawl4ai_disable,
    cmd_crawl4ai_enable,
    cmd_penulis_ilmiah_disable,
    cmd_penulis_ilmiah_enable,
    cmd_scrapling_disable,
    cmd_scrapling_enable,
    cmd_install,
)
from lib.integrity import cmd_verify  # noqa: E402
from tests.support import IsolatedHome  # noqa: E402


class McpListParserTests(unittest.TestCase):
    def test_per_server_connected_vs_disconnected(self):
        text = """
codebase-memory-mcp connected
context7 disconnected
shadcn connected
"""
        out = parse_mcp_list(text)
        self.assertEqual(out["codebase-memory-mcp"], "CONNECTED")
        self.assertEqual(out["context7"], "DISCONNECTED")
        self.assertEqual(out["shadcn"], "CONNECTED")

    def test_disconnected_is_not_connected_substring(self):
        text = "context7 disconnected\n"
        out = parse_mcp_list(text)
        self.assertEqual(out["context7"], "DISCONNECTED")
        self.assertEqual(out["codebase-memory-mcp"], "NOT_CHECKED")
        self.assertEqual(out["shadcn"], "NOT_CHECKED")

    def test_skips_ambiguous_multi_name_line(self):
        text = "codebase-memory-mcp connected context7 disconnected\n"
        out = parse_mcp_list(text)
        self.assertEqual(out["codebase-memory-mcp"], "NOT_CHECKED")
        self.assertEqual(out["context7"], "NOT_CHECKED")

    def test_strips_ansi_and_parses_connected(self):
        text = "\x1b[0m\n●  ✓ codebase-memory-mcp \x1b[90mconnected\n"
        out = parse_mcp_list(text)
        self.assertEqual(out["codebase-memory-mcp"], "CONNECTED")

    def test_path_line_does_not_downgrade_connected(self):
        text = """
●  ✓ codebase-memory-mcp connected
│      /home/u/.local/share/opencode-highend/components/codebase-memory/bin/codebase-memory-mcp
●  ✓ context7 connected
│      https://mcp.context7.com/mcp
●  ✓ shadcn connected
│      npx -y shadcn@4.21.0 mcp
"""
        out = parse_mcp_list(text)
        self.assertEqual(out["codebase-memory-mcp"], "CONNECTED")
        self.assertEqual(out["context7"], "CONNECTED")
        self.assertEqual(out["shadcn"], "CONNECTED")

    def test_shadcn_mcp_subcommand_probe(self):
        text = "●  ✓ shadcn connected\n│      npx -y shadcn@4.21.0 mcp\n"
        out = parse_mcp_list(text)
        self.assertEqual(out["shadcn"], "CONNECTED")


class AgentsBlockTests(unittest.TestCase):
    def test_owned_block_ignores_foreign_text(self):
        text = ("USER\n" * 200) + "<!-- OPENCODEHIGHEND:BEGIN -->\nrouter\n<!-- OPENCODEHIGHEND:END -->\n"
        block = owned_agents_block(text)
        self.assertIsNotNone(block)
        self.assertLessEqual(block.count("\n"), 5)
        self.assertGreater(text.count("\n"), 120)


class DoctorDeepTests(IsolatedHome):
    def _install(self):
        self.assertEqual(cmd_install(), 0)

    def test_deep_all_connected_exits_0(self):
        self._install()
        self.write_mcp_list(
            "codebase-memory-mcp connected\ncontext7 connected\nshadcn connected\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONNECTED", buf.getvalue())

    def test_deep_one_disconnected_exits_1(self):
        self._install()
        self.write_mcp_list(
            "codebase-memory-mcp connected\ncontext7 disconnected\nshadcn connected\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("DISCONNECTED", buf.getvalue())

    def test_deep_not_checked_exits_1(self):
        self._install()
        self.write_mcp_list("codebase-memory-mcp connected\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 1, buf.getvalue())

    def test_deep_empty_list_exits_1(self):
        self._install()
        os.environ.pop("OPENCODE_HE_MOCK_MCP_LIST", None)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 1, buf.getvalue())

    def test_deep_command_failure_exits_1(self):
        self._install()
        self.write_mcp_list("codebase-memory-mcp connected\ncontext7 connected\nshadcn connected\n")
        os.environ["OPENCODE_HE_MOCK_MCP_LIST_RC"] = "1"
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 1, buf.getvalue())

    def test_non_deep_does_not_claim_connected(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=False)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertNotIn("PASS                   mcp:context7                 CONNECTED", buf.getvalue())
        self.assertIn("CONFIGURED", buf.getvalue())

    def test_stale_agents_detected(self):
        self._install()
        agents = self.tmp / ".config" / "opencode" / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        text = text.replace("USED", "NOPE").replace("CONSIDERED_NOT_USED", "X").replace("MANUAL_NOT_INVOKED", "Y")
        agents.write_text(text, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("STALE", buf.getvalue())
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cmd_verify(), 1)

    def test_installed_design_v2_runtime_drift_detected(self):
        self._install()
        runtime = (
            self.tmp
            / ".local"
            / "share"
            / "opencode-highend"
            / "product"
            / "lib"
            / "design_v2"
            / "search.py"
        )
        runtime.write_text(runtime.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_verify()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("DRIFT", buf.getvalue())
        self.assertIn("product/lib/design_v2/search.py", buf.getvalue())

    def test_missing_installed_design_v2_runtime_detected(self):
        self._install()
        runtime = (
            self.tmp
            / ".local"
            / "share"
            / "opencode-highend"
            / "product"
            / "lib"
            / "design_v2"
            / "search.py"
        )
        runtime.unlink()
        os.environ["OPENCODE_HE_ROOT"] = str(
            self.tmp / ".local" / "share" / "opencode-highend" / "product"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_verify()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("MISSING", buf.getvalue())
        self.assertIn("product/lib/design_v2/search.py", buf.getvalue())

    def test_stale_routing_detected(self):
        self._install()
        routing = self.tmp / ".config" / "opencode" / "highend" / "rules" / "00-routing.md"
        routing.write_text("# Claude Code specialist routing (opencode-highend)\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("STALE", buf.getvalue())

    def test_context_guard_not_pass(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_doctor()
        out = buf.getvalue()
        self.assertIn("NOT_APPLICABLE", out)
        self.assertIn("NOT_PORTED_BY_DESIGN", out)
        self.assertNotIn("PASS                   Context Guard", out)

    def test_permission_wildcard_degraded_strict_fails(self):
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        cfg.write_text(
            """{
  "permission": { "*": "allow" },
  "mcp": {}
}
""",
            encoding="utf-8",
        )
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("DEGRADED_SECURITY", buf.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=True)
        self.assertEqual(rc, 1, buf.getvalue())

    def test_shadcn_requires_node_npx(self):
        self._install()
        empty = self.tmp / "empty-bin"
        empty.mkdir()
        py = shutil.which("python3")
        self.assertIsNotNone(py)
        os.symlink(py, empty / "python3")
        os.environ["PATH"] = str(empty)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        os.environ["PATH"] = self.prev["PATH"] or ""
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertTrue("npx" in buf.getvalue() or "node" in buf.getvalue())

    def test_doctor_stitch_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:stitch", buf.getvalue())

    def test_doctor_deep_stitch_missing_does_not_fail(self):
        self._install()
        self.write_mcp_list(
            "codebase-memory-mcp connected\ncontext7 connected\nshadcn connected\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(deep=True)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:stitch", buf.getvalue())

    def test_doctor_stitch_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["stitch"] = {
            "type": "local",
            "command": ["stitch-bin"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:stitch", buf.getvalue())

    def test_doctor_stitch_valid_configured_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["stitch"] = {
            "type": "remote",
            "url": "https://stitch.googleapis.com/mcp",
            "enabled": True,
            "headers": {"X-Goog-Api-Key": "{env:STITCH_API_KEY}"},
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:stitch", buf.getvalue())

    def test_doctor_reticle_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:reticle", buf.getvalue())

    def test_doctor_reticle_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["reticle"] = {
            "type": "remote",
            "url": "https://example.invalid",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:reticle", buf.getvalue())

    def test_doctor_reticle_valid_configured_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["reticle"] = {
            "type": "local",
            "command": ["npx", "-y", "@reticlehq/server", "mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:reticle", buf.getvalue())

    def test_doctor_ui_skills_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:ui-skills", buf.getvalue())

    def test_doctor_ui_skills_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["ui-skills"] = {
            "type": "local",
            "command": ["ui-skills-bin"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:ui-skills", buf.getvalue())

    def test_doctor_ui_skills_valid_configured_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["ui-skills"] = {
            "type": "remote",
            "url": "https://www.ui-skills.com/mcp",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:ui-skills", buf.getvalue())

    def test_doctor_markitdown_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:markitdown", buf.getvalue())

    def test_doctor_markitdown_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["markitdown"] = {
            "type": "local",
            "command": ["docker", "run", "--rm", "-i", "-p", "0.0.0.0:3001:3001", "markitdown-mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:markitdown", buf.getvalue())

    def test_doctor_markitdown_http_bind_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["markitdown"] = {
            "type": "local",
            "command": ["uvx", "--from", "markitdown-mcp", "markitdown-mcp", "--http", "0.0.0.0"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:markitdown", buf.getvalue())

    def test_doctor_markitdown_valid_configured_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["markitdown"] = {
            "type": "local",
            "command": ["uvx", "--from", "markitdown-mcp", "markitdown-mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("WARN                   mcp:markitdown               MARKITDOWN_UNPINNED", buf.getvalue())
        data["mcp"]["markitdown"]["command"] = [
            "uvx",
            "--from",
            "markitdown-mcp==0.0.1a7",
            "--with",
            "markitdown[all]==0.1.8",
            "markitdown-mcp",
        ]
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:markitdown", buf.getvalue())

    def test_doctor_markitdown_legacy_version_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["markitdown"] = {
            "type": "local",
            "command": ["uvx", "--from", "markitdown-mcp==0.1.8", "markitdown-mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:markitdown", buf.getvalue())
        self.assertIn("opencode-he markitdown enable", buf.getvalue())

    def test_doctor_crawl4ai_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_zero_bind_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "http://0.0.0.0:11235/mcp",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_invalid_url_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "http://127.0.0.1:9999/mcp",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_cloud_raw_secret_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "https://api.crawl4ai.com/mcp",
            "headers": {"Authorization": "Bearer raw_secret_key_123"},
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_cloud_missing_token_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "https://api.crawl4ai.com/mcp",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_valid_local_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "http://127.0.0.1:11235/mcp/sse",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:crawl4ai", buf.getvalue())

        # Legacy URL triggers WARN
        data["mcp"]["crawl4ai"]["url"] = "http://127.0.0.1:11235/mcp"
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("WARN                   mcp:crawl4ai                 CRAWL4AI_LEGACY_URL", buf.getvalue())

    def test_doctor_crawl4ai_valid_cloud_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["crawl4ai"] = {
            "type": "remote",
            "url": "https://api.crawl4ai.com/mcp",
            "headers": {"Authorization": "Bearer {env:CRAWL4AI_KEY}"},
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_enable_local_and_disable(self):
        self._install()
        rc = cmd_crawl4ai_enable()
        self.assertEqual(rc, 0)
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertIn("crawl4ai", servers)
        self.assertEqual(servers["crawl4ai"]["url"], "http://127.0.0.1:11235/mcp/sse")
        self.assertNotIn("0.0.0.0", str(servers["crawl4ai"]))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:crawl4ai", buf.getvalue())
        rc = cmd_crawl4ai_disable()
        self.assertEqual(rc, 0)
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertNotIn("crawl4ai", servers)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:crawl4ai", buf.getvalue())

    def test_doctor_crawl4ai_enable_cloud(self):
        self._install()
        os.environ["CRAWL4AI_KEY"] = "super-secret-key-999"
        try:
            rc = cmd_crawl4ai_enable(cloud=True)
            self.assertEqual(rc, 0)
            cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
            raw_text = cfg.read_text(encoding="utf-8")
            self.assertNotIn("super-secret-key-999", raw_text)
            self.assertIn("{env:CRAWL4AI_KEY}", raw_text)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_doctor()
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertIn("CONFIGURED             mcp:crawl4ai", buf.getvalue())
        finally:
            os.environ.pop("CRAWL4AI_KEY", None)

    def test_doctor_plugins_clean_when_absent(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("PASS                   plugins                      0 (directory absent)", buf.getvalue())

    def test_doctor_plugins_warns_on_v1_leftover(self):
        self._install()
        pdir = self.tmp / ".config" / "opencode" / "plugins"
        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "impeccable-live-poll.ts").write_text("import type { Plugin } from '@opencode-ai/plugin';", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=False)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("WARN                   plugins                      V1_PLUGIN_LEFTOVER impeccable-live-poll.ts", buf.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf):
            strict_rc = cmd_doctor(strict=True)
        self.assertEqual(strict_rc, 1, buf.getvalue())

    def test_doctor_plugins_pass_on_user_v2_plugin(self):
        self._install()
        pdir = self.tmp / ".config" / "opencode" / "plugins"
        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "my-custom.ts").write_text("export default { id: 'my-custom' };", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("PASS                   plugins                      1 user plugin(s)", buf.getvalue())

    def test_doctor_scrapling_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:scrapling", buf.getvalue())

    def test_doctor_scrapling_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))

        # Remote type fails
        data["mcp"]["scrapling"] = {
            "type": "remote",
            "url": "http://127.0.0.1:8000/mcp",
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:scrapling", buf.getvalue())

        # Docker command fails
        data["mcp"]["scrapling"] = {
            "type": "local",
            "command": ["docker", "run", "scrapling", "mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:scrapling", buf.getvalue())

        # --http or 0.0.0.0 fails
        data["mcp"]["scrapling"] = {
            "type": "local",
            "command": ["uvx", "--from", "scrapling[ai]==0.4.15", "scrapling", "mcp", "--http", "0.0.0.0"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:scrapling", buf.getvalue())

        # Unpinned package fails
        data["mcp"]["scrapling"] = {
            "type": "local",
            "command": ["uvx", "--from", "scrapling", "scrapling", "mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("FAIL                   mcp:scrapling", buf.getvalue())

    def test_doctor_scrapling_valid_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["scrapling"] = {
            "type": "local",
            "command": ["uvx", "--from", "scrapling[ai]==0.4.15", "scrapling", "mcp"],
            "enabled": True,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:scrapling", buf.getvalue())

    def test_doctor_scrapling_enable_and_disable(self):
        self._install()
        rc = cmd_scrapling_enable()
        self.assertEqual(rc, 0)
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertIn("scrapling", servers)
        self.assertEqual(servers["scrapling"]["type"], "local")
        self.assertEqual(servers["scrapling"]["command"], ["uvx", "--from", "scrapling[ai]==0.4.15", "scrapling", "mcp"])
        self.assertNotIn("0.0.0.0", str(servers["scrapling"]))

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:scrapling", buf.getvalue())

        rc = cmd_scrapling_disable()
        self.assertEqual(rc, 0)
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertNotIn("scrapling", servers)

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:scrapling", buf.getvalue())

    def test_doctor_penulis_ilmiah_missing_does_not_fail(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:penulis-ilmiah", buf.getvalue())

    def test_doctor_penulis_ilmiah_invalid_schema_fails(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data.setdefault("mcp", {})
        data["mcp"].setdefault("servers", {})

        # Type remote fails
        data["mcp"]["servers"]["penulis-ilmiah"] = {
            "type": "remote",
            "url": "http://127.0.0.1:8000/mcp",
        }
        cfg.write_text(json.dumps(data, indent=2), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1)
        self.assertIn("FAIL                   mcp:penulis-ilmiah", buf.getvalue())

        # Forbidden 0.0.0.0 or --http fails
        data["mcp"]["servers"]["penulis-ilmiah"] = {
            "type": "local",
            "command": ["npx", "tsx", "mcp/penulis-ilmiah/src/index.ts", "--http", "0.0.0.0"],
        }
        cfg.write_text(json.dumps(data, indent=2), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 1)
        self.assertIn("FAIL                   mcp:penulis-ilmiah", buf.getvalue())

    def test_doctor_penulis_ilmiah_valid_passes(self):
        self._install()
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data.setdefault("mcp", {})
        data["mcp"].setdefault("servers", {})
        data["mcp"]["servers"]["penulis-ilmiah"] = {
            "type": "local",
            "command": ["npx", "tsx", "/path/to/mcp/penulis-ilmiah/src/index.ts"],
        }
        cfg.write_text(json.dumps(data, indent=2), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:penulis-ilmiah", buf.getvalue())

    def test_doctor_penulis_ilmiah_enable_and_disable(self):
        self._install()
        rc = cmd_penulis_ilmiah_enable()
        self.assertEqual(rc, 0)
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertIn("penulis-ilmiah", servers)
        self.assertEqual(servers["penulis-ilmiah"]["type"], "local")
        self.assertTrue(any("penulis-ilmiah" in str(p) for p in servers["penulis-ilmiah"]["command"]))
        self.assertNotIn("0.0.0.0", str(servers["penulis-ilmiah"]))

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("CONFIGURED             mcp:penulis-ilmiah", buf.getvalue())

        rc = cmd_penulis_ilmiah_disable()
        self.assertEqual(rc, 0)
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        servers = jsonc.mcp_servers_from_config(data)
        self.assertNotIn("penulis-ilmiah", servers)

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        mcp:penulis-ilmiah", buf.getvalue())

    def test_doctor_agent_reach_cli_findings(self):
        self._install()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("OPTIONAL_ABSENT        Agent-Reach CLI              NOT_INSTALLED", buf.getvalue())

        # Mock agent-reach in mock-bin
        ar_bin = self.tmp / "bin" / "agent-reach"
        ar_bin.parent.mkdir(parents=True, exist_ok=True)
        ar_bin.write_text("#!/bin/sh\necho '1.5.0'\n", encoding="utf-8")
        ar_bin.chmod(0o755)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{ar_bin.parent}:{old_path}"
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_doctor()
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertIn("PASS                   Agent-Reach CLI", buf.getvalue())
            self.assertIn("1.5.0", buf.getvalue())
        finally:
            os.environ["PATH"] = old_path

    def test_doctor_foreign_skill_shadow_warning(self):
        self._install()
        skills_dir = self.tmp / ".config" / "opencode" / "skills"

        # Create unmanaged foreign skill directory
        shadow = skills_dir / "agent-reach"
        shadow.mkdir(parents=True, exist_ok=True)
        (shadow / "SKILL.md").write_text("---\nname: agent-reach\n---\n", encoding="utf-8")

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=False)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("WARN                   FOREIGN_SKILL_SHADOW", buf.getvalue())
        self.assertIn("agent-reach: foreign skill hijacking router", buf.getvalue())

        # With ownership marker, warning should not be emitted
        (shadow / ".opencode-highend.json").write_text("{}", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=False)
        self.assertNotIn("FOREIGN_SKILL_SHADOW", buf.getvalue())

        # Test context7-mcp skill shadow
        c7_shadow = skills_dir / "context7-mcp"
        c7_shadow.mkdir(parents=True, exist_ok=True)
        (c7_shadow / "SKILL.md").write_text("---\nname: context7-mcp\n---\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=False)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("context7-mcp: foreign skill hijacking router", buf.getvalue())
        (c7_shadow / ".opencode-highend.json").write_text("{}", encoding="utf-8")

        # Test context7-mcp server shadow in opencode.jsonc
        cfg = self.tmp / ".config" / "opencode" / "opencode.jsonc"
        data = jsonc.loads(cfg.read_text(encoding="utf-8"))
        data["mcp"]["servers"]["context7-mcp"] = {
            "type": "remote",
            "url": "https://mcp.context7.com/mcp",
            "disabled": False,
        }
        cfg.write_text(jsonc.dumps(data), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_doctor(strict=False)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("WARN                   FOREIGN_MCP_SHADOW", buf.getvalue())
        self.assertIn("context7-mcp: duplicate shadow of context7", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
