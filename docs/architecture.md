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
      47 automatic       Codebase Memory        Verification
      15 manual          Context7              Engineering
                       shadcn
        │
        ▼
     Design / Documents
      ├─ Design Bank
      │  ├─ Refero
      │  └─ Motionsites
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
