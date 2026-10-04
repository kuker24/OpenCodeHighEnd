# MCP

OpenCode 2 schema: `mcp.servers.<name>` with required `type` (`local` or `remote`) and `disabled`. V1 `mcp.<name>` / `enabled` is not written. OpenCode 1.x fails closed.

Owned:

| Name | Type | Pin |
| --- | --- | --- |
| codebase-memory-mcp | local stdio | 0.11.0 SHA-256 verified |
| context7 | remote HTTP | https://mcp.context7.com/mcp |
| shadcn | local stdio | `npx -y shadcn@4.21.1 mcp` |

Codebase indexing uses two adapters: CLI `opencode-he cbm status` and `opencode-he cbm index [path]` (runs `index_repository --mode fast` after path check), or MCP `index_repository` (`mode: full` for semantic graph). Rebuilding the index does not require reinstalling.

Optional:

- `serena` — `opencode-he serena enable` if the binary is on PATH
- `stitch` — `opencode-he stitch enable` (remote comp/mock source only; auth via `{env:STITCH_API_KEY}` or `--oauth`)
- `reticle` — `opencode-he reticle enable` (local stdio via `npx -y @reticlehq/server@3.5.0 mcp`; perception only, never auto-implementer)
- `ui-skills` — `opencode-he ui-skills enable` (remote HTTP `https://www.ui-skills.com/mcp`; design-skill lookup only)
- `markitdown` — `opencode-he markitdown enable` (local stdio via `uvx --from markitdown-mcp==0.0.1a7 --with markitdown[all]==0.1.8 markitdown-mcp`; Markdown ingest only)
- `crawl4ai` — `opencode-he crawl4ai enable` (remote HTTP `http://127.0.0.1:11235/mcp/sse`; cloud via `--cloud` with `{env:CRAWL4AI_KEY}`)
- `scrapling` — `opencode-he scrapling enable` (local stdio via `uvx --from scrapling[ai]==0.4.15 scrapling mcp`; structured web scraping)
- `exa` — foreign; never add/remove/overwrite

Merge is parse-aware. Comment-free JSON is rewritten with `json.dumps`. JSONC with comments is patched surgically (owned MCP keys only). If surgical merge cannot be verified, install fails closed instead of destroying comments.

Doctor reports `CONFIGURED` for owned MCP entries present in config. That is not a live connection. `opencode-he doctor --deep` probes `opencode mcp list` per server/per line and **exits 1** unless every core server is `CONNECTED`. `DISCONNECTED`, `NOT_CHECKED`, `LISTED`, empty output, and command failure are not healthy. The substring `connected` inside `disconnected` is not treated as connected. ANSI codes are stripped before parse.

`opencode-he serena enable` adds Serena only if absent. JSONC comments, provider keys, and foreign MCP are preserved via the same surgical merge as core MCP. Invalid config fails closed.

`opencode-he stitch enable` configures Google Stitch as an optional remote comp/mock server (`https://stitch.googleapis.com/mcp`). It is not an owned core server and not a UI implementer. Keys are never written directly to config, only referenced via `{env:STITCH_API_KEY}` or omitted when using `--oauth`. `opencode-he stitch disable` surgically removes only the stitch server key.

`opencode-he reticle enable` configures Reticle as an optional local perception MCP server (`npx -y @reticlehq/server@3.5.0 mcp`). It is `FOREIGN_ON_DEMAND`. The server package is FSL-1.1-ALv2 (competing-use clause); SDK packages (Apache-2.0) are not vendored. Reticle is never an auto-implementer; after a feature is done, default verification remains `playwright-qa` or `chrome-devtools-axi`. Reticle is extra perception if the user enabled it. `opencode-he reticle disable` surgically removes only the reticle server key. Absent is not a doctor failure; a malformed entry fails closed.

`opencode-he ui-skills enable` configures UI Skills as an optional remote MCP server (`https://www.ui-skills.com/mcp`). It is `FOREIGN_ON_DEMAND` for design-skill lookup only (`list_skills`, `get_skill`). Product UI remains Design Bank + Impeccable + Design V2 atoms + shadcn; `BANK_MISS` never generates from a random ui-skills document. `opencode-he ui-skills disable` surgically removes only the ui-skills server key. Absent is not a doctor failure; a malformed entry fails closed.

`opencode-he markitdown enable` configures MarkItDown as an optional local stdio ingest MCP (`uvx --from markitdown-mcp==0.0.1a7 --with markitdown[all]==0.1.8 markitdown-mcp`). It is `FOREIGN_ON_DEMAND`. Official server is for local trusted agents only; never `--http`, never bind `0.0.0.0`, never docker bind-all. Bare `markitdown-mcp` emits `WARN MARKITDOWN_UNPINNED`. The converter is not vendored into `lib/`. Missing `uvx` is documented in the skill (CLI/`pipx`/`enable`); enable still writes the stdio command like reticle. `opencode-he markitdown disable` surgically removes only the markitdown server key. Absent is not a doctor failure; a malformed entry (including `--http` / `0.0.0.0`) fails closed.

`opencode-he crawl4ai enable` configures Crawl4AI as an optional web content extraction remote MCP (`http://127.0.0.1:11235/mcp/sse`). It is `FOREIGN_ON_DEMAND` for content extraction, not exploratory browser QA (which remains `playwright-qa`). Legacy `/mcp` emits `WARN CRAWL4AI_LEGACY_URL`. For Docker users, bind strictly to `127.0.0.1:11235` (e.g. `docker run -p 127.0.0.1:11235:11235 ...`); never bind `0.0.0.0`. OpenCodeHighEnd does not launch or manage the container. With `--cloud`, it configures `https://api.crawl4ai.com/mcp` using `{env:CRAWL4AI_KEY}` without writing secrets to disk. `opencode-he crawl4ai disable` surgically removes only the crawl4ai server key. Absent is not a doctor failure; binding to `0.0.0.0` or invalid URLs fails closed.

`opencode-he scrapling enable` configures Scrapling as an optional local stdio MCP (`uvx --from scrapling[ai]==0.4.15 scrapling mcp`). It is `FOREIGN_ON_DEMAND` for structured web scraping and element extraction, not exploratory browser QA (which remains `playwright-qa`). Local stdio only: never `--http`, never bind `0.0.0.0`, never docker bind-all. Do not run `scrapling install` as it invokes `playwright install-deps` with sudo. The scraper is not vendored into `lib/`. `opencode-he scrapling disable` surgically removes only the scrapling server key. Absent is not a doctor failure; a malformed entry (including `--http` / `0.0.0.0`) fails closed.

## Evaluated, Skipped & Rejected

- **Scrapling (`D4Vinci/Scrapling`)** — Promoted to `FOREIGN_ON_DEMAND` optional local stdio MCP in Wave 0.1.11 via `opencode-he scrapling enable` (pinned `0.4.15`). Not a core MCP; not vendored. Stdio only; `--http` and `0.0.0.0` forbidden. Never run `scrapling install`.
- **TypeSafe Jev (`jev-mcp`)** — TypeSafe Jev / `jkudish/jev-mcp` was evaluated and is intentionally **SKIPPED** as a required runtime MCP. It is not vendored and not bundled in core MCPs. If ever manually configured by a user, it remains optional `FOREIGN_ON_DEMAND` only with `{env:TYPESAFE_API_KEY}`. Core verification, done-gates, and evidence ledgers operate fully offline without external Jev services.
- **Agent-Reach (`Panniantong/Agent-Reach`)** — Evaluated and designated `POINTER_ONLY` host CLI under `research` (`references/web-data.md`) in Wave 0.1.11. Strictly **REJECTED** as a core MCP, optional MCP, or skill. Never run `agent-reach install --system` (mutates system packages and copies foreign skills into `~/.config/opencode/skills/`). Doctor detects foreign skill shadowing and warns.
- **Patchright-Enhanced (`whaleyxbt/patchright-enhanced`)** — Evaluated and strictly **REJECTED**. Unofficial fork; carries security, maintenance, and upstream divergence risks. Do not vendor, install, or reference.
- **TypeSafe MCP (`itsmostafa/typesafe-mcp`)** — Evaluated and **REJECTED** as an extra core MCP. Core MCPs remain strictly `codebase-memory-mcp`, `context7`, and `shadcn`.
- **Graphiti (`getzep/graphiti`) & Cognee (`topoteretes/cognee`)** — Evaluated and **REJECTED** as external memory MCP servers. Complex graph databases and temporal entity graph memory requiring separate backends/services are out of scope. Codebase indexing and symbol memory is strictly owned by `codebase-memory-mcp` (v0.11.0). Core MCPs remain strictly `codebase-memory-mcp`, `context7`, and `shadcn`.
- **PageIndex Cloud MCP (`VectifyAI/PageIndex`)** — Skill `pageindex` is a first-party wrapper for tree/reasoning long-doc navigation. The Cloud/hosted MCP is **REJECTED** as an extra core MCP. Do not register it. Missing local SDK is `NOT_CONFIGURED` on the skill, not a doctor failure.
- **9Router Gateway (`decolua/9router`)** — 9Router is a `FOREIGN_ON_DEMAND` gateway, NOT a core MCP server. Core MCP servers remain strictly `codebase-memory-mcp` (0.11.0), `context7`, and `shadcn` (@4.21.1). First-party gateway stub lives in `skills/ninerouter/SKILL.md` connecting via `{env:NINEROUTER_URL}` (default `http://127.0.0.1:20128`). Upstream capability skills are fetched on demand and not vendored. Absence of a running gateway reports `NOT_CONFIGURED` on the skill, never an installer or `doctor` failure. Never bind to `0.0.0.0`.
