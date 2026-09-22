# Troubleshooting

`OPENCODE_MISSING` — install OpenCode 2.x (`curl -fsSL https://opencode.ai/v2/install | bash`) and put `opencode` on PATH.

`UNSUPPORTED_OPENCODE_VERSION` — this release supports OpenCode 2.x (`mcp.servers`). 1.x fails closed.

`V1_PLUGIN_LEFTOVER` / `failed to load plugin` — OpenCode 2 rejects legacy V1 plugins (such as `impeccable-live-poll.ts` from OCBF) in `~/.config/opencode/plugins/`. Re-run `./install.sh` to quarantine known legacy plugins to `~/.local/share/opencode-highend/quarantine/plugins/`, or move them manually.

`CODEBASE_MEMORY_CHECKSUM_FAILED` — delete `~/.local/share/opencode-highend/cache/downloads/` and retry. Do not ignore a mismatch.

`DESIGN_BANK_INVALID` — bootstrap requires parseable 21st, Aura, Refero, and Motionsites catalogs (the 4 foundational bootstrap catalogs; `found-this-design` indexes up to 12 banks once present). Fix the configured target or choose a new empty `--target`.

`DOWNLOAD_FAILED` / `CHECKSUM_MISMATCH` — core installation remains valid. Retry `opencode-he design bootstrap`; an unverified archive is never extracted.

`FOREIGN skill collision` — an unowned skill already occupies that name. Move or rename it.

`STALE_TRANSACTION` — `./install.sh --recover`

`INVALID_BACKUP_STAMP` / `BACKUP_PATH_ESCAPE` — restore stamps are `[A-Za-z0-9][A-Za-z0-9._-]{0,63}` only.

`FAIL INSTALLED_VERSION` / `FAIL SOURCE_REPOSITORY` — runtime is not this OpenCodeHighEnd release. Re-run `./install.sh` from the matching clone (ClaudeBestFriend overlays migrate automatically).

`STALE AGENTS.md` — owned block missing USED / CONSIDERED_NOT_USED / MANUAL_NOT_INVOKED. Reinstall.

Doctor `OPTIONAL_ABSENT` is not a core failure. `DEGRADED` is non-fatal unless `doctor --strict`. `EMPTY Design V2` means no user bank yet — not a failure. `DEGRADED_FTS` means JSONL search works without SQLite FTS.

`doctor --deep` exit 1 with `NOT_CHECKED` — `opencode mcp list` failed or was empty; core MCP is not proven live.

Restart OpenCode after install.
