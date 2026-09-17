# Changelog

## Unreleased

## 0.1.0 — 2026-09-18

First OpenCodeHighEnd release. New product on OpenCode 2. Not OpenCodeBestFriend 1.8.6, not Claude Code, not GrokBuild.

- Catalog inherited frozen from OpenCodeBestFriend 1.8.6 (`67142e4` / PR #29): **62** names (47 model-invoked, 15 manual slash commands).
- Native V2 config: `skills` is an array; MCP lives under `mcp.servers`; every server has `type`; `disabled` replaces V1 `enabled`.
- Installer fails closed on OpenCode 1.x. Gate is major `>= 2`.
- New identity: CLI `opencode-he`, overlay `~/.config/opencode/highend`, share `~/.local/share/opencode-highend`, AGENTS markers `OPENCODEHIGHEND:BEGIN/END`.
- V1 plugins are not copied. `lsp` is not ported. Design Bank / Design V2 / SmartDoc remain user data, never git media.
- FOREIGN_ON_DEMAND MCP stay enable-gated: serena, stitch, reticle, ui-skills, markitdown; exa is never added/removed/overwritten.
- Retired twins stay retired: `ask-matt`, `grilling`, `wait-what`, `matt-implement`.
- Dropped deprecated `GROK_*` env aliases. Runtime paths never use GrokBuild, `~/.grok`, or `~/.claude`.
