# MCP

OpenCode 2 schema: `mcp.servers.<name>` with required `type` (`local` or `remote`) and `disabled`. V1 `mcp.<name>` / `enabled` is not written. OpenCode 1.x fails closed.

Owned:

| Name | Type | Pin |
| --- | --- | --- |
| codebase-memory-mcp | local stdio | 0.9.0 SHA-256 verified |
| context7 | remote HTTP | https://mcp.context7.com/mcp |
| shadcn | local stdio | `npx -y shadcn@4.18.0 mcp` |

Optional:

- `serena` — `opencode-he serena enable` if the binary is on PATH
- `stitch` — `opencode-he stitch enable` (remote comp/mock source only; auth via `{env:STITCH_API_KEY}` or `--oauth`)
- `reticle` — `opencode-he reticle enable` (local stdio via `npx -y @reticlehq/server mcp`; perception only, never auto-implementer)
- `ui-skills` — `opencode-he ui-skills enable` (remote HTTP `https://www.ui-skills.com/mcp`; design-skill lookup only)
- `markitdown` — `opencode-he markitdown enable` (local stdio via `uvx --from markitdown-mcp markitdown-mcp`; Markdown ingest only)
- `exa` — foreign; never add/remove/overwrite

Merge is parse-aware. Comment-free JSON is rewritten with `json.dumps`. JSONC with comments is patched surgically (owned MCP keys only). If surgical merge cannot be verified, install fails closed instead of destroying comments.

Doctor reports `CONFIGURED` for owned MCP entries present in config. That is not a live connection. `opencode-he doctor --deep` probes `opencode mcp list` per server/per line and **exits 1** unless every core server is `CONNECTED`. `DISCONNECTED`, `NOT_CHECKED`, `LISTED`, empty output, and command failure are not healthy. The substring `connected` inside `disconnected` is not treated as connected. ANSI codes are stripped before parse.

`opencode-he serena enable` adds Serena only if absent. JSONC comments, provider keys, and foreign MCP are preserved via the same surgical merge as core MCP. Invalid config fails closed.

`opencode-he stitch enable` configures Google Stitch as an optional remote comp/mock server (`https://stitch.googleapis.com/mcp`). It is not an owned core server and not a UI implementer. Keys are never written directly to config, only referenced via `{env:STITCH_API_KEY}` or omitted when using `--oauth`. `opencode-he stitch disable` surgically removes only the stitch server key.

`opencode-he reticle enable` configures Reticle as an optional local perception MCP server (`npx -y @reticlehq/server mcp`). It is `FOREIGN_ON_DEMAND`. The server package is FSL-1.1-ALv2 (competing-use clause); SDK packages (Apache-2.0) are not vendored. Reticle is never an auto-implementer; after a feature is done, default verification remains `playwright-qa` or `chrome-devtools-axi`. Reticle is extra perception if the user enabled it. `opencode-he reticle disable` surgically removes only the reticle server key. Absent is not a doctor failure; a malformed entry fails closed.

`opencode-he ui-skills enable` configures UI Skills as an optional remote MCP server (`https://www.ui-skills.com/mcp`). It is `FOREIGN_ON_DEMAND` for design-skill lookup only (`list_skills`, `get_skill`). Product UI remains Design Bank + Impeccable + Design V2 atoms + shadcn; `BANK_MISS` never generates from a random ui-skills document. `opencode-he ui-skills disable` surgically removes only the ui-skills server key. Absent is not a doctor failure; a malformed entry fails closed.

`opencode-he markitdown enable` configures MarkItDown as an optional local stdio ingest MCP (`uvx --from markitdown-mcp markitdown-mcp`). It is `FOREIGN_ON_DEMAND`. Official server is for local trusted agents only; never `--http`, never bind `0.0.0.0`, never docker bind-all. The converter is not vendored into `lib/`. Missing `uvx` is documented in the skill (CLI/`pipx`/`enable`); enable still writes the stdio command like reticle. `opencode-he markitdown disable` surgically removes only the markitdown server key. Absent is not a doctor failure; a malformed entry (including `--http` / `0.0.0.0`) fails closed.

## Evaluated, Skipped & Rejected

- **TypeSafe Jev (`jev-mcp`)** — TypeSafe Jev / `jkudish/jev-mcp` was evaluated and is intentionally **SKIPPED** as a required runtime MCP. It is not vendored and not bundled in core MCPs. If ever manually configured by a user, it remains optional `FOREIGN_ON_DEMAND` only with `{env:TYPESAFE_API_KEY}`. Core verification, done-gates, and evidence ledgers operate fully offline without external Jev services.
- **Agent-Reach (`Panniantong/Agent-Reach`)** — Agent-Reach was evaluated and is strictly **REJECTED** as a core MCP or skill. It is not an alternative to Playwright QA eyes, carries ToS/cookie/account risks, and relies on Exa which is already designated `FOREIGN_ON_DEMAND`. Never register Agent-Reach as a core or required tool.
- **TypeSafe MCP (`itsmostafa/typesafe-mcp`)** — Evaluated and **REJECTED** as an extra core MCP. Core MCPs remain strictly `codebase-memory-mcp`, `context7`, and `shadcn`.
