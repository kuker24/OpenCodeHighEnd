# Tree then reason

Pin: `VectifyAI/PageIndex@037a7dbacfb9a19f38b354ce60cee5094b3f854c` (MIT).

## Why a tree

Vector RAG retrieves by similarity. Long professional documents need
**relevance**, which takes a map of sections and a reason to open one.
PageIndex-style retrieval is two steps:

1. **Index** — hierarchical tree (title, summary, page/section span, children).
2. **Retrieve** — LLM (or this session) walks the tree, recording why each node
   was opened, then reads only those leaves.

No vector DB. No blind chunking.

## Local overlay path (no extra deps)

When the SDK is absent:

1. Extract text via `smartdoc` or `markitdown` (existing tools).
2. Build a heading tree from TOC / `h1–h3` / numbered sections.
3. Summarize each node in ≤150 words from its own text (do not invent).
4. Walk: start at root, pick children with a one-line reason, stop at leaves.
5. Quote spans with page or heading provenance.

This is DEGRADED relative to upstream flash indexing, but it is honest.
Missing extractors → `NOT_CONFIGURED`.

## Optional SDK (user machine)

```text
pageindex Python package on PATH or importable
→ local flash index allowed
→ never pip-install into OpenCodeHighEnd
```

Cloud `index="cloud"` / `PAGEINDEX_API_KEY` / PageIndex MCP: do not configure.

## Boundaries

| Need | Route |
|---|---|
| Tree/reasoning over a long doc | **pageindex** |
| Official docs / API facts | `research` |
| Scholarly IMRaD | `academic` |
| Contract/OCR/render | `smartdoc` |
| Code symbols | codebase-memory-mcp |
| Entity knowledge graphs | REJECT (Graphiti/Cognee) |
