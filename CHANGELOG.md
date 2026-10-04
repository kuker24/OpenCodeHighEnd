# Changelog

## 0.1.16 — 2026-10-04

Patch koreksi pasca-0.1.15 untuk atribusi aset anti-slop, pemulihan catatan penundaan upstream c44ef22, dan penyempurnaan emulasi Playwright QA (permissions geolokasi). Katalog tetap 65 (50 model + 15 manual). Closed intents tetap 25. Tidak ada penambahan atau pensiun skill (`vendor/skill-allowlist.txt` dan `vendor/skill-policy.json` tidak berubah).

- **Koreksi**: Klaim pada 0.1.15 "memperbaiki pemeriksaan terbalik" adalah salah atribusi; upstream `e8c4880` tidak pernah memiliki bug tersebut, melainkan sinkronisasi 0.1.15 memulihkan drift lokal yang ada di OCH sejak bootstrap 0.1.0 (`202cc46`). Catatan evaluasi upstream `c44ef22` (3 generic rules, 4 Effect rules, shared helpers, vendored eslint-stylistic) dipulihkan ke `docs/source-wave.md` dengan status DEFERRED.
- **Penyempurnaan emulasi Playwright QA (geolokasi & permissions)**: Menegaskan bahwa emulasi geolokasi pada launch config `.playwright/cli.config.json` wajib menyertakan `contextOptions.permissions: ["geolocation"]` agar tidak ditolak dengan `"User denied Geolocation"`. Menjelaskan pemisahan runtime `run-code`: geolokasi menggunakan API Playwright standar (`grantPermissions`/`setGeolocation`) yang lintas-browser, sedangkan emulasi runtime timezone dan locale spesifik Chromium via CDP (`setTimezoneOverride`/`setLocaleOverride`).
- **Versi Produk**: Bump versi ke `0.1.16` (`VERSION`, `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `README.md`, `docs/CATALOG-FREEZE.md`).

## 0.1.15 — 2026-10-04

Rilis pemeliharaan Wave 0.1.15 untuk sinkronisasi aset vendored anti-slop, standardisasi emulasi Playwright QA, dan pembersihan impor mati. Katalog tetap 65 (50 model + 15 manual). Closed intents tetap 25. Tidak ada penambahan atau pensiun skill (`vendor/skill-allowlist.txt` dan `vendor/skill-policy.json` tidak berubah).

- **Sinkronisasi aset anti-slop (v0.1.2)**: Menyinkronkan seluruh aset linter Oxlint vendored di `skills/install-anti-slop/assets/anti-slop` dari upstream `dmmulroy/anti-slop@e8c4880471b23ab7f216fba7b27d173a6ef07d4c`, memperbaiki pemeriksaan jenis variabel terbalik pada `rules/no-widen-then-assert.ts`. Seluruh 23 berkas aset terverifikasi identik 100% dengan blob upstream. Memperbarui catatan di `docs/source-wave.md`.
- **Standardisasi emulasi Playwright QA**: Menstandardisasi doktrin emulasi timezone, locale, dan geolocation dengan konfigurasi JSON pada peluncuran (`.playwright/cli.config.json` via `contextOptions`) sebagai metode lintas-browser utama, dan `run-code` sebagai alternatif runtime spesifik Chromium via CDP. Menyelaraskan dokumentasi pada `skills/playwright-qa/references/workflow.md`, `skills/playwright-qa/SKILL.md`, dan `rules/00-routing.md`.
- **Pembersihan impor mati**: Menghapus impor yang tidak terpakai `repo_root` pada `lib/design_v2/bootstrap.py` dan `tarfile` pada `tests/test_design_bootstrap.py`.
- **Versi Produk**: Bump versi ke `0.1.15` (`VERSION`, `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `README.md`, `docs/CATALOG-FREEZE.md`).

## 0.1.14 — 2026-10-04

Patch rilis pasca-0.1.13 untuk koreksi pin sumber, penuntasan pensiun fallback Design Bank, dan perbaikan path config Playwright. Katalog tetap 65 (50 model + 15 manual). Closed intents tetap 25. Tidak ada penambahan atau pensiun skill (`vendor/skill-allowlist.txt` dan `vendor/skill-policy.json` tidak berubah).

- **Koreksi pin crawl4ai**: Memperbaiki commit SHA crawl4ai di `vendor/sources.json` yang sebelumnya salah tercatat (salah hash tip) menjadi `133e1d92e37885dfccc03ea2e3687d06c98b7ceb` sesuai rilis tag resmi `v0.9.4` (tag `a9634e9`), menyelesaikan error HTTP 422 pada resolusi commit GitHub API. Menambahkan tes invariant di `tests/test_v2_schema.py`.
- **Penuntasan pensiun Design Bank Fallback #4**: Menghapus implementasi runtime fallback GitHub dari `lib/design_v2/bootstrap.py` dan method `curl-github-release`. Kegagalan resolusi Google Drive kini langsung meneruskan `BootstrapError` asli (fail-closed) tanpa menutupi akar masalah. Memperbarui `tests/test_design_bootstrap.py` untuk menguji penjalaran error Drive tanpa fallback. Mengarahkan entri komponen `design-bank` di `vendor/provenance.json` ke pin Google Drive v3 (`lib/design_v2/bootstrap_sources.json`, `OpenCodeHighEnd-DesignBank-v3.zip`, SHA-256 `91d90b4e...`).
- **Koreksi path config Playwright QA**: Memperbaiki dokumentasi pada `skills/playwright-qa/references/workflow.md` agar merujuk ke file JSON (default `.playwright/cli.config.json`). Menegaskan bahwa emulasi timezone, locale, dan geolocation diatur secara programatik melalui `run-code`. Menyelaraskan catatan pada `skills/playwright-qa/SKILL.md` dan `rules/00-routing.md`.
- **Harmonisasi hierarki invarian reflect**: Memperjelas subjudul pada `manual-skills/reflect/references/correct.md` menjadi adaptasi 5 level OCH (upstream pstack menggabungkan types dan linter menjadi 4 level).
- **Versi Produk**: Bump versi ke `0.1.14` (`VERSION`, `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `README.md`, `docs/CATALOG-FREEZE.md`).

## 0.1.13 — 2026-10-04

Wave 0.1.13 upstream sync across 6 discrete scopes (A–F). Katalog tetap 65 (50 model + 15 manual). Closed intents tetap 25. Tidak ada penambahan atau pensiun skill (`vendor/skill-allowlist.txt` dan `vendor/skill-policy.json` tidak berubah).

- **Scope A (Pins & MCP)**: Pembaruan pin MCP `shadcn@4.21.1`, `@reticlehq/server@3.5.0`, `markitdown-mcp==0.0.1a7` dengan `markitdown[all]==0.1.8`, dan standardisasi `crawl4ai` endpoint ke `/mcp/sse` (URL lama `/mcp` memicu peringatan `CRAWL4AI_LEGACY_URL`). Menambahkan deteksi shadow `context7-mcp` pada doctor.
- **Scope B (Skill Refresh)**: Memperbarui `playwright-qa` dengan opsi emulasi perangkat (`open --device`), resize viewport (`resize`), perintah sesi media (`set-color-scheme`, `set-reduced-motion`), dan batas keamanan WebMCP (`webmcp-list`, `webmcp-call`). Menambahkan mode `update` pada `install-anti-slop` (`manage.mjs`) untuk memperbarui aset vendored sambil menjaga preferensi profil. Menyelaraskan handoff browser dual-door pada `scroll-craft`.
- **Scope C (Doctrines)**: Mengadaptasi doktrin adversarial UI stress testing `break-ui` (Emil Kowalski) ke `skills/impeccable/reference/break-ui.md` dengan alur 6 fase, dev toggle, dan failure signatures. Mengadaptasi hierarki penegakan invarian 5 level `pstack /correct` ke `manual-skills/reflect/references/correct.md`. Memperbarui `business-motion-film` (product-film mode) dengan scored review 7 dimensi, tinjauan layar ponsel 360 px, dan rata-rata subframe motion blur. Memperbarui `manual-skills/architect` dengan lensa kontributor agent (asumsi perbaikan lokal harus aman global).
- **Scope D (Tata Kelola & Inventaris)**: Pembaruan catatan disposisi upstream di `docs/source-wave.md` dan `docs/warehouse-inventory.md` untuk sinkronisasi wave 0.1.13. Batas lisensi GPL-3.0-or-later repository `oraios/serena` (`6707cd9b7efbaea1435fb7bfd7ff20d4b5916983`) ditegaskan tetap sebagai pointer eksternal (`POINTER_ONLY`/`OPTIONAL_ABSENT`).
- **Scope E (Atribusi & Notices)**: Sinkronisasi atribusi upstream pada `THIRD_PARTY_NOTICES.md`, `vendor/sources.json`, `vendor/license-audit.json`, dan berkas `NOTICE.md` terkait (`skills/business-motion-film/NOTICE.md`, `skills/install-anti-slop/NOTICE.md`, `skills/playwright-qa/NOTICE.md`, `skills/scroll-craft/NOTICE.md`). Bukti lisensi pstack diperbarui ke `e43c7ee` (0.15.9). Label Matt Pocock distandardisasi menjadi `v1.3.0 (d81f3a1; tag 984a2c0 = version bump)`. Full SHA hyperframes (`6037d228441e`) dan ninerouter (`a99cf57239ff`) diverifikasi penuh.
- **Scope F (Rilis)**: Bump versi produk ke 0.1.13 (`VERSION`, `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `docs/CATALOG-FREEZE.md`, `README.md`). Menjalankan seluruh test suite secara komprehensif.
- Design Bank: pensiunkan fallback #4 GitHub release artifact (kuker24/GrokBestFriend 404); prioritas bootstrap kini: local bank -> operator URL/SHA -> Google Drive ZIP pin.

## 0.1.12 — 2026-10-04

Wave 0.1.12 body-only ("skill-refresh"). Katalog tetap 65 (50 model + 15 manual). Tidak ada pertumbuhan allowlist (`vendor/skill-allowlist.txt` tidak berubah). Tidak ada penambahan atau pensiun skill. Exception 0.1.8 tetap spent.

- `hyperframes`: Pembaruan ke upstream v0.8.119 (commit `3a0299e851ce`). Mengadaptasi kontrak render deklaratif berbasis data attributes (`data-composition-id`, `data-width`, `data-height`, `data-fps` pada elemen root dan `data-start`, `data-duration`, `data-track-index` pada elemen klip berkelas `.clip`). Memperbarui pipeline CLI resmi (`npx hyperframes render [dir] -o <path> -f <fps> -q <quality> [--format]`) dengan fallback CDP/FFmpeg. Menegaskan prasyarat Node.js ≥22 dan FFmpeg lokal (jika tidak lengkap -> `NOT_CONFIGURED`, dilarang melaporkan PASS palsu). Menolak instalasi skill luar (`npx skills add heygen-com/hyperframes` dan `npx hyperframes skills update` dilarang).
- `awesome-opus5-5-videos`: Penambahan referensi first-party `POINTER_ONLY` di `skills/hyperframes/references/prompt-patterns.md` (snapshot `3d54892e2ae5b0e8d337171e6508bba4cec01ab8`, 2026-09-29). Menjelaskan translasi prompt viral satu baris menjadi brief HyperFrames berparameter deterministik tanpa menyalin prompt, dataset, atau media pihak ketiga. Menambahkan pointer di `rules/00-routing.md`.
- Migrasi Matt Pocock cluster: Format nama domain glossary diperbarui dari konvensi lama `CONTEXT.md` / `CONTEXT-MAP.md` menjadi `GLOSSARY.md` / `GLOSSARY-MAP.md` mengikuti upstream v1.3. Berkas `skills/domain-modeling/CONTEXT-FORMAT.md` dipindahkan menjadi `GLOSSARY-FORMAT.md`. Seluruh referensi pada spesialis dan aturan (`domain-modeling`, `grill-with-docs`, `codebase-design`, `tdd`, `diagnosing-bugs`, `/improve-codebase-architecture`, `/why`, `00-routing.md`, `03-prose-discipline.md`) diselaraskan ke `GLOSSARY.md`. Fallback kompatibilitas backward dipertahankan di `domain-modeling` dan `grill-with-docs` agar repositori pengguna yang sudah memiliki `CONTEXT.md` tetap terbaca tanpa diubah secara sepihak. Menolak impor skill baru dari upstream (`implement-spec`, `pr`, `retro`).
- Pembersihan referensi mati & bump minor: Menghapus referensi `game-asset-core` pada `visual-studio` dan `scroll-world`, digantikan status `NOT_APPLICABLE (out of catalog)` sesuai batas routing. `humanizer` diperbarui ke v3.1.0 (`225a6f39ac85`) dengan adaptasi pola 25 & 26 (menulis tentang dokumen itu sendiri dan menjelaskan ulang konteks yang sudah diketahui). `diagram-design` di-pin ke 2.6.51 (`f903933a534b`). Evaluasi upstream `impeccable` v4.5.0 ditunda (deferred) demi menjaga integritas batas catalog freeze dan arsitektur specialist.
- Sumber dan pin diperbarui di `VERSION`, `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `docs/CATALOG-FREEZE.md`, `docs/source-wave.md`, dan `README.md`. Versi produk 0.1.12.
- Release-prep & dokumentasi: Penyelarasan pin upstream Matt Pocock ke `d81f3a1` di seluruh dokumentasi dan third-party notices, pencatatan evaluasi `impeccable` v4.5.0 (deferred) di `docs/source-wave.md`, penambahan ringkasan "What's new (0.1.11 + 0.1.12)" pada `README.md`, verifikasi 25 closed intents, dan penegasan status catalog freeze 65/65 untuk rilis ganda v0.1.11 dan v0.1.12.

## 0.1.11 — 2026-10-04

Wave 0.1.11 body-only ("web_research" data-gathering). Katalog tetap 65 (50 model + 15 manual). Tidak ada pertumbuhan allowlist (`vendor/skill-allowlist.txt` tidak berubah). Tidak ada penambahan atau pensiun skill. Exception 0.1.8 tetap spent.

- Closed intent bertambah 24 → 25: menambahkan `web_research` yang dipetakan ke spesialis `research` (pembaruan badan skill + referensi baru `skills/research/references/web-data.md`).
- `research`: pembaruan deskripsi dan instruksi untuk pengumpulan data web dan media sosial secara read-only. Aturan sumber primer tetap berlaku: setiap klaim wajib merujuk ke sumber primer pemiliknya, output berupa data.
- Ladder backend web data: `WebSearch`/`WebFetch` ringan → ekstraksi artikel Markdown via `crawl4ai` (jika aktif) → structured scraping via `scrapling` (jika aktif) → penangkapan background XHR/JSON via skrip sementara di `/tmp` → feed pengembang/API tanpa konfigurasi via CLI `agent-reach` (pointer host) → platform berotentikasi (kredensial milik pengguna, tidak menyimpan cookie/token) → alur sesi browser persisten via `browser-act`. Pengujian aplikasi UI lokal tetap menggunakan `playwright-qa`.
- Batasan etika & keamanan scraping: bypass stealth dan anti-bot nonaktif secara default (hanya atas persetujuan eksplisit pengguna); patuhi `robots.txt` dan delay sopan; dilarang membobol paywall/login; dilarang mengekstrak cookie dari browser desktop pengguna (`--from-browser` dilarang); dilarang proxy rotasi penipuan.
- Scrapling: dipromosikan menjadi MCP opsional `FOREIGN_ON_DEMAND` lokal stdio (`uvx --from scrapling[ai]==0.4.15 scrapling mcp`). Dikelola lewat CLI `opencode-he scrapling enable` dan `opencode-he scrapling disable`. Tidak divendor ke `lib/`. Mode `--http`, docker bind-all, dan binding `0.0.0.0` dilarang keras dan ditolak oleh `doctor`. Dilarang menjalankan `scrapling install` (karena memanggil `playwright install-deps` dengan sudo).
- Agent-Reach: ditetapkan sebagai `POINTER_ONLY` CLI pada host di bawah `research` (`skills/research/references/web-data.md`). Ditolak sebagai MCP maupun skill. Dilarang menjalankan `agent-reach install --system` (karena memutasi paket sistem dan menyalin skill asing ke direktori konfigurasi).
- Deteksi `doctor`: menambahkan pemeriksaan versi CLI `agent-reach` dan deteksi pembajakan router oleh direktori skill tak terkelola (`FOREIGN_SKILL_SHADOW` untuk `agent-reach` atau `scrapling-official` di `~/.config/opencode/skills/` tanpa `.opencode-highend.json`).
- `whaleyxbt/patchright-enhanced`: ditolak secara tegas di seluruh dokumentasi karena risiko keamanan dan pemeliharaan fork tidak resmi.
- Batasan spesialis tetangga dipertegas: `playwright-qa` dan `browser-act` menegaskan pengumpulan data web/sosial bukan tugas QA aplikasi dan diarahkan ke `research`.
- Sumber dan pin diperbarui di `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `vendor/mcp-policy.json`, `vendor/mcp-wanted.json`, `THIRD_PARTY_NOTICES.md`, dan `docs/source-wave.md`. Versi produk 0.1.11.

## 0.1.10 — 2026-10-03

Rilis ini menutup kerja yang sudah di `main` setelah tag `v0.1.9`. Katalog tetap 65 (50 model + 15 manual). Tidak ada pertumbuhan allowlist. Tidak ada penambahan atau pensiun skill.

- `found-this-design`: badan skill diindeks ke Oversight Supply (template + 32 section) di samping 12 bank universal. Perubahan ini ada di `aa747fa`, setelah tag `v0.1.9`.
- Design Bank bootstrap: pin default pindah ke `OpenCodeHighEnd-DesignBank-v3.zip` (SHA-256 `91d90b4ef9e1af9a44b222171ecb8becac521cfc0814117bdcdc08a54e86df53`). Catatan rilis `v0.1.9` sudah menyebut pin ini, tetapi commit-nya belum masuk tag itu.
- Adaptor indeks Codebase Memory didokumentasikan dua jalur: CLI `opencode-he cbm index .` (`--mode fast`) dan tool MCP `index_repository` (`mode: full`).
- Pin pstack selected skills pindah `60c641e` → `23e4138` (0.15.6) di `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `THIRD_PARTY_NOTICES.md`, dan `docs/source-wave.md`. Badan skill lokal tidak disalin ulang dari upstream. Verification skills tetap menulis `.opencode/skills/verify-*`, bukan `.cursor/skills`. Statusnya adapted-from, bukan byte-identical.
- Ditolak: `poteto-mode`, `/how`, `~/.cursor/rules/pstack-models.mdc`, konektor SaaS asing, dan loop autopilot (`ralph-loop`, `orchestrate`, `continual-learning`).
- Versi produk 0.1.10.

## 0.1.9 — 2026-10-01

Wave 0.1.9 body-only. Katalog tetap 65 (50 model + 15 manual). Tidak ada pertumbuhan allowlist. Tidak ada penambahan atau pensiun skill. Exception 0.1.8 tetap spent.
MERGE: `kaventro/motion-designer` (`0cf0ba92d3db7d8d5ae603a65b56a99a2866311c`, MIT) ke `skills/business-motion-film`.

- `business-motion-film`: Penambahan mode `product-film` untuk membuat film peluncuran (launch film, teaser, product promo) dari UI aplikasi nyata (iOS, macOS/Windows/Linux desktop, Electron/Tauri, web app) di dalam wadah perangkat asli (iPhone / window desktop), bukan iklan komersial abstrak.
- Layar dibangun langsung dari kode sumber atau tangkapan layar terverifikasi di repo. Mockup generik ditolak. Mobile selalu di dalam frame iPhone (dynamic island / status bar); desktop selalu di dalam jendela aplikasi dengan pergerakan kursor yang bermakna.
- Kontrak frame deterministik murni `seek(t)`: dilarang menggunakan timer (`setTimeout`/`setInterval`), `Date.now()`, `Math.random()`, maupun transisi/animasi CSS. Loop timeline harus menutup rapat; frame identik dari arah scrub manapun.
- Beat-map audio: struktur narasi mengikuti tempo (BPM), bar, dan drop musik; aksi kunci mendarat tepat pada drop. Track audio pengguna selalu didahulukan.
- Gerbang 4 still (buka, momen produk utama, drop, frame akhir) wajib disetujui pengguna sebelum build; berhenti jika belum disetujui.
- QA & ledger bukti (`FACT:`): contact sheet + audit daftar kesalahan umum (label terpotong, UI full-bleed, crossfade sembarangan, pointer melayang, klaim tanpa bukti). Pelaporan wajib menyertakan path mp4, status ketersediaan ffmpeg dan Chrome, serta loudness LUFS jika ada audio. Ketiadaan ffmpeg atau Chrome dilaporkan sebagai `NOT_CONFIGURED`, bukan PASS palsu.
- Pipeline render: pintu default tetap `hyperframes` (brag card 18 detik tetap `skills/hyperframes/references/brag.md`). Pipeline render Chrome DevTools upstream hanya digunakan jika diminta secara eksplisit dan Chrome tersedia.
- Model audio/suara upstream (ACE-Step ~11 GB, Chatterbox, Kokoro) adalah `OPTIONAL_POINTER`. Tidak ada pengunduhan model dan script `install.sh` upstream tidak dijalankan. Ketiadaan model = `NOT_CONFIGURED`.
- Peran spesialis tetangga tidak berubah: `id-demo-video` (demo narasi Indonesia), `scroll-craft` (scrollytelling 2D), `scroll-world` (kamera 3D), `emil-design-eng` (motion physics UI; token film memakai token Emil, bukan style kit Meadow/Midnight), `impeccable`, `found-this-design`, `ninerouter`.
- Pin sumber dan lisensi dicatat di `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, `vendor/licenses/KAVENTRO-MOTION-DESIGNER-MIT.txt`, `THIRD_PARTY_NOTICES.md`, dan `docs/source-wave.md`. Versi produk 0.1.9.

## 0.1.8 — 2026-10-01

Unfreeze terbatas 0.1.8. Katalog tetap 65.
RETIRE allowlist name: img2threejs (ilmu Three.js pindah, nama skill dihapus).
ADD model-invoked: business-motion-film (dari echris6/motion-video-kit, MIT, pin commit yang kamu verifikasi di vendor/sources.json + provenance + license-audit + THIRD_PARTY_NOTICES).
ADD model-invoked gateway: ninerouter (first-party stub, bukan salinan 9 file upstream).
RETIRE kedua: prompt-optimizer (tumpang tindih research + humanizer).
Hasil: 50 model + 15 manual = 65. Tidak ada padding.

- Intent `img3d` diganti dua intent tertutup: `launch_film` dan `gateway_llm` (total intent tertutup: 24).
- `business-motion-film`: Iklan, launch film, explainer bisnis, sample reel, dan pitch video. Render tetap lewat `hyperframes`. Pola Three.js product-hero pindah ke referensi `business-motion-film`, bukan skill sendiri. Brag 18s tetap `skills/hyperframes/references/brag.md`. Narasi Indonesia tetap `id-demo-video`.
- `ninerouter`: First-party stub untuk gateway 9Router user via `NINEROUTER_URL` (default `http://127.0.0.1:20128`) dan `NINEROUTER_KEY`. Fail-closed jika URL mengandung `0.0.0.0`. Bukan core MCP; absen gateway menghasilkan `NOT_CONFIGURED`, bukan kegagalan doctor. Capability on-demand, tidak divendor.
- Pensiun `img2threejs` dan `prompt-optimizer`: dihapus dari allowlist, policy, routing, AGENTS.md, docs, dan warehouse inventory. Kritik prompt ditangani `humanizer` (prosa), `research` / Context7 (fakta), `writing-for-agents` (struktur agent), dan `eval-harness` (benchmark pass@k).
- Katalog kembali dibekukan pada 65 (50 model + 15 manual). Versi produk 0.1.8.

## 0.1.7 — 2026-09-28

Unfreeze exception (human-written): catalog grows **62 → 65** to add modern specialists `json-render`, `deck-design`, and `pageindex`. **No twin retired.** No silent padding. UI doctrines remain MERGE’d into `impeccable` / `emil-design-eng`. `react-doctor` stays OPTIONAL_TOOL (not a 4th skill). Closed intent set grows by three: `generative_ui`, `slides_pptx`, `longdoc_nav`.

- Power-up existing specialists (no duplicate UI skill folders):
  - `impeccable/reference/audit.md`: unified React smell checklist and an explicit “when to run react-doctor” OPTIONAL_TOOL door.
  - `impeccable/reference/taste-guard.md`: Delivery Gate liveliness / LCP / leftover-lorem items (net-new only).
  - `emil-design-eng/references/interface-feel.md`: contrast boundaries, non-hue state, container-adaptive density (no duplicate hairline section).
  - `playwright-qa`: evidence ledger + tracing FACT rows; remains door 1; browser-use not vendored.
  - `prototype` + `found-this-design`: schema/JSON UI handoff → `json-render`.
  - `smartdoc`: PPTX generation out of scope → `deck-design`.
  - `research`: long structured docs → `pageindex`; primary-source rule kept.
  - `eval-harness` + `full-audit-keamanan`: `deepteam` OPTIONAL_POINTER tightened (non-vendored, `OPTIONAL_ABSENT` when missing).
- Added three model-invoked skills (catalog 50 model + 15 manual = 65):
  - `json-render` — pin `vercel-labs/json-render@c2600d73` (Apache-2.0). Generative UI from typed catalog/JSON. After tokens/direction or internal schema UI. Never bypass Design Bank for marketing. Jev compose not ported.
  - `deck-design` — pin `carnot-tech/consulting-pptx-skill@f50edac` (MIT). Consulting PPTX / 16:9 HTML decks. Upstream 62-type packs not vendored.
  - `pageindex` — pin `VectifyAI/PageIndex@037a7dba` (MIT). Tree/reasoning long-doc nav. Not Graphiti/Cognee/second CBM. Degrade `NOT_CONFIGURED`. Not a core MCP.
- Re-froze catalog at **65/65**. Product version 0.1.7. No new core MCP. No Jev.

## 0.1.6 — 2026-09-28

- Closed remaining open `UPDATE` dispositions in `docs/source-wave.md` (`scroll-world`, `browser-act`, `impeccable`, `codebase-memory-mcp`):
  - Refreshed `skills/scroll-world/SKILL.md` with upstream seam QA calibration from `oso95/scroll-world@71cc36d` (calibrating seam verification by composition rather than raw PSNR, with ~18–25 dB shimmer tolerance on verified-good builds). Retained boundary (`scroll-craft` = 2D timeline, `scroll-world` = 3D camera flight) and graceful degradation to `NOT_CONFIGURED` when video backends are unconfigured. Pinned `oso95/scroll-world` at `71cc36d3bb15` in `vendor/sources.json`, `vendor/provenance.json`, `vendor/license-audit.json`, and `THIRD_PARTY_NOTICES.md`.
  - Refreshed `skills/browser-act/SKILL.md` to explicitly document the three supported execution modes (`chrome`, `stealth-fresh`, `stealth-fixed`), reaffirmed strict ban on `--type chrome-direct`, confirmed `playwright-qa` as primary default QA adapter (door 1) with `browser-act` as adapter 2 in the 4-door hierarchy, and updated policy strings to OpenCodeHighEnd.
  - Evaluated upstream tip deltas for `pbakaus/impeccable` (`e0881d2...9d715cc`): verified changes pertain to component-review subagents for the proprietary native Rust engine and test suite regexes, with no meaningful craft-floor, taste-guard, or audit changes. Retained pin at `skill-v4.3.1` / `e0881d2de397` without churn.
  - Formally marked `codebase-memory-mcp` disposition DONE (binary pinned to v0.11.0 with SHA-256 verification and automatic `--format json` argument propagation).
- Evaluated and dispositioned 11 starred repositories in `docs/source-wave.md` and `docs/mcp.md`:
  - `genspark-ai/genoffice` (REJECT — multi-app Electron office suite).
  - `hardbeat920/monocode` (REJECT — external desktop host GUI wrapping CLI agents).
  - `CopilotKit/openmuse` (REJECT — full multi-service personal agent application stack).
  - `tt-a1i/archify` (PIN_ONLY — editorial HTML/SVG diagrams already owned by `diagram-design`).
  - `nilbuild/video-demo` (POINTER_ONLY — walkthrough recordings already owned by `id-demo-video` and `hyperframes`).
  - `carnot-tech/consulting-pptx-skill` (POINTER_ONLY — slide factory; document contracts and ingest stay strictly under `smartdoc` and `markitdown`).
  - `blixvip/NullMotion` (POINTER_ONLY — unlicensed launch-film preview; 18s brag launch card pattern already synthesized in `hyperframes/references/brag.md`).
  - `latent-spaces/brag` (DONE — confirmed synthesis into `skills/hyperframes/references/brag.md`).
  - `getzep/graphiti` & `topoteretes/cognee` (REJECT — external graph databases; codebase memory remains strictly `codebase-memory-mcp` v0.11.0; documented in `docs/mcp.md`).
  - `THU-MAIC/OpenMAIC`, `Tencent/WeKnora`, `VectifyAI/PageIndex`, `open-webui/open-webui`, `QwenAudio/qwen-audio-agent` (REJECT — full RAG/apps/modal model platforms).
  - `jakubkrehel/better-interface` (MERGE/DONE — key tactile guideline "No Hairline-Only Affordances" merged in `interface-feel.md`).
- Confirmed zero catalog bloat, maintaining frozen catalog at exactly 62 skills (47 model-invoked, 15 manual slash commands).
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata (`docs/CATALOG-FREEZE.md`), compatibility targets (`docs/compatibility.md`), README front page, and vendor specifications to 0.1.6.

## 0.1.5 — 2026-09-26

- Refocused OpenCodeHighEnd public identity and documentation: neutralized legacy predecessor references across `README.md`, `docs/CATALOG-FREEZE.md`, vendor metadata, and install manifests into a standalone OpenCode 2 runtime overlay.
- Integrated native verification corrective loop:
  - Created `manual-skills/create-verification-skill/references/verification-loop.md` with explicit When, Corrective action, and Evidence ledger protocols (requiring mechanical `FACT:` rows and banning test weakening).
  - Updated `manual-skills/create-verification-skill/SKILL.md` to require executing the corrective loop before claiming PASS and copying it into generated skill failure handling.
  - Added Corrective loop section to `rules/01-verification.md` referencing the verification loop protocol and anti-test-weakening constraints.
  - Added exploratory visual layout shift (CLS) observation recipe in `skills/playwright-qa/references/cls.md` and linked reference in `skills/playwright-qa/SKILL.md` while strictly preserving the 200-newline budget.
  - Documented `/chrome-devtools-axi` diagnostic entry point for observed layout shifts via `127.0.0.1:9223`.
- Added 18-second brag launch video card pattern to HyperFrames:
  - Created `skills/hyperframes/references/brag.md` specifying an 18-second, 60fps, 1080p deterministic video recipe across 4 narrative beats (Hook & Problem, Solution Reveal, Capability Highlight, Call to Action) with local-only assets and target output `brag-output/brag.mp4`.
  - Updated `skills/hyperframes/SKILL.md` and `skills/hyperframes/NOTICE.md` to reference the brag card recipe.
  - Updated `rules/00-routing.md` under `video_html` and `README.md` to route short launch video cards to `hyperframes` via `references/brag.md`.
- Implemented optional Crawl4AI web extraction MCP:
  - Registered `crawl4ai` as an optional `FOREIGN_ON_DEMAND` remote MCP (`http://127.0.0.1:11235/mcp`; `--cloud` using `https://api.crawl4ai.com/mcp` with `{env:CRAWL4AI_KEY}`) via `opencode-he crawl4ai enable [--cloud]` and `opencode-he crawl4ai disable`.
  - Added strict doctor validation in `lib/doctor.py`: enforces `127.0.0.1:11235` local binding, rejects `0.0.0.0` or invalid URLs, prevents raw secret keys on cloud endpoints, and reports `OPTIONAL_ABSENT` when unconfigured.
  - Added CLI options in `lib/cli.py` and enablement handlers in `lib/install.py`.
  - Added doctor unit tests in `tests/test_doctor.py` covering missing, zero-bind, invalid URL, cloud missing token, cloud raw secret, valid local, valid cloud, and enable/disable flows.
  - Documented configuration and boundaries in `docs/mcp.md`, `docs/CATALOG-FREEZE.md`, `docs/source-wave.md`, `docs/troubleshooting.md`, and `README.md` (documenting Scrapling as an unmanaged pointer and retaining Agent-Reach as rejected).
  - Maintained frozen catalog of 62 skills (47 model-invoked, 15 manual slash commands) with zero new skill names. Product version bumped to 0.1.5.

## 0.1.4 — 2026-09-23

- Upgraded `codebase-memory-mcp` pin to v0.11.0 with SHA-256 verified portable tarball download, and added automatic `--format json` argument propagation in `lib/cbm.py` for reliable JSON extraction across project listing and status commands.
- Bumped `shadcn` CLI MCP pin to `4.21.0` across `vendor/mcp-wanted.json`, `vendor/mcp-policy.json`, `lib/install.py`, `rules/00-routing.md`, and doctor tests.
- Refreshed `impeccable` craft floor mechanics in `skills/impeccable/reference/craft-floor.md` from upstream `skill-v4.3.1` / main (tracking caps at -0.04em, single elevation declarations via border or shadow, banning amateur sketch imitation in SVG while preserving geometric linework, subject-world textures, and truth-grounded claims).
- Created `skills/impeccable/reference/email.md` synthesizing email design intelligence and bulletproof rendering (CosmoBlk, email-pro-max, email-skills, agent-skills): 6 committed archetypes (Editorial, Bold-mono, Minimal-lux, Founder letter, Punk/Character, Lookbook), strict presentation tables (or React Email/MJML framework components), inline CSS, 6-digit hex colors, bulletproof table-cell CTA buttons, preheader anti-spill ZWNJ padding, dark mode resilience, and <100KB deliverability constraints.
- Wired email design routing into `skills/impeccable/SKILL.md`, `skills/impeccable/reference/routing.md`, and `skills/impeccable/reference/ui-hub.md` to guarantee web component libraries are never mistakenly installed into email templates.
- Consolidated Emil Kowalski motion doctrines into `skills/emil-design-eng/references/`: created `motion.md` (decision framework, compositor-only properties, production recipes, exit choreography), `apple-principles.md` (WWDC 2018 fluid interfaces, physics-based springs, velocity handoff, momentum projection, materials, SF Pro optical sizing), and `native-motion.md` (eliminating mobile web browser tells, 100dvh, safe area insets, touch-action, overscroll containment, and Expo / React Native Reanimated 3 worklets). Maintained zero new skill names, preserving catalog freeze at 62.
- Refreshed upstream pins in `vendor/sources.json` for `pbakaus/impeccable` (tag `skill-v4.3.1` `cd12f8660e2d` / verified main `e0881d2de397`), `emilkowalski/skills` (`85e8e2363b71`), `microsoft/markitdown` (v0.1.8 `b8f79c57`, PIN_ONLY), and `kunchenguid/axi` (`85a8723276ca`, PIN_ONLY).
- Updated `docs/source-wave.md`, `docs/mcp.md`, `README.md`, and `THIRD_PARTY_NOTICES.md` with complete attribution and license notices for merged doctrines.
- Recorded `CODEBASE_MEMORY_BINARY_CHECKSUM_FAILED` in `docs/troubleshooting.md` (delete download cache and `components/codebase-memory`, then reinstall; v0.11 index rebuilds once). Vendored `vendor/licenses/IMPECCABLE-APACHE2.txt` and `vendor/licenses/EMILKOWALSKI-MIT.txt` so `licenseFile` pins are not empty pointers.
- Pinned `opencode-he markitdown enable` to `uvx --from markitdown-mcp==0.1.8 markitdown-mcp`. Skill body stays PIN_ONLY. `scroll-world` and `browser-act` stay **UPDATE** (not body-refreshed).
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, README front page, and vendor specifications to 0.1.4. Tag `v0.1.3` stays on the previous cut.

## 0.1.3 — 2026-09-23

- Codified the 20-member closed intent classification set in `rules/00-routing.md`, `docs/routing.md`, and `templates/AGENTS.md` (`repo_understand | bug | security | perf | ui_direction | ui_implement | motion | scroll_2d | scroll_3d | img3d | docs | ingest_md | prose | academic | browser_qa | architecture | warehouse | ops_data | video_html | demo_id`).
- Codified artifact-gated specialist handoff graph in `rules/00-routing.md`, `docs/routing.md`, and `docs/architecture.md`, enforcing `found-this-design` must emit `.impeccable/found-this-design.json` before `impeccable` starts.
- Enforced OpenCode 2 host and Code Mode tooling guardrails: session operations strictly use `tools.opencode.session_move` and `tools.opencode.session_rename` (never foreign namespaces); Codebase Memory MCP strictly targets verified repository paths.
- Absorbed offline typed-gate verification patterns (Jev/Canny MERGE) across `rules/01-verification.md` and `rules/decision-log-protocol.md`: assertions in tickets/PRs are hypotheses requiring `FACT:` rows, missing facts halt progress to ask user, and auto-progression requires low blast radius and mechanical proof.
- Merged anti-generic frontend design principles from `anthropics/frontend-design` into `skills/impeccable/reference/taste-guard.md` (no default warm cream ground kit, no terracotta cards, token system before build, domain-grounded typography).
- Merged keyboard navigation flows and reduced-motion fallbacks from `addyosmani/accessibility` into `skills/impeccable/reference/accessibility.md`.
- Merged Apple-grade tactile motion, velocity inheritance, and interruptible springs from `emilkowalski/apple-design` and `wshobson/interaction-design`, along with layered ambient shadows and container-adaptive layouts into `skills/emil-design-eng/references/interface-feel.md`.
- Updated `docs/source-wave.md` with explicit dispositions for upstream wave sources (Canny, Jev demos, typesafe-mcp, Agent-Reach, etc.).
- Explicitly documented `Agent-Reach` and `typesafe-mcp` as REJECTED in `docs/mcp.md` and `docs/source-wave.md`, keeping core MCP servers frozen at `codebase-memory-mcp`, `context7`, and `shadcn`.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.3.

## 0.1.2 — 2026-09-22

- Aligned done-gate vocabulary in `rules/01-verification.md` explicitly requiring `FACT: <outcome>` (blocking) and `JUDGMENT: <assessment>` (advisory) backed by `rules/decision-log-protocol.md`.
- Documented TypeSafe Jev (`jev-mcp`) as SKIPPED in `docs/mcp.md` and `docs/source-wave.md`, noting Canny verification patterns are absorbed into rules and decision logs without external server dependencies.
- Added upstream disposition for `microsoft/playwright-cli` (REFRESH) in `docs/source-wave.md`.
- Documented `confident-ai/deepteam` as an optional external maintainer-side red-team framework pointer in `skills/full-audit-keamanan/SKILL.md` and `skills/eval-harness/SKILL.md` (non-vendored, no extra dependencies).
- Merged interface tactile feel principles (typography stability, hit targets, concentric border radius, layered shadows) from `make-interfaces-feel-better` into `skills/emil-design-eng/references/interface-feel.md`.
- Merged practical WCAG AA checklist (accessible names, focus rings, dialog focus trapping, `aria-invalid`) from `fixing-accessibility` into `skills/impeccable/reference/accessibility.md` and wired into audit and critique workflows.
- Refreshed `skills/playwright-qa` with Playwright CLI diagnostics (`find`, `highlight`, `tracing-start`/`tracing-stop`, `console`) while maintaining strict 4-door browser hierarchy and <=200 line budget.
- Documented `react-doctor` as an optional on-demand tool for React audits in `skills/impeccable/reference/audit.md` and `skills/full-performance-audit/SKILL.md` (no network required at install, zero skill catalog bloat).
- Updated `docs/source-wave.md` with explicit MERGE and OPTIONAL dispositions.
- Hardened done-gate verification pattern across `rules/01-verification.md`, `rules/decision-log-protocol.md`, `manual-skills/decision-log/SKILL.md`, and `templates/AGENTS.md`. Mechanical completion now explicitly requires an evidence ledger (commands, exit codes, artifact paths) with mandatory pointers for done claims and strict separation of blocking `FACT:` proofs from advisory `JUDGMENT:` assessments.
- Fixed Design Bank config resolution path drift in `found-this-design` (`lib.mjs` and `banks.md` now read `~/.config/opencode/highend/config/design-bank.json` and share cache instead of legacy `bestfriend` paths and personal machine folders).
- Aligned documentation across `docs/design-bank.md`, `docs/troubleshooting.md`, and `docs/architecture.md` clarifying the distinction between the 12-bank discovery footprint and 4-catalog bootstrap requirements.
- Formalized specialist architecture as an artifact-gated directed graph and codified harness engineering principles across `rules/00-routing.md` and `docs/architecture.md`.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.2.

## 0.1.1 — 2026-09-19

- Modernized `found-this-design` skill with a local zero-token search engine across 12 universal design banks (Refero, Aura, Motionsites, Scrolltide, Bencho, Layers, Supahero, NavbarGallery, FooterDesign, CtaGallery, 404sDesign, 21st).
- Upgraded Design Bank bootstrap default pin to `OpenCodeHighEnd-DesignBank-v2.zip` (SHA-256 `43b36134c35c476bcdeb633aa55f58ada18a163ade4e867d8fcf9380433b54d2`) with fail-closed checksum verification and Google Drive direct download URL resolution.
- Updated unit test fixtures in `tests/test_design_bootstrap.py` for v2 archive naming, checksums, and version assertions.
- Synchronized release acceptance fixtures (`docs/acceptance.md`), catalog freeze metadata, compatibility targets, and vendor specifications to 0.1.1.

## 0.1.0 — 2026-09-18

First OpenCodeHighEnd release. New product on OpenCode 2. Not OpenCodeBestFriend 1.8.6, not Claude Code, not GrokBuild.

- Catalog inherited frozen from OpenCodeBestFriend 1.8.6 (`67142e4` / PR #29): **62** names (47 model-invoked, 15 manual slash commands).
- Native V2 config: `skills` is an array; MCP lives under `mcp.servers`; every server has `type`; `disabled` replaces V1 `enabled`.
- Installer fails closed on OpenCode 1.x. Gate is major `>= 2`.
- New identity: CLI `opencode-he`, overlay `~/.config/opencode/highend`, share `~/.local/share/opencode-highend`, AGENTS markers `OPENCODEHIGHEND:BEGIN/END`.
- V1 plugins are not copied. `lsp` is not ported. Design Bank / Design V2 / SmartDoc remain user data, never git media.
- Design Bank bootstrap: local valid bank first; `OPENCODE_DESIGN_BANK_URL` + `OPENCODE_DESIGN_BANK_SHA256` (URL without SHA fails closed); default Drive ZIP pin; GitHub `Design-bank.tgz` fallback. Uninstall never deletes `~/Design` or `~/DesignV2`.
- Legacy V1 plugins (`impeccable-live-poll.ts`) quarantined to `~/.local/share/opencode-highend/quarantine/plugins/`; doctor reports `V1_PLUGIN_LEFTOVER`.
- FOREIGN_ON_DEMAND MCP stay enable-gated: serena, stitch, reticle, ui-skills, markitdown; exa is never added/removed/overwritten.
- Retired twins stay retired: `ask-matt`, `grilling`, `wait-what`, `matt-implement`.
- Dropped deprecated `GROK_*` env aliases. Runtime paths never use GrokBuild, `~/.grok`, or `~/.claude`.
