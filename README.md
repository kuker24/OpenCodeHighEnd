# OpenCodeHighEnd

OpenCode 2 overlay: 62 frozen routed skills, thin `AGENTS.md`, `opencode-he`.

Installer and runtime overlay for [OpenCode 2](https://opencode.ai/v2/docs/). It is **not** Claude Code, **not** GrokBuild, **not** OpenCodeBestFriend runtime, **not** a model provider, and **not** a dump of a developer home directory.

Version **0.1.0**. The 62-skill catalog is inherited from OpenCodeBestFriend 1.8.6 (`67142e4` / PR #29) and stays frozen. This is a new product on a new host.

## What it is

- 62 skills: 47 model-invoked, 15 manual slash commands (frozen; see [docs/CATALOG-FREEZE.md](docs/CATALOG-FREEZE.md))
- A thin `AGENTS.md` router (lazy, one primary specialist)
- Core MCP: Codebase Memory, Context7, shadcn
- 12 Universal Design Banks (34,500+ items across Identity, Motion, Section, Atomic) with zero-token local search & Google Drive v2 bootstrap
- Design Intelligence (lazy, inside Impeccable)
- `opencode-he doctor`, transactional install, uninstall, restore
- Claude Code isolation: `OPENCODE_DISABLE_CLAUDE_CODE=1`

## What it is not

- Not Claude Code configuration
- Not Context Guard / Claude hooks / Claude autocompact
- Not your provider keys, models, or auth state
- Not a Design Bank media repository
- Not OpenCode 1.x (installer fails closed on 1.x)
- Not claimed as macOS/Windows-tested (Linux x86_64 only for this release)

## Quickstart

```bash
# OpenCode 2 must already be on PATH (`opencode --version` → 2.x)
git clone https://github.com/kuker24/OpenCodeHighEnd.git
cd OpenCodeHighEnd

./install.sh --dry-run
./install.sh

# optional: acquire the full user-owned Design Bank and build DesignV2
./install.sh --with-design-bank
# or after install:
# opencode-he design bootstrap
# OPENCODE_DESIGN_BANK_URL=... OPENCODE_DESIGN_BANK_SHA256=... opencode-he design bootstrap

# pick up OPENCODE_DISABLE_CLAUDE_CODE=1
exec "$SHELL"
# or: source ~/.bashrc   (bash)
# or: source ~/.zshrc    (zsh)

opencode-he verify
opencode-he doctor
opencode-he doctor --deep
opencode
```

Restart OpenCode after install. Config is not hot-reloaded.

## Architecture

```text
                         OpenCode
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
      │  ├─ 21st
      │  ├─ Aura
      │  ├─ Refero
      │  └─ Motionsites
      ├─ Design Intelligence
      ├─ Design V2 (offline user bank, ~/DesignV2)
      └─ SmartDoc / SmartBook (user-owned ~/SmartDoc)
```

Availability is not a reason to activate a tool. One primary specialist. At most one risk specialist.

## Skill routing

Default: repository evidence first. Then at most one specialist.

| Intent | Route |
| --- | --- |
| Repo understanding | Codebase Memory MCP |
| How it works / where it lives | Codebase Memory then `code-tour` |
| Repo rationale | `/why` (manual) |
| Hard unknown bug | `diagnosing-bugs` |
| Security-sensitive work | `full-audit-keamanan` |
| Measured performance regression | `full-performance-audit` |
| Current library docs | Context7 |
| UI registry | shadcn MCP |
| Visual direction | `found-this-design` |
| UI implementation after a direction | `impeccable` |
| Generic AI UI look | `impeccable` taste-gate (not `install-anti-slop`) |
| Motion | `emil-design-eng` |
| Photoreal / media | `visual-studio` |
| Scroll-led storytelling | `scroll-craft` |
| Scroll-driven 3D / camera world | `scroll-world` |
| Procedural Three.js object from image | `img2threejs` |
| Deterministic HTML composition video | `hyperframes` |
| Demo video aplikasi & narasi ID | `id-demo-video` (`/demo-video`) |
| Browser | `playwright-qa` → `browser-act` → `chrome-devtools-axi` → `click-path-audit` |
| Documents (PDF/DOCX/answer/extract/review) | `smartdoc` |
| File to Markdown ingest | `markitdown` |
| Reusable book/module knowledge | `smartbook-ingest` |
| Scholarly literature & manuscripts | `academic` |
| Generic AI prose | `humanizer` / `/unslop` |
| Editorial HTML/SVG diagrams | `diagram-design` |
| TS Oxlint install | `install-anti-slop` (explicit only) |
| Architecture bake-off | `/architect` (manual) |

Warehouse: `api-design`, `contract-first`, `automation-audit-ops`, `code-tour`, `click-path-audit` (plus Wave 2 diagnostics).

Examples: interactive product story told by scroll → `scroll-craft`. Unbroken camera through a miniature factory → `scroll-world`. Clean security dashboard → `impeccable`. Video, image generation, and Design V2 stay optional.

Manual skills are OpenCode commands. They are not auto-discovered.

When an agent names tools, it should report `USED` / `CONSIDERED_NOT_USED` / `MANUAL_NOT_INVOKED`.

## MCP

Native OpenCode 2 shape (`mcp.servers`, every entry has `type`, `disabled` not V1 `enabled`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/.config/opencode/skills"],
  "mcp": {
    "servers": {
      "codebase-memory-mcp": {
        "type": "local",
        "command": ["~/.local/share/opencode-highend/components/codebase-memory/bin/codebase-memory-mcp"],
        "disabled": false
      },
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "disabled": false
      },
      "shadcn": {
        "type": "local",
        "command": ["npx", "-y", "shadcn@4.18.0", "mcp"],
        "disabled": false
      }
    }
  }
}
```

Core (installed):

- `codebase-memory-mcp` — downloaded, SHA-256 verified, Linux x86_64. If the binary will not run, doctor reports `DEGRADED`, never fake `CONNECTED`.
- `context7` — `https://mcp.context7.com/mcp` (no secret stored)
- `shadcn` — `npx -y shadcn@4.18.0 mcp`

Optional:

- `serena` — host binary may exist; MCP is **not** registered unless you run `opencode-he serena enable`
- `stitch` — `opencode-he stitch enable` registers Google Stitch as a remote comp/mock source. Not an owned core server and not a production UI implementer: hand screens to `found-this-design` or `impeccable` before shipping. Keys are never written into config, only referenced as `{env:STITCH_API_KEY}`, or omitted with `--oauth`. `opencode-he stitch disable` removes only that server key. Absent is not a `doctor` failure; a malformed entry fails closed.
- `reticle` — `opencode-he reticle enable` registers Reticle as a local perception server (`npx -y @reticlehq/server mcp`). `FOREIGN_ON_DEMAND`. Server package is FSL-1.1-ALv2 (competing-use clause); SDK packages (Apache-2.0) are not vendored. Never an auto-implementer; default verification remains `playwright-qa` / `chrome-devtools-axi`. `opencode-he reticle disable` removes only that server key. Absent is not a `doctor` failure; a malformed entry fails closed.
- `ui-skills` — `opencode-he ui-skills enable` registers UI Skills (`https://www.ui-skills.com/mcp`) as an optional remote MCP server. `FOREIGN_ON_DEMAND` for design-skill lookup only. Product UI remains Design Bank + Impeccable + Design V2 atoms + shadcn; `BANK_MISS` never generates from a random ui-skills document. `opencode-he ui-skills disable` removes only that server key. Absent is not a `doctor` failure; a malformed entry fails closed.
- `markitdown` — `opencode-he markitdown enable` registers MarkItDown as a local stdio ingest converter (`uvx --from markitdown-mcp markitdown-mcp`). `FOREIGN_ON_DEMAND`. Local trusted agents only; never `--http` / `0.0.0.0` / docker bind-all. Output is Markdown data; SmartDoc keeps contract/QA/render. `opencode-he markitdown disable` removes only that server key. Absent is not a `doctor` failure; a malformed entry fails closed.
- `exa` — `FOREIGN_ON_DEMAND`; installer never adds, removes, or overwrites it

NVIDIA SkillEvaluator is `FOREIGN_ON_DEMAND` in the same sense: a maintainer may run it externally for embedding-based overlap scoring or live catalog evaluation. Caliper is `FOREIGN_ON_DEMAND` similarly: a maintainer may `pipx install caliper-eval` off-tree for prompt/agent benchmark evaluation. Neither is vendored into `lib/`, the installer never adds them, `doctor` does not fail when they are absent, and a malformed MCP entry fails closed like any other schema violation.

The installer merges only owned MCP keys. Provider, model, permissions, plugins, and foreign MCP stay yours.

## Design Bank (12 Universal Banks)

Design Bank media is **not** vendored in this repository. Redistribution of the media archive is not cleared as first-party content.

OpenCodeHighEnd connects to an offline collection of **12 Design Banks** (34,500+ curated items) across four architectural tiers:
- **Identity**: `Refero` (design systems, CSS tokens, typography, colors), `Aura` (complete landing & dashboard templates)
- **Motion**: `Motionsites` (motion direction & UI animation), `Scrolltide` (scrollytelling & timeline pinning), `Bencho` (micro-interactions & widgets), `Layers` (3D Three.js & WebGL shaders)
- **Section**: `Supahero` (SaaS hero headers), `NavbarGallery` (navigation bars & mega menus), `FooterDesign` (footers & sitemaps), `CtaGallery` (call-to-action blocks), `404sDesign` (empty states & error pages)
- **Atomic**: `21st` (atomic components; handed off to Impeccable)

Normal `./install.sh` installs the engine only and never starts the multi-gigabyte download. Full setup with the design suite is explicit:

```bash
./install.sh --with-design-bank
# or anytime post-install:
opencode-he design bootstrap
# custom mirror override:
OPENCODE_DESIGN_BANK_URL=... OPENCODE_DESIGN_BANK_SHA256=... opencode-he design bootstrap
```

Download sources (SHA-256 fail-closed; URL without SHA is refused):

1. **Default Drive pin** in `lib/design_v2/bootstrap_sources.json` (`OpenCodeHighEnd-DesignBank-v2.zip`, SHA-256 `43b36134c35c476bcdeb633aa55f58ada18a163ade4e867d8fcf9380433b54d2`). Google Drive is contacted only during bootstrap.
2. **Fallback GitHub artifact** in `vendor/sources.json` (`GrokBestFriend` `Design-bank.tgz`, sha256 `9866f5a8…`). Used when the Drive pin is unavailable.

Operator override: `OPENCODE_DESIGN_BANK_URL` + `OPENCODE_DESIGN_BANK_SHA256`. Drive view links (`/file/d/ID/view`) resolve to `uc?export=download`. A valid local bank (at `OPENCODE_DESIGN_BANK` or `~/Design`) is used as-is — no download.

Bootstrap verifies SHA-256, extracts to a temp directory, validates catalogs, then commits into `~/Design` or `OPENCODE_DESIGN_BANK`. Uninstall never deletes `~/Design` or `~/DesignV2`. After bootstrap, all queries and searches via skill `found-this-design` stay 100% offline with zero token context overhead.

## Design Intelligence

Portable policy, taxonomy, schemas, and Python runtime ship in git. The installer copies them into OpenCode-owned paths. Retrieval stays lazy inside Impeccable `new-work`.

## Design V2

Offline user-data bank at `OPENCODE_DESIGN_V2` or `~/DesignV2`. Not installer-owned. Uninstall does not touch it.

## SmartDoc / SmartBook

`smartdoc` handles per-job documents (answer, create, transform, extract, review, PDF/DOCX). `smartbook-ingest` compiles reusable local knowledge. User data lives at `OPENCODE_SMARTDOC` or `~/SmartDoc` and survives uninstall.

```bash
opencode-he smartdoc status --json
opencode-he smartdoc doctor --json
opencode-he smartdoc render content.md --renderer handwriting --output tugas.pdf --json
opencode-he smartdoc profile create campus --field Nama=Budi --field NIM=12345
opencode-he smartbook ingest ./module.md --slug jaringan
```

Local Similarity Audit compares against a named corpus. It is not Turnitin and does not report `0.0` for unreadable evidence. Optional `pypdf`, Pillow, `pdftoppm`, and Tesseract (`eng`/`ind`) report `NOT_CONFIGURED` when absent. PDF extract uses native text when sufficient and OCR AUTO per page otherwise; OCR limits and partial pages are explicit.

```bash
opencode-he design import ~/Downloads/aura-export --provider aura
opencode-he design sources
opencode-he design ingest --provider aura --source-id <source_id>
opencode-he design dedupe
opencode-he design rebuild
opencode-he design doctor
opencode-he design search "premium cybersecurity dashboard dark minimal"
opencode-he design shortlist --query "premium cybersecurity dashboard dark minimal"
opencode-he design inspect <id>
```

`import` accepts local files, folders, or ZIPs only and returns a stable staged `source_id`. A direct `ingest --provider <provider> <local-path>` remains available as a one-step shortcut. URLs are rejected and no command fetches Aura or 21st content.

Search, inspect, doctor, sources, and shortlist are read-only and do not create the bank. JSONL is canonical; missing or stale FTS is `DEGRADED_FTS`. Run `opencode-he design --help` for the complete local lifecycle.

## Claude isolation

OpenCodeHighEnd does not write `~/.claude/`, does not run `claude`, and does not import Claude hooks or Context Guard.

```text
Context Guard: NOT_PORTED_BY_DESIGN
OpenCode autocompact: NATIVE
```

## Installer

User-local, no sudo:

```text
~/.config/opencode/
~/.local/share/opencode-highend/
~/.local/bin/
```

Transactional states: `PREPARING` → `STAGED` → `VALIDATED` → `BACKED_UP` → `APPLIED` → `VERIFIED` → `COMMITTED`.

Backup `preInstall` records whether config, `AGENTS.md`, commands, helpers, shell rc, and share trees existed. Recover restores present files and **deletes** installer-created files that were previously absent.

`AGENTS.md` is marker-merged (`<!-- OPENCODEHIGHEND:BEGIN -->` … `END`). Foreign text outside the markers is preserved. Foreign `commands/<name>.md` and foreign `~/.local/bin/opencode-he` / `opencode-chromium-cdp` fail closed instead of being overwritten.

Upgrade recover restores prior `~/.local/share/opencode-highend/product` and `components` when those trees existed before apply.

Collision preflight (foreign skills/commands/helpers, parseable config, writable targets) runs before backup and apply. `opencode-he serena enable` does not strip JSONC comments.

Official OpenCode gate is **2.x** (1.x fails closed). Config is native V2: `skills` is an array, MCP lives under `mcp.servers`, every server has `type`. JSONC comments are preserved when owned MCP keys can be patched surgically. V1 plugins are not copied and do not run. `lsp` is not ported.

```bash
./install.sh --dry-run
./install.sh --recover
opencode-he uninstall
opencode-he restore --list
opencode-he verify
opencode-he doctor
opencode-he doctor --deep
opencode-he doctor --strict
```

`verify` checks owned files are canonical. `doctor` checks install/config health (MCP `CONFIGURED` is not live). `doctor --deep` requires core MCP `CONNECTED`. `doctor --strict` fails on `DEGRADED`/`WARN`. FOREIGN MCP absent is not a failure; a malformed MCP entry (missing `type`) fails closed.

Update:

```bash
git pull
./install.sh
```

## Compatibility

Officially tested:

- Linux x86_64
- OpenCode 2.x
- Python 3, Node + npx, git, curl, tar

Optional host tools: Chromium, `gh`, browser-act, serena, semgrep, osv-scanner, gitleaks.

## Security model

- Fail-closed checksums for Codebase Memory and Design Bank downloads
- No API keys, tokens, or provider maps in git
- Ownership manifest: only claimed files are uninstalled
- Optional scanners are detected, never bundled

See [docs/security.md](docs/security.md).

## Provenance

Capability source: [OpenCodeBestFriend](https://github.com/kuker24/OpenCodeBestFriend) 1.8.6 (`67142e4`, catalog freeze PR #29). That overlay targeted OpenCode 1.18.x; HighEnd rewrites the installer and config for OpenCode 2. Adapted ≠ first-party. Licenses: [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Copied vs rewritten

Copied from OCBF 1.8.6 then path-rewritten: 47 model skills, 15 manuals + commands, rules, Design Intelligence, Design V2 / SmartDoc libraries, CBM pin, allowlist/policy.

Rewritten native V2: installer version gate, `mcp.servers` merge, `skills` array, doctor, AGENTS markers (`OPENCODEHIGHEND`), identity (`opencode-he`, `~/.config/opencode/highend`).

Not copied: V1 plugins, `lsp` blocks, provider tokens, Design Bank media, GrokBuild / `~/.grok` runtime paths.

## License

MIT for first-party installer, docs, overlays, and tests. Vendored skills keep their upstream licenses.
