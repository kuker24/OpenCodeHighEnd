# Catalog Freeze Contract

This contract defines the immutable boundary and governance for the OpenCodeHighEnd catalog. The 65-skill catalog is strictly frozen.

- **Product version**: 0.1.12
- **Catalog**: 65 names. 50 model-invoked under `skills/`. 15 manual under `manual-skills/` + `commands/`.
- **Wave 0.1.12 body-only**: catalog strictly frozen at 65 (50 model + 15 manual). Zero catalog growth. No new exceptions. Upstream hyperframes refreshed to v0.8.119 (declarative data attributes, CLI render pipeline); awesome-opus5-5-videos added as first-party POINTER_ONLY prompt patterns reference; Matt Pocock cluster migrated to GLOSSARY.md convention with legacy CONTEXT.md fallback; dead game-asset-core references removed; humanizer bumped to v3.1.0 with patterns 25 & 26; diagram-design pinned to 2.6.51; impeccable v4.5.0 deferred.
- **Wave 0.1.11 body-only**: catalog strictly frozen at 65 (50 model + 15 manual). Zero catalog growth. No new exceptions. Adds closed intent `web_research` mapped to existing skill `research` (body-only update + `references/web-data.md`). Scrapling added as optional MCP `FOREIGN_ON_DEMAND`. Agent-Reach documented as `POINTER_ONLY` host CLI. Patchright-Enhanced strictly rejected.
- **Wave 0.1.10**: catalog stays frozen at 65. No new exception. `found-this-design` indexes Oversight Supply; Design Bank bootstrap pin is DesignBank v3. pstack selected-skill provenance moves to `23e4138`; owned skill bodies are host adaptations, not an upstream body copy. `poteto-mode` stays rejected.
- **Wave 0.1.9 body-only**: catalog strictly frozen at 65 (50 model + 15 manual). Zero catalog growth. No new exceptions; 0.1.8 exception is spent. Upstream `kaventro/motion-designer` merged into `business-motion-film` (product-film mode).
- **Wave 0.1.8 limited unfreeze exception** (CHANGELOG 0.1.8): catalog stays 65 (50 model + 15 manual). Retired names: `img2threejs` (Three.js product-hero patterns moved to `business-motion-film` references), `prompt-optimizer` (overlaps `research` + `humanizer`). Added model-invoked: `business-motion-film` (from `echris6/motion-video-kit`, MIT), `ninerouter` (first-party gateway stub). Intent `img3d` replaced by `launch_film | gateway_llm`. This exception is spent.
- **Wave 0.1.7 unfreeze exception** (CHANGELOG 0.1.7): catalog grew 62 → 65 to add `json-render`, `deck-design`, `pageindex`. No twin retired. (Spent).
- **Retired in prior waves and not to be revived**: `ask-matt`, `grilling`, `wait-what`, `matt-implement`.
- **Kept on purpose**: `wizard` (target-app bash wizard), `codebase-design` (new module), `/improve-codebase-architecture` (scan + HTML report).
- **Name collision remains**: `install-anti-slop` = Oxlint; UI/copy filter lives in `impeccable` taste-gate + `humanizer`; `/unslop` = `humanizer`.
- **FOREIGN_ON_DEMAND stays out of the overlay**: `ECC`, `noodle`, `serena`, `stitch`, `reticle`, `ui-skills` MCP, `markitdown` MCP, `crawl4ai` MCP, `scrapling` MCP, `exa`, `Caliper`, `SkillEvaluator`, PageIndex Cloud MCP, `9router` capability skills. `doctor` must not fail when they are absent.
- **No new allowlist name without retiring one existing name in the same change**, except a human-written CHANGELOG exception (the 0.1.7 growth is that exception; it is spent).
- **No padding back to 64.**
- **No `/how`, `/poteto-mode`, `/antislop`, `taste-skill`, `axi-core`, `human-atlas`, `awesome-design-md` vendor.**
- **No auto-edit of skills/rules from a learning log. No silent `--auto`.**
- **Next unfreeze requires a human-written exception in CHANGELOG that names the retired twin, or a new explicit growth exception.**
