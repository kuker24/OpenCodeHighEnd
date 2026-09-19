# Changelog

## Unreleased

## 0.1.1 — 2026-09-19

- Modernized `found-this-design` skill with a local zero-token search engine across 12 universal design banks (Refero, Aura, Motionsites, Scrolltide, Bencho, Layers, Supahero, NavbarGallery, FooterDesign, CtaGallery, 404sDesign, 21st).
- Upgraded Design Bank bootstrap default pin to `OpenCodeHighEnd-DesignBank-v2.zip` (SHA-256 `43b36134c35c476bcdeb633aa55f58ada18a163ade4e867d8fcf9380433b54d2`) with fail-closed checksum verification and Google Drive direct download URL resolution.
- Updated unit test fixtures in `tests/test_design_bootstrap.py` for v2 archive naming, checksums, and version assertions.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.1.

## 0.1.0 — 2026-09-18

First OpenCodeHighEnd release. New product on OpenCode 2. Not OpenCodeBestFriend 1.8.6, not Claude Code, not GrokBuild.

- Catalog inherited frozen from OpenCodeBestFriend 1.8.6 (`67142e4` / PR #29): **62** names (47 model-invoked, 15 manual slash commands).
- Native V2 config: `skills` is an array; MCP lives under `mcp.servers`; every server has `type`; `disabled` replaces V1 `enabled`.
- Installer fails closed on OpenCode 1.x. Gate is major `>= 2`.
- New identity: CLI `opencode-he`, overlay `~/.config/opencode/highend`, share `~/.local/share/opencode-highend`, AGENTS markers `OPENCODEHIGHEND:BEGIN/END`.
- V1 plugins are not copied. `lsp` is not ported. Design Bank / Design V2 / SmartDoc remain user data, never git media.
- Design Bank bootstrap: local valid bank first; `OPENCODE_DESIGN_BANK_URL` + `OPENCODE_DESIGN_BANK_SHA256` (URL without SHA fails closed); default Drive ZIP pin; GitHub `Design-bank.tgz` fallback. Uninstall never deletes `~/Design` or `~/DesignV2`.
- Legacy V1 plugins (`impeccable-live-poll.ts`) quarantined to `~/.local/share/opencode-highend/quarantine/plugins/`; doctor reports `V1_PLUGIN_LEFTOVER`.
- FOREIGN_ON_DEMAND MCP stay enable-gated: serena, stitch, reticle, ui-skills, markitdown; exa is never added/removed/overwritten.
- Retired twins stay retired: `ask-matt`, `grilling`, `wait-what`, `matt-implement`.
- Dropped deprecated `GROK_*` env aliases. Runtime paths never use GrokBuild, `~/.grok`, or `~/.claude`.
