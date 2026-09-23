# Changelog

## Unreleased

- Upgraded `codebase-memory-mcp` pin to v0.11.0 with SHA-256 verified portable tarball download, and added automatic `--format json` argument propagation in `lib/cbm.py` for reliable JSON extraction across project listing and status commands.
- Bumped `shadcn` CLI MCP pin to `4.21.0` across `vendor/mcp-wanted.json`, `vendor/mcp-policy.json`, `lib/install.py`, `rules/00-routing.md`, and doctor tests.
- Refreshed `impeccable` craft floor mechanics in `skills/impeccable/reference/craft-floor.md` from upstream `skill-v4.3.1` / main (tracking caps at -0.04em, single elevation declarations via border or shadow, banning amateur sketch imitation in SVG while preserving geometric linework, subject-world textures, and truth-grounded claims).
- Created `skills/impeccable/reference/email.md` synthesizing email design intelligence and bulletproof rendering (CosmoBlk, email-pro-max, email-skills, agent-skills): 6 committed archetypes (Editorial, Bold-mono, Minimal-lux, Founder letter, Punk/Character, Lookbook), strict presentation tables (or React Email/MJML framework components), inline CSS, 6-digit hex colors, bulletproof table-cell CTA buttons, preheader anti-spill ZWNJ padding, dark mode resilience, and <100KB deliverability constraints.
- Wired email design routing into `skills/impeccable/SKILL.md`, `skills/impeccable/reference/routing.md`, and `skills/impeccable/reference/ui-hub.md` to guarantee web component libraries are never mistakenly installed into email templates.
- Consolidated Emil Kowalski motion doctrines into `skills/emil-design-eng/references/`: created `motion.md` (decision framework, compositor-only properties, production recipes, exit choreography), `apple-principles.md` (WWDC 2018 fluid interfaces, physics-based springs, velocity handoff, momentum projection, materials, SF Pro optical sizing), and `native-motion.md` (eliminating mobile web browser tells, 100dvh, safe area insets, touch-action, overscroll containment, and Expo / React Native Reanimated 3 worklets). Maintained zero new skill names, preserving catalog freeze at 62.
- Refreshed upstream pins in `vendor/sources.json` for `pbakaus/impeccable` (tag `skill-v4.3.1` `cd12f8660e2d` / verified main `e0881d2de397`), `emilkowalski/skills` (`85e8e2363b71`), `microsoft/markitdown` (v0.1.8 `b8f79c57`, PIN_ONLY), and `kunchenguid/axi` (`85a8723276ca`, PIN_ONLY).
- Updated `docs/source-wave.md`, `docs/mcp.md`, `README.md`, and `THIRD_PARTY_NOTICES.md` with complete attribution and license notices for merged doctrines.
- Recorded `CODEBASE_MEMORY_BINARY_CHECKSUM_FAILED` in `docs/troubleshooting.md` (delete download cache and `components/codebase-memory`, then reinstall; v0.11 index rebuilds once). Vendored `vendor/licenses/IMPECCABLE-APACHE2.txt` and `vendor/licenses/EMILKOWALSKI-MIT.txt` so `licenseFile` pins are not empty pointers. `scroll-world` and `browser-act` stay **UPDATE** (not body-refreshed in this wave). markitdown `uvx` invocation stays unpinned (`PIN_ONLY` follow-up).

## 0.1.3 — 2026-09-23

- Codified the 20-member closed intent classification set in `rules/00-routing.md`, `docs/routing.md`, and `templates/AGENTS.md` (`repo_understand | bug | security | perf | ui_direction | ui_implement | motion | scroll_2d | scroll_3d | img3d | docs | ingest_md | prose | academic | browser_qa | architecture | warehouse | ops_data | video_html | demo_id`).
- Codified artifact-gated specialist handoff graph in `rules/00-routing.md`, `docs/routing.md`, and `docs/architecture.md`, enforcing `found-this-design` must emit `.impeccable/found-this-design.json` before `impeccable` starts.
- Enforced OpenCode 2 host and Code Mode tooling guardrails: session operations strictly use `tools.opencode.session_move` and `tools.opencode.session_rename` (never foreign namespaces); Codebase Memory MCP strictly targets verified repository paths.
- Absorbed offline typed-gate verification patterns (Jev/Canny MERGE) across `rules/01-verification.md` and `rules/decision-log-protocol.md`: assertions in tickets/PRs are hypotheses requiring `FACT:` rows, missing facts halt progress to ask user, and auto-progression requires low blast radius and mechanical proof.
- Merged anti-generic frontend design principles from `anthropics/frontend-design` into `skills/impeccable/reference/taste-guard.md` (no default warm cream ground kit, no terracotta cards, token system before build, domain-grounded typography).
- Merged keyboard navigation flows and reduced-motion fallbacks from `addyosmani/accessibility` into `skills/impeccable/reference/accessibility.md`.
- Merged Apple-grade tactile motion, velocity inheritance, and interruptible springs from `emilkowalski/apple-design` and `wshobson/interaction-design`, along with layered ambient shadows and container-adaptive layouts into `skills/emil-design-eng/references/interface-feel.md`.
- Updated `docs/source-wave.md` with explicit dispositions for upstream wave sources (Canny, Jev demos, typesafe-mcp, Agent-Reach, etc.).
- Explicitly documented `Agent-Reach` and `typesafe-mcp` as REJECTED in `docs/mcp.md` and `docs/source-wave.md`, keeping core MCP servers frozen at `codebase-memory-mcp`, `context7`, and `shadcn`.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.3.

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
