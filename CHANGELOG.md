# Changelog

## Unreleased

## 0.1.2 — 2026-09-22

- Aligned done-gate vocabulary in `rules/01-verification.md` explicitly requiring `FACT: <outcome>` (blocking) and `JUDGMENT: <assessment>` (advisory) backed by `rules/decision-log-protocol.md`.
- Documented TypeSafe Jev (`jev-mcp`) as SKIPPED in `docs/mcp.md` and `docs/source-wave.md`, noting Canny verification patterns are absorbed into rules and decision logs without external server dependencies.
- Added upstream disposition for `microsoft/playwright-cli` (REFRESH) in `docs/source-wave.md`.
- Documented `confident-ai/deepteam` as an optional external maintainer-side red-team framework pointer in `skills/full-audit-keamanan/SKILL.md` and `skills/eval-harness/SKILL.md` (non-vendored, no extra dependencies).
- Merged interface tactile feel principles (typography stability, hit targets, concentric border radius, layered shadows) from `make-interfaces-feel-better` into `skills/emil-design-eng/references/interface-feel.md`.
- Merged practical WCAG AA checklist (accessible names, focus rings, dialog focus trapping, `aria-invalid`) from `fixing-accessibility` into `skills/impeccable/reference/accessibility.md` and wired into audit and critique workflows.
- Refreshed `skills/playwright-qa` with Playwright CLI diagnostics (`find`, `highlight`, `tracing-start`/`tracing-stop`, `console`) while maintaining strict 4-door browser hierarchy and <=200 line budget.
- Documented `react-doctor` as an optional on-demand tool for React audits in `skills/impeccable/reference/audit.md` and `skills/full-performance-audit/SKILL.md` (no network required at install, zero skill catalog bloat).
- Updated `docs/source-wave.md` with explicit MERGE and OPTIONAL dispositions.
- Hardened done-gate verification pattern across `rules/01-verification.md`, `rules/decision-log-protocol.md`, `manual-skills/decision-log/SKILL.md`, and `templates/AGENTS.md`. Mechanical completion now explicitly requires an evidence ledger (commands, exit codes, artifact paths) with mandatory pointers for done claims and strict separation of blocking `FACT:` proofs from advisory `JUDGMENT:` assessments.
- Fixed Design Bank config resolution path drift in `found-this-design` (`lib.mjs` and `banks.md` now read `~/.config/opencode/highend/config/design-bank.json` and share cache instead of legacy `bestfriend` paths and personal machine folders).
- Aligned documentation across `docs/design-bank.md`, `docs/troubleshooting.md`, and `docs/architecture.md` clarifying the distinction between the 12-bank discovery footprint and 4-catalog bootstrap requirements.
- Formalized specialist architecture as an artifact-gated directed graph and codified harness engineering principles across `rules/00-routing.md` and `docs/architecture.md`.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.2.

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
