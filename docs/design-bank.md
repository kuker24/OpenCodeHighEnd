# Design Bank

Not in git. Full bootstrap catalogs:

```text
21st/library/catalog.json
aura/library/catalog.json
Refero/bank/catalog.json
motionsites/library/catalog.json
```

Normal `./install.sh` installs the engine only. It does not download Design Bank media.

```bash
./install.sh --with-design-bank
opencode-he design bootstrap
OPENCODE_DESIGN_BANK_URL=... OPENCODE_DESIGN_BANK_SHA256=... opencode-he design bootstrap
```

## Priority

1. Valid local bank (`OPENCODE_DESIGN_BANK` or `~/Design` with all four catalogs) → `already_present`, no download.
2. `OPENCODE_DESIGN_BANK_URL` + `OPENCODE_DESIGN_BANK_SHA256`. URL without SHA-256 fails closed; nothing is downloaded.
3. Default Google Drive ZIP pin in `lib/design_v2/bootstrap_sources.json`.
4. Fallback GitHub `.tgz` in `vendor/sources.json` (`design-bank.artifactUrl` + `artifactSha256`).

The target and generated `~/DesignV2` are user data, not installer-owned. Uninstall never deletes them.

## Operator Drive archive

Publish the ZIP (or `.tgz`) on Google Drive as anyone-with-the-link, or keep it restricted and download it yourself then point `OPENCODE_DESIGN_BANK` at the extracted tree.

Compute the digest of the **archive file**, not of a folder:

```bash
sha256sum OpenCodeHighEnd-DesignBank-v1.zip
```

Accepted URL shapes:

- `https://drive.google.com/uc?export=download&id=FILE_ID`
- `https://drive.google.com/file/d/FILE_ID/view`
- a direct `https://` artifact

View links are rewritten to `uc?export=download`. Large Drive files may hit a virus-scan confirm page; bootstrap follows that token **once** with a temporary cookie jar. The jar is never written into git or `~/.config`.

Drive is first-hop only. After the bank is committed, search, shortlist, inspect, doctor, dedupe, and rebuild stay offline. Aura and 21st live sites are never fetched.

There is no gcloud user OAuth in the installer. Do not put the tarball in this git repository.

## Pointer

```text
~/.config/opencode/highend/config/design-bank.json
```

Missing bank is `DEGRADED` in `opencode-he doctor`, not `FAIL`.

After commit, Design V2 pointer-ingests Refero, Motionsites, 21st, and Aura, then dedupes, rebuilds, and doctors. Preview media remains only under the Design root.

Design Intelligence ships in-tree (`design-intelligence/`) and stays lazy inside Impeccable.
