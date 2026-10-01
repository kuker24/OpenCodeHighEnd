# Architecture

```text
                         OpenCode 2
                            │
                       AGENTS.md
                            │
                     Thin Lazy Router
                            │
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                    ▼
      Skills               MCP                 Rules
      50 automatic       Codebase Memory        Verification
      15 manual          Context7              Engineering
                       shadcn
        │
        ▼
     Design / Documents
      ├─ Design Bank (12 universal banks; 4 bootstrap required: Refero, Motionsites, 21st, Aura)
      │  ├─ Identity: Refero, Aura
      │  ├─ Motion: Motionsites, Scrolltide, Bencho, Layers
      │  ├─ Section: Supahero, Navbar, Footer, CTA, 404s
      │  └─ Atoms: 21st
      ├─ Design Intelligence
      ├─ Design V2 (offline, ~/DesignV2)
      └─ SmartDoc / SmartBook (resolved SmartDoc root)
```

Runtime destinations (user-local):

- Model skills → `~/.config/opencode/skills/<name>/`
- Manual skills → `~/.config/opencode/highend/skills/<name>/`
- Commands → `~/.config/opencode/commands/<name>.md`
- Rules → `~/.config/opencode/highend/rules/`
- Ownership → `~/.config/opencode/highend/manifests/ownership.json`

OpenCode native context engine and autocompact are unchanged. Context Guard is not ported.

## Specialist Graph & Handoff Edges

Instead of opaque multi-agent swarms or chat-based delegation, OpenCodeHighEnd operates as an explicit, artifact-gated directed graph:

1. **Direction Node -> Implementation Node**: `found-this-design` must write `.impeccable/found-this-design.json` before `impeccable` begins implementation. Direction without a pinned artifact is rejected.
2. **Implementation Node -> Verification Node**: `impeccable` produces code, which hands off to `playwright-qa` across an isolated verification boundary. The verification agent operates in a clean session, proving claims with screenshots, traces, or test exit codes rather than relying on builder reasoning.
3. **Data Nodes vs Agents**: Design Bank, Design V2, and shadcn are passive data sources and component registries, never pseudo-agents.
4. **No Phantom Transitions**: Every inter-specialist edge requires a machine-readable artifact or ledger entry. Unbacked "and then" handoffs are strictly forbidden.
5. **Generative UI Node (`json-render`)**: Handed off from `prototype` or `found-this-design` when UI must be generated from typed JSON schemas or component catalogs rather than freeform layout code.
6. **Consulting Slide Decks Node (`deck-design`)**: Handed off from `smartdoc` for consulting PPTX and 16:9 HTML slide decks. `smartdoc` retains document contracts/OCR/PDF rendering; `markitdown` retains file-to-Markdown ingest.
7. **Long-Document Navigation Node (`pageindex`)**: Handed off from `research` for navigating deep, structured documents (filings, manuals, technical specs) using hierarchical tree reasoning rather than naive vector similarity chunking. Primary-source citation rules remain strictly enforced.
8. **Commercial Launch Films & Business Explainers (`business-motion-film`)**: Handed off for business ads, launch films (including real app UI product-film mode), sample reels, and explainers. Rendering is strictly executed through `hyperframes`; Three.js product-hero patterns are absorbed into references (not a standalone skill). Continuous 3D camera flight stays with `scroll-world`, 18s brag cards stay in `hyperframes/references/brag.md`, and Indonesian narrated tours stay with `id-demo-video`.
9. **Multi-Provider Gateway Node (`ninerouter`)**: Handed off when routing inference, image/video generation, speech, transcription, embeddings, or web fetch/search through a user-managed 9Router gateway. 9Router is `FOREIGN_ON_DEMAND`, not an extra core MCP server. Zero-bind prohibition: fails closed immediately on `0.0.0.0`. Graceful degradation to `NOT_CONFIGURED` if the gateway is absent or unreachable.

## Harness Engineering Principles

Adapted from *awesome-harness-engineering* and production agent systems:
- **Harness Over Model**: System correctness, fail-closed boundaries, and deterministic verification gates matter far more than prompt persuasion.
- **Context Hygiene**: Lazy specialist activation ensures context is never polluted with irrelevant skills. Closed intent classification routes requests to exactly one specialist.
- **Evidence-First Done Gate**: Completion claims require mechanical fact proofs in an evidence ledger (`FACT:` vs `JUDGMENT:`). Model judgment advises but never overrides verification results. External Jev/Canny servers are skipped; typed-gate verification patterns operate entirely offline.
- **Host & Tooling Guardrails**: Product identity is strictly OpenCode 2. Session tools are strictly `tools.opencode.*`; Codebase Memory operations only target verified existing repository roots.
