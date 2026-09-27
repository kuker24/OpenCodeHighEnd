# Catalog Freeze Contract

This contract defines the immutable boundary and governance for the OpenCodeHighEnd catalog. The 65-skill catalog is strictly frozen.

- **Product version**: 0.1.7
- **Catalog**: 65 names. 50 model-invoked under `skills/`. 15 manual under `manual-skills/` + `commands/`.
- **Wave 0.1.7 unfreeze exception** (CHANGELOG 0.1.7): catalog grew 62 → 65 to add `json-render`, `deck-design`, `pageindex`. No twin retired. UI doctrines remain MERGE’d. `react-doctor` stays OPTIONAL_TOOL.
- **Retired in prior waves and not to be revived**: `ask-matt`, `grilling`, `wait-what`, `matt-implement`.
- **Kept on purpose**: `wizard` (target-app bash wizard), `codebase-design` (new module), `/improve-codebase-architecture` (scan + HTML report).
- **Name collision remains**: `install-anti-slop` = Oxlint; UI/copy filter lives in `impeccable` taste-gate + `humanizer`; `/unslop` = `humanizer`.
- **FOREIGN_ON_DEMAND stays out of the overlay**: `ECC`, `noodle`, `serena`, `stitch`, `reticle`, `ui-skills` MCP, `markitdown` MCP, `crawl4ai` MCP, `exa`, `Caliper`, `SkillEvaluator`, PageIndex Cloud MCP. `doctor` must not fail when they are absent.
- **No new allowlist name without retiring one existing name in the same change**, except a human-written CHANGELOG exception (the 0.1.7 growth is that exception; it is spent).
- **No padding back to 64.**
- **No `/how`, `/poteto-mode`, `/antislop`, `taste-skill`, `axi-core`, `human-atlas`, `awesome-design-md` vendor.**
- **No auto-edit of skills/rules from a learning log. No silent `--auto`.**
- **Next unfreeze requires a human-written exception in CHANGELOG that names the retired twin, or a new explicit growth exception.**
