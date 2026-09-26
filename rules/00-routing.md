# OpenCode specialist routing (opencode-highend)

Read this file only when routing is non-obvious. Do not load every specialist.

Use tools lazily. Prefer current repository evidence before external tools. Use one primary specialist per problem. If a risk trigger is active (auth, authorization, secrets, public APIs, payment, upload, webhook, privileged operations), also load at most one verification specialist (`/full-audit-keamanan`). If the concern is a measured performance regression (LCP, INP, CLS, latency, bundle, query, memory), the verification specialist is `/full-performance-audit`. Do not load a second implementation specialist. Availability is not a reason to activate a tool. For mixed requests (e.g., landing + button + video), pick the primary largest surface (typically `/impeccable`); motion or video is step 2 after user pick, never a parallel load.

```text
pikir dulu → bukti di repo → satu spesialis → cek hasil
```

Do not infer a model provider from a logical model name. Treat custom-gateway aliases as opaque. Never print tokens, gateway URLs, or model-mapping values.

## Default path

1. **Repo evidence is enough** → do the work. No specialist. Verification: FAST or STANDARD.
2. **User typed a slash skill** → load that skill. Do not substitute.
3. **User is choosing a workflow** (`which skill`, `alur apa`) → read `~/.config/opencode/AGENTS.md` or this file. No specialist.
4. **Architecture / PR-plan DAG** → the OpenCode plan agent. After approval → implement in this session. There is no bundled `/design` or `/execute-plan`.
5. **Feature still needs a plan** (interview, glossary, ADR) → `/grill-with-docs` (includes frontier rounds). Then `/to-spec` → `/to-tickets` only if the user asked for tickets or the work is multi-session.
6. **Ordinary implementation** → write in this session. Use `/tdd` when test-first. Spec and `/to-tickets` implementations stay in this session with `/tdd`. There is no user `/implement` skill.
7. **Review** → in-session review. `/matt-code-review` only if the user asked for two-axis Standards + Spec. There is no user `/code-review` skill.
8. **Verification** → pick a profile, then Read `~/.config/opencode/highend/rules/01-verification.md`. Required configured failures block a completion claim.

## Closed Intent Classification

The router classifies every user task into exactly one closed intent:

```text
repo_understand | bug | security | perf | ui_direction | ui_implement
motion | scroll_2d | scroll_3d | img3d | docs | ingest_md | prose
academic | browser_qa | architecture | warehouse | ops_data | video_html | demo_id
```

| Intent | Primary Route | Handoff Boundary / Rule |
|---|---|---|
| `repo_understand` | Codebase Memory MCP → `code-tour` | Codebase Memory first; guided tour anchors `.tours/` |
| `architecture` | `/why` (manual); blast risk → `/blast-radius` | Rationale and blast radius; no auto-architect |
| `bug` | `diagnosing-bugs` | Reproduce red-green; known typos stay `/tdd` or in-session |
| `security` | `full-audit-keamanan` | Defensive code/auth/secrets audit (max 1 risk specialist) |
| `perf` | `full-performance-audit` | Measured LCP/INP/CLS/latency/bundle bottlenecks |
| `ui_direction` | `found-this-design` | Stop after writing `.impeccable/found-this-design.json` |
| `ui_implement` | `impeccable` | Requires pinned world or project `DESIGN.md` |
| `motion` | `emil-design-eng` | Micro-interactions, spring physics, touch feel |
| `scroll_2d` | `scroll-craft` | Scrollytelling, pinned 2D timelines, scroll triggers |
| `scroll_3d` | `scroll-world` | Continuous 3D fly-through, camera-scrub worlds |
| `img3d` | `img2threejs` | Procedural Three.js models from reference images |
| `docs` | `smartdoc` | Technical docs, OCR/PDF/DOCX extraction & contracts |
| `ingest_md` | `markitdown` | Structure-preserving Markdown ingest from Office/PDF |
| `prose` | `humanizer` / `/unslop` | Prose AI-tell removal; technical docs stay `technical-writing` |
| `academic` | `academic` | Literature surveys, IMRaD manuscripts, peer critique |
| `browser_qa` | `playwright-qa` → `browser-act` → `chrome-devtools-axi` → `click-path-audit` | 4-door hierarchy; isolated verification sessions |
| `video_html` | `hyperframes` | Programmatic HTML-to-MP4 via headless Chrome + FFmpeg |
| `demo_id` | `id-demo-video` (`/demo-video`) | Indonesian narrated app tour; cards via hyperframes |
| `warehouse` | Only when user names the job | `agent-architecture-audit`, `cost-aware-llm-pipeline`, etc. |
| `ops_data` | `supabase-ops` / `mongodb-ops` / `vercel-ops` | Operational data/hosting config; never generates UI |

## Tool Reporting

When reporting tool or specialist usage to the operator, strictly use:

```text
USED
CONSIDERED_NOT_USED
MANUAL_NOT_INVOKED
```

Never list unused tools or uncalled MCP methods as used.

## Jev-Shaped Verification Policy (Without External Server)

1. **Assertions ≠ Evidence**: Claims made in the user prompt, PR body, or issue tickets are hypotheses until backed by verifiable mechanical facts.
2. **Missing Facts Stop**: If a required priority, test command, or baseline constraint is missing or ambiguous, halt and stop with `ask_user` or targeted repo investigation before mutating code.
3. **Execution Bands**:
   - `auto`: Permitted ONLY when an objective, mechanical FACT exists (tests passing, compiler green, clean lint, exit 0) AND blast radius is low.
   - `review`: Required whenever mechanical proof is missing, tests are unconfigured, or changes touch auth, secrets, or payments.
4. **Hard Artifacts Overwrite Model Confidence**: Compiler errors, test suites, SHA-256 checks, traces, and screenshots strictly overrule model reasoning or confidence.

## Harness & Code Mode Tooling Rules

1. **Host Identity**: OpenCodeHighEnd runs on OpenCode 2. Never assume foreign host/gateway namespaces (e.g. `tools.antigravity.*`) in Code Mode execution scripts.
2. **Session Tools**: Session manipulation in Code Mode is strictly `tools.opencode.session_move` and `tools.opencode.session_rename`. Always call `search()` before executing unknown tool paths.
3. **Codebase Memory Path Verification**: Codebase Memory MCP operations (`index_repository`, `index_status`) strictly require verified, existing filesystem directory paths matching cwd or an explicit user path. Never guess or invent unverified sibling directory paths (e.g. `AntigravityHighEnd`). If an indexing worker reports an error or the path is missing, verify `cwd` or run `list_projects` first rather than retrying arbitrary paths.

## Knowledge

- Repository structure and impact: MCP `codebase-memory-mcp` first. If Codebase Memory has no project for cwd, skip it and use repo files. Do not retry.
- Exact cross-file symbol work: MCP `serena` only if already registered and only after Codebase Memory and simpler repo evidence are not enough. Do not run Serena and Codebase Memory as the main brain at the same time. If Serena is absent, say so; do not `opencode mcp add serena` from a session unless the user asked. Helper: `opencode-he serena enable`.
- Current library or framework docs: MCP `context7` only when repo evidence is insufficient.
- Installable React/shadcn registry items: MCP `shadcn` (pinned CLI `shadcn@4.21.0`). Search, inspect, then install. Context7 stays documentation.
- Broader web research: built-in `WebSearch` and `WebFetch`. MCP `exa` is foreign/pre-existing and ON_DEMAND. Use it only if already connected and research needs it. Never add or remove `exa`.
- Hard, high-impact, divergent decisions, fuzzy debugging, API or schema alternatives, trap detection: `/adhd` on demand only. Skip ADHD for typos, ordinary CRUD, or bugs with a known cause.
- Official library, spec, or first-party API facts: `/research` (Context7 when repo evidence is not enough). Why *this repo* chose an approach: suggest `/why` (manual). Do not mix the two.
- Scholarly literature surveys, academic manuscripts (IMRaD/thesis/proposal), and structured peer critique: `/academic` (not `research`, not `smartdoc` unless file extract/render).
- Fuzzy or conflicting domain terms, glossary, CONTEXT.md / ADR writing: `/domain-modeling`. Full product interviews that should leave CONTEXT.md/ADRs: `/grill-with-docs`.
- Module, interface, seam, testability, abstraction: `/codebase-design` (distinct from `/api-design` for REST and `/contract-first` for machine schemas). Multi-sketch bake-off: suggest `/architect` (manual). Do not auto-start `/architect`.
- Throwaway evidence for one design question: `/prototype`. Not for production UI; skip ordinary implementation, ADHD, and `/arena`.
- Unknown / hard bugs, regressions, measured slowdown: `/diagnosing-bugs`. Skip typos, known-cause, and test-first known fixes (`/tdd`).
- Authoring SKILL.md / AGENTS.md / skill descriptions / context pointers: `/writing-for-agents` (distinct from `/skill-stocktake` which audits catalog hygiene). Workflow choice is handled directly by the router without a specialist.
- Documents (answer, create, transform, extract, review, PDF/DOCX): `/smartdoc`. File to Markdown ingest: `/markitdown`. Reusable book/module knowledge: `/smartbook-ingest`. SmartDoc may read an existing SmartBook; that is not a second implementation specialist. Impeccable `document` stays DESIGN.md.
- Prose AI-tell removal and natural tone polishing: `/humanizer`. Manual `/unslop` is an alias to the same specialist body. Do not auto-apply on ordinary code or diffs. Technical documentation structure stays `/technical-writing`. Code linting stays `/install-anti-slop`. Prompt structure stays `/prompt-optimizer`.
- Editorial HTML and inline SVG diagrams (architecture, sequence, ER, flowcharts, Wardley): `/diagram-design`. Mermaid/draw.io are inputs to redraw, not final output. Frontend UI implementation stays `/impeccable`. Code-level seams stay `/codebase-design`.
- Agent architecture diagnosis, autonomous loop failures, context leakage, wrapper regressions: `/agent-architecture-audit`. Load only when user names the agent stack job. Defensive security and secrets auditing stay `/full-audit-keamanan`.
- Evaluation harness, prompt/agent benchmarks, pass@k metrics, regression suites: `/eval-harness`. Load only when user names benchmark work. Project code unit tests stay `/tdd`.
- Cost-aware LLM architectures, complexity model tiering, token budgets, prompt caching: `/cost-aware-llm-pipeline`. Load only when user names cost/token budget work. Application bundle and page latency profiling stay `/full-performance-audit`.
- Prompt critique, structural optimization, negative constraints, format locks: `/prompt-optimizer`. General prose polishing stays `/humanizer`.
- OpenCodeHighEnd skill catalog hygiene, frontmatter validation, boundary integrity: `/skill-stocktake`. Code standards review stays `/matt-code-review`.
- REST resource, status, pagination, and versioning design: `/api-design`. Library docs stay Context7. Shared schema ownership stays `/contract-first`. Seam design stays `/codebase-design`.
- Consumer/provider OpenAPI, AsyncAPI, or Protobuf contracts: `/contract-first`. Module seams stay `/codebase-design`.
- Live cron, CI, hook, MCP, and wrapper inventory (keep/merge/cut): `/automation-audit-ops`. Catalog hygiene stays `/skill-stocktake`.
- CodeTour `.tour` walkthroughs with verified file anchors: `/code-tour`. Prose docs stay `/technical-writing`.
- Button/handler sequential-undo and shared-store side effects: `/click-path-audit`. Exploratory browser QA stays `/playwright-qa`.
- Supabase Auth, RLS policies, migrations, Edge Functions: `/supabase-ops` (Context7; not `/impeccable`). Defensive security review of public tables stays `/full-audit-keamanan`.
- MongoDB schemas, indexing, aggregation pipelines: `/mongodb-ops`. Connection strings must never be printed. Official syntax stays Context7.
- Vercel deployment, `vercel.json`, preview URLs, hosting config: `/vercel-ops`. Deploy PR workflow stays `/gh-axi`. Never run `vercel --prod` automatically. Never replace `/found-this-design` or `/impeccable`.
- How it works / where it lives: Codebase Memory first, then `/code-tour`. Why this repo made a choice: suggest `/why`. Break risk: suggest `/blast-radius`.
- Generic AI UI look: `impeccable` taste-guard (not `install-anti-slop`). Generic AI prose: `humanizer` (`/unslop`).
- TypeScript anti-pattern lint install: `/install-anti-slop` (explicit user request only).
- DESIGN.md without bank: still filter slop; do not invent brand facts.
- pstack playbooks: route to existing specialists; no `/poteto-mode`.
- Foreign harness control planes (ECC, Ralph loop, orchestrate, continual-learning) that write AGENTS.md or rules: REJECT.

## Explicit Handoff Graph (Artifact-Gated Edges)

The specialist architecture forms a deterministic graph connected by file artifacts, not conversational hand-waving:
- **UI Direction Edge**: `found-this-design` must emit `.impeccable/found-this-design.json` (pinned `slug`, `bank`, and lane) before handing off to `impeccable`. Never jump from direction to code without an artifact pin.
- **Verification Edge**: `impeccable` produces code, then transfers to `playwright-qa` across an isolated verification boundary (fresh task session, objective snapshot/screenshot evidence). Never accept builder-agent self-attestation as proof.
- **Data Nodes**: Design Bank, Design V2, and shadcn are passive data stores and components, not autonomous agents.
- **Edge Prohibition**: Verbal "and then" transitions without intermediate file artifacts or ledger entries are forbidden.

## UI and browser

- Matching or choosing a visual direction from the local design bank (Refero / Motionsites): `/found-this-design` first. Stop before component implementation. Then `/impeccable` after a pick. Bank root comes from `~/.config/opencode/highend/config/design-bank.json` (optional override `OPENCODE_DESIGN_BANK`).
- Visual UI once a world is chosen, the brief is already visual, or creating UI atoms (buttons, inputs, cards, nav): UI atoms → impeccable after Design V2 shortlist; BANK_MISS ≠ generate. Design V2 shortlist `kind=component` is an internal stage, never a separate specialist route. Do not run `/found-this-design` for atomic components.
- Design Intelligence is an internal, lazy retrieval stage of Impeccable `new-work`, never a primary route or specialist. Design V2 is the same: an offline user bank, never a specialist.
- Stitch MCP: screen/comp generation only; then found-this-design or impeccable + Design V2 atoms. Never implement production UI from Stitch alone. Treat existing Stitch screens as approved comps; local atom shortlist remains mandatory.
- UI Skills MCP: design-skill lookup only. Product UI remains Design Bank + Impeccable + Design V2 atoms + shadcn. BANK_MISS ≠ generate from a random ui-skills document.
- Installable UI components: MCP `shadcn` only. Do not add Magic UI, Kibo, 21st.dev, or community UI MCP servers.
- Use the hub only when cwd has `components.json`. Never silent `shadcn init` on this adapter, a backend or Python tree, or a non-UI cwd.
- Scroll-led storytelling (scroll is the timeline, scrollytelling, signature interaction): `/scroll-craft`. Ordinary scrollable UI stays `/impeccable`. `/scroll-craft` plus Continuous World: Scroll Craft writes the brief, then `/scroll-world`.
- Continuous camera fly-through, diorama, or 3D-world landing: `/scroll-world` even if the request says scroll.
- Procedural Three.js object from image: `/img2threejs` (factory Group, editable primitives, visible vs inferred spec). Not `scroll-world` (camera fly-through), not `hyperframes` (HTML-to-MP4), not `visual-studio` (photoreal stills/media), and not `impeccable` (product UI).
- Deterministic HTML composition rendered to video: `/hyperframes` (headless Chrome + FFmpeg; 18s brag/launch cards via `references/brag.md`). Not `visual-studio`, not `emil-design-eng`. Ordinary scrollable UI stays `/impeccable`.
- Demo video aplikasi, walkthrough layar, narasi Indonesia, demo lomba: skill `id-demo-video` (bukan `hyperframes` untuk durasi panjang utuh, bukan `playwright-qa`, bukan `visual-studio`). Kartu judul HTML→MP4 tetap `hyperframes`.
- Photoreal stills / ads / identity with no UI surface: `/visual-studio`.
- Motion after Impeccable: `/emil-design-eng`.
- Image/video generation: use OpenCode native image tools if the session exposes them. Otherwise write prompt files and mark DEGRADED. Do not invent `image_gen`.
- Exploratory application UI QA: `/playwright-qa` is the primary adapter (navigation, form inputs, state inspection, snapshot, screenshot). Never launch for backend/non-UI.
- Explicit multi-account or persistent browser sessions: `/browser-act`. Load the skill before any `browser-act` command. Never `--type chrome-direct`.
- Observed browser cause: `/chrome-devtools-axi` after `opencode-chromium-cdp start` on `http://127.0.0.1:9223`. Never Google Chrome.
- Deterministic browser regression: existing project test suite (Playwright Test, Cypress, etc.) using project scripts/package manager.
- Anti-Slop lint setup, audit, migration, or removal on TS/JS projects: `/install-anti-slop` (explicit user request only; never auto-run in ordinary coding). Prose cleanup stays manual `/unslop`.

## Risk and GitHub

- Auth, authorization, secrets, public APIs, payment, upload, webhook, privileged operations: `/full-audit-keamanan` plus `semgrep`, `osv-scanner`, `gitleaks`. Do not print secret values.
- Measured regressions in bundle, query, memory, latency, or Core Web Vitals (LCP, INP, CLS): `/full-performance-audit`. FID is legacy.
- GitHub issues, PRs, Actions, releases: `/gh-axi` via `npx -y gh-axi`. If `gh` is not logged in, ask the human to run `gh auth login`.

## Matt flow versus missing bundled names

- Planning and tickets stay on Matt skills: `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/tdd`.
- Architecture DAG: the OpenCode plan agent, not a skill.
- Ordinary writes stay in this session. Spec and ticket implementations stay in this session with `/tdd`.
- Default review is in-session. Two-axis: `/matt-code-review`.
- Manual / slash-only (do not auto-start): `/architect`, `/arena`, `/blast-radius`, `/create-verification-skill`, `/decision-log`, `/demo-video`, `/figure-it-out`, `/improve-codebase-architecture`, `/interrogate`, `/maintain-verification-skill`, `/reflect`, `/technical-writing`, `/unslop`, `/why`, `/wizard`. Suggest them when the user names the job; do not load them as the default path.

## Grok bundled names (do not fake)

| Missing name | OpenCodeHighEnd |
| --- | --- |
| `/design` `/execute-plan` | Plan mode, then in-session write |
| `/implement` | in-session write (no user skill) |
| `/review` `/code-review` | in-session review; `/matt-code-review` if two-axis |
| `/imagine` | NOT_APPLICABLE; directors stay visual-studio / scroll-craft / scroll-world |
| `/docx` `/pdf` | missing alias; nearest = `smartdoc` (do not add `commands/pdf.md` or `commands/docx.md`) |
| `/pptx` | NOT_APPLICABLE |
| `/pr-babysit` | `/gh-axi` |
| `game-asset-*` `/resume-*` `/build-with-ai` | NOT_APPLICABLE |

## Plugins and extra MCP

- No extra marketplace plugins. Foundation = skills + MCP + thin AGENTS.md + runtime helpers.
- User MCP: `codebase-memory-mcp`, `context7`, and `shadcn` on; `serena`, `stitch`, `reticle`, and `ui-skills` absent until a human enables them; `exa` foreign.
- ECC / other harness overlays: `FOREIGN_ON_DEMAND`. Never add, remove, or merge foreign harness control planes or continuous-learning runtimes. Individual warehouse procedures ported in Wave 2 (agent-architecture-audit, cost-aware-llm-pipeline, eval-harness, prompt-optimizer, skill-stocktake) and Wave 3 (api-design, contract-first, automation-audit-ops, code-tour, click-path-audit) are first-party MIT skills. If external ECC is already present in user environment, do not merge and do not shadow.
- FOREIGN vendor packs (e.g. `mongodb/agent-skills`, `supabase/agent-skills`, `vercel-labs/agent-skills`) stay off the overlay; user may `npx skills add mongodb/agent-skills|supabase/agent-skills` locally; never `frontend-design` for product UI.
- Never auto-edit rules or skills from a learning log (no `/learn`, `/evolve`, or session-end skill writers).

## Do not

- Do not enable every specialist in one turn.
- Do not load two implementation specialists in parallel; on mixed requests, implement the primary largest surface first.
- Do not load Wave 2 or Wave 3 warehouse skills unless the user explicitly names the job.
- Do not use vendor `frontend-design` for product UI; UI direction stays `/found-this-design` and implementation stays `/impeccable`.
- Do not print database connection strings, JWTs, or secret keys in Supabase, MongoDB, or Vercel ops.
- Do not use Stitch as an automatic UI implementer or let it replace Design V2 atom shortlist.
- Do not run `/found-this-design` for atomic components (button, input, card, nav); stay in `/impeccable`.
- Do not auto-start planning interviews for ordinary implementation; `/grill-with-docs` handles planning interviews when requested.
- Do not `@`-import the full routing or verification files into CLAUDE.md.
- Do not register 21st.dev, Magic UI MCP, Kibo MCP, or unofficial React Bits / Aceternity MCP.
- Do not run `shadcn init` on this adapter, backend, or Python repositories.
- Do not use Serena before Codebase Memory.
- Do not use ADHD for ordinary work.
- Do not use Emil for static UI, or Impeccable for motion-only work.
- Do not use BrowserAct as a stand-in for project Playwright.
- Do not claim TypeScript, Vitest, coverage, Knip, or Playwright exist unless the current project has them.
- Do not copy or print tokens, gateway URLs, or model-mapping values.
- Do not depend on `~/.grok` at runtime.
