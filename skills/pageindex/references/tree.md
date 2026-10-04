# Tree then reason

Pin: `VectifyAI/PageIndex@037a7dbacfb9a19f38b354ce60cee5094b3f854c` (v0.2.21, MIT).

## Why a tree

Vector RAG retrieves by similarity. Long professional documents need
**relevance**, which takes a map of sections and a reason to open one.
PageIndex-style retrieval is two steps:

1. **Index** — hierarchical tree (title, summary, start_index, end_index, page/section span, children).
2. **Retrieve** — LLM (or this session) walks the tree, recording why each node
   was opened, then reads only those leaves.

No vector DB. No blind chunking.

## Tree Node Schema (v0.2.21)

Every node in the hierarchical tree structure carries explicit range boundaries:

- `title`: Heading text or section name.
- `summary`: Abstract or distillation of the section content (≤150 words).
- `start_index`: 0-based start index / page offset of the node within document stream.
- `end_index`: 0-based end index / page offset (span boundary).
- `page_span`: Human-readable page interval (e.g. `pp. 14–22`).
- `children`: Nested list of child tree nodes.

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
