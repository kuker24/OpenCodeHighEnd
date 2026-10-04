# OpenCodeHighEnd third-party notices

Adapted from ClaudeBestFriend / GrokBestFriend. Adapted ≠ first-party. This OpenCode port does not include Context Guard, Claude hooks, or Claude runtime config.

First-party installer, docs, overlays, and tests are MIT (see `LICENSE`).

This product vendors OpenCode-adapted skills and Design Intelligence runtime, originally snapshotted through GrokBestFriend 1.3.1 and ClaudeBestFriend 1.4.2-claude.1 (`05e6fdc`).

Selected skills also come from [mattpocock/skills](https://github.com/mattpocock/skills) (`d81f3a1`, v1.2.3+ (d81f3a1), MIT © 2026 Matt Pocock) and [cursor/plugins](https://github.com/cursor/plugins) `pstack/` (`e43c7ee`, pstack 0.15.9, MIT © 2026 Lauren Tan). Full plugins are not installed.

Licenses below are taken from vendored frontmatter or an obvious upstream statement. If a skill has no license in tree, this file says so. **That is not a grant.**

Machine-readable copy: `vendor/license-audit.json`.

| Component | Upstream | License in this tree | Redistribution |
| --- | --- | --- | --- |
| `adhd` | vendored frontmatter | MIT | follow MIT |
| `impeccable` | vendored frontmatter | Apache-2.0 | follow Apache-2.0 |
| Matt Pocock selected skills (`diagnosing-bugs`, `domain-modeling`, `codebase-design`, `writing-for-agents`, `research`, `prototype`, `improve-codebase-architecture`, `wizard`, `grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `matt-code-review` ← `code-review`) | mattpocock/skills `d81f3a1` MIT LICENSE — `vendor/licenses/MATT-POCOCK-MIT.txt` | MIT | follow MIT |
| Pstack selected skills (`blast-radius`, `unslop`, `create-verification-skill`, `maintain-verification-skill`, `technical-writing`, `arena`, `interrogate`, `architect`, `decision-log`, `why`, `reflect`, `figure-it-out`) | cursor/plugins pstack `e43c7ee` (0.15.9; `/correct` at `9511e60` merged into `manual-skills/reflect/references/correct.md`) | MIT — `vendor/licenses/PSTACK-MIT.txt` | follow MIT |
| Snapshot skills (`browser-act`, `chrome-devtools-axi`, `emil-design-eng`, `found-this-design`, `full-audit-keamanan`, `full-performance-audit`, `gh-axi`, `scroll-world`, `visual-studio`) | GrokBestFriend 1.3.1 snapshot + `vendor/licenses/GROKBESTFRIEND-MIT.txt`; skill wrappers MIT. Separate CLIs follow their own packages. | MIT | follow MIT |
| `scroll-world` | [oso95/scroll-world](https://github.com/oso95/scroll-world) `71cc36d` + GrokBestFriend snapshot; seam QA calibration note merged | MIT © 2026 cyw | follow MIT |
| `scroll-craft` | [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) `0b81622` — `vendor/licenses/NATEHERK-SCROLL-CRAFT-MIT.txt`; skill `NOTICE.md` | MIT © 2026 Nate Herk | follow MIT |
| `playwright-qa` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) `655530f` — `vendor/licenses/MICROSOFT-PLAYWRIGHT-CLI-APACHE2.txt`; skill `NOTICE.md` | Apache-2.0 © Microsoft Corporation | follow Apache-2.0 |
| `taste-guard` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) `ccbc156` — `vendor/licenses/LEONXLNX-TASTE-MIT.txt`; integrated in Impeccable | MIT © 2026 Leonxlnx | follow MIT |
| `install-anti-slop` | [dmmulroy/anti-slop](https://github.com/dmmulroy/anti-slop) `e8c4880` — `vendor/licenses/DMMULROY-ANTI-SLOP-MIT.txt`; skill `NOTICE.md` (updated with `update` mode) | MIT © 2026 Dillon Mulroy | follow MIT |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) 3.1.0 (`225a6f3`); skill `NOTICE.md` | MIT © 2024-2026 blader contributors | follow MIT |
| `academic` | Original first-party text. Conceptual pipeline (research→write→review→revise) independently implemented. No source copied from Imbad0202/academic-research-skills (CC-BY-NC-4.0). | MIT © 2026 OpenCodeHighEnd contributors | follow MIT |
| `hyperframes` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) v0.8.119 (`3a0299e`), refreshed in 0.1.13 to v0.8.122 (`6037d22`); skill `NOTICE.md` | Apache-2.0 | follow Apache-2.0 |
| `json-render` | [vercel-labs/json-render](https://github.com/vercel-labs/json-render) `c2600d73`; skill `NOTICE.md`. npm packages not vendored. | Apache-2.0 © 2025 Vercel Inc. | follow Apache-2.0 |
| `deck-design` | [carnot-tech/consulting-pptx-skill](https://github.com/carnot-tech/consulting-pptx-skill) `f50edac`; skill `NOTICE.md`. 62-type packs not vendored. | MIT © carnot-tech contributors | follow MIT |
| `pageindex` | [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) `037a7dba` (v0.2.21); skill `NOTICE.md`. SDK/Cloud not vendored. | MIT © 2026 PageIndex AI / VectifyAI | follow MIT |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design); skill `NOTICE.md` | MIT © 2024-2026 Cathryn Lavery contributors | follow MIT |
| Email design doctrine | Merged from [CosmoBlk/email-design](https://github.com/CosmoBlk/email-design) (MIT © 2026 CosmoBlk), [jayesh-bansal/email-pro-max](https://github.com/jayesh-bansal/email-pro-max) (MIT © 2026 Jayesh Bansal), [chunkydotdev/email-skills](https://github.com/chunkydotdev/email-skills) (MIT © 2026 chunkydotdev), and [Olshansk/agent-skills](https://github.com/Olshansk/agent-skills) (MIT © 2026 Olshansk) into `skills/impeccable/reference/email.md` | MIT | follow MIT |
| Emil Kowalski motion & design doctrines | Merged from [emilkowalski/skills](https://github.com/emilkowalski/skills) (`e8a175de22ae`) into `skills/emil-design-eng/references/` (`motion.md`, `apple-principles.md`, `native-motion.md`, `interface-feel.md`) and `skills/impeccable/reference/break-ui.md` (adversarial UI stress testing). Text: `vendor/licenses/EMILKOWALSKI-MIT.txt` | MIT © 2026 Emil Kowalski | follow MIT |
| Warehouse Batch 2a (`agent-architecture-audit`, `cost-aware-llm-pipeline`, `eval-harness`, `skill-stocktake`) | Adapted from [affaan-m/ECC](https://github.com/affaan-m/ECC); respective skill `NOTICE.md` files (prompt-optimizer retired in 0.1.8) | MIT © 2024-2026 affaan-m and ECC contributors | follow MIT |
| `business-motion-film` | [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) `255562b` — `vendor/licenses/ECHRIS6-MOTION-VIDEO-KIT-MIT.txt`; [kaventro/motion-designer](https://github.com/kaventro/motion-designer) `7d0b8bb` (v1.2.0, product-film mode with phone review, motion blur, and scored review) — `vendor/licenses/KAVENTRO-MOTION-DESIGNER-MIT.txt`; skill `NOTICE.md` | MIT © 2026 echris6; MIT © 2026 kaventro | follow MIT |
| `ninerouter` | [decolua/9router](https://github.com/decolua/9router) `a99cf57` (v0.5.95; `f01fb90` base); skill `NOTICE.md`. First-party gateway stub; skills on-demand. | MIT © 2026 decolua | follow MIT |
| Warehouse Batch 3a (`api-design`, `automation-audit-ops`, `click-path-audit`, `code-tour`, `contract-first`) | Adapted from [affaan-m/ECC](https://github.com/affaan-m/ECC); respective skill `NOTICE.md` files | MIT © 2024-2026 affaan-m and ECC contributors | follow MIT |
| Design bank media | User-provided public bootstrap artifact or existing local bank | **not cleared** | not in git; normal install does not download it |
| Codebase Memory, serena, browser-act CLI, Scrapling, Agent-Reach CLI, semgrep, gitleaks, osv-scanner | `vendor/sources.json` | upstream; not vendored | follow upstream |

See `vendor/provenance.json` and `vendor/sources.json` for pins.
