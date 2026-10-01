# Skills

Policy: `vendor/skill-policy.json` plus `vendor/skill-allowlist.txt`.

- 50 model-invoked skills live under `skills/` and install to `~/.config/opencode/skills/` (core + Wave 2/3 warehouse specialists + 0.1.7 `json-render`, `deck-design`, `pageindex` + 0.1.8 `business-motion-film`, `ninerouter`)
- 15 manual skills live under `manual-skills/` and install to `~/.config/opencode/highend/skills/` plus `commands/`

`smartdoc` is per-job document intelligence. `deck-design` owns consulting PPTX / 16:9 HTML slide decks. `pageindex` owns tree/reasoning navigation of long structured documents. `json-render` owns schema/JSON generative UI after tokens/direction (or internal schema UI). `markitdown` converts Office/PDF/HTML/CSV/XLSX/PPTX/EPUB/ZIP to Markdown for ingest; SmartDoc keeps contract/QA/render. `smartbook-ingest` compiles reusable local knowledge. `humanizer` cleans user-facing prose tells (`/unslop` is its manual alias). `academic` manages scholarly research, writing, and peer review. `hyperframes` handles deterministic HTML-to-MP4 video composition. `id-demo-video` coordinates Indonesian application demo video production (`/demo-video` is its manual slash command). `diagram-design` crafts editorial HTML/SVG diagrams. `business-motion-film` plans and quality-checks commercial launch films, real app UI product promos, and explainers (rendered via hyperframes; absorbs Three.js product-hero patterns). `ninerouter` routes models, images, video, speech, and web tools through a 9Router gateway. Warehouse diagnostics include `agent-architecture-audit` (agent stack layers), `cost-aware-llm-pipeline` (token budgeting), `eval-harness` (benchmarks), and `skill-stocktake` (catalog hygiene; `prompt-optimizer` retired in 0.1.8 with prompt refinement handled by humanizer, research, and writing-for-agents). Wave 3 adds `api-design`, `contract-first`, `automation-audit-ops`, `code-tour`, and `click-path-audit`. Handwriting is a SmartDoc renderer, not a skill.

OpenCode 2 discovers `~/.config/opencode/skills` and project `.opencode/skills`. Manual skills must not be copied into those directories; they live under `~/.config/opencode/highend/skills/` and are invoked only as `~/.config/opencode/commands/<name>.md` (or project `.opencode/commands/<name>.md`).

`opencode-he skills verify` checks counts, missing files, and duplicates.
