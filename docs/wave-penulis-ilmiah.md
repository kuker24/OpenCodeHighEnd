# Wave 0.1.18 — Penulis Ilmiah Design Stub

Desain dan arsitektur integrasi modul `penulis-ilmiah` ke dalam OpenCodeHighEnd untuk Wave 0.1.18.

## 1. Latar Belakang & Keputusan (Option B)

Modul `penulis-ilmiah` dirancang untuk mendukung penulisan Bahasa Indonesia ilmiah yang benar sesuai dengan kaidah EYD V dan kata baku KBBI untuk esai, skripsi, jurnal SINTA, proposal lomba, dan abstrak jurnal internasional (Scopus) dengan **rujukan terverifikasi** (anti rujukan halu / anti-hallucination).

### Keputusan Unfreeze 65 → 66
Sesuai arahan pengembang (Option B):
- Batas katalog OpenCodeHighEnd di-unfreeze dari **65 menjadi 66 nama** (51 model-invoked di bawah `skills/` + 15 manual di bawah `manual-skills/` / `commands/`).
- Tidak ada *twin* yang dipensiunkan (*no twin retired*), serupa dengan *growth exception* terkelola pada Wave 0.1.7.
- Intent bertambah dari **25 menjadi 26 closed intents** (`penulis_ilmiah`).

---

## 2. Batas Tanggung Jawab Antar-Spesialis (Boundaries)

| Spesialis | Fokus & Tanggung Jawab | Batasan / Jangan Gunakan Untuk |
|---|---|---|
| **`penulis-ilmiah`** | Draf ilmiah Bahasa Indonesia (esai, skripsi, jurnal SINTA, proposal lomba), pemeriksaan kata depan/ejaan EYD V, validasi kata baku KBBI, dan verifikasi sitasi *fail-closed* via MCP. | Bukan untuk peer review metodologi bahasa Inggris murni, bukan pembersih gaya prosa umum, bukan render file. |
| **`academic`** | Tinjauan literatur komprehensif, telaah metodologi, manuskrip IMRaD English-first, telaah sejawat (*peer review*), dan matriks sanggahan revisi. | Bukan untuk pemeriksaan ejaan EYD V atau verifikasi kata baku KBBI. |
| **`humanizer` / `/unslop`** | Pembersihan ciri khas dan klise teks hasil luaran model AI (*AI tells*). | Bukan untuk logika verifikasi sitasi atau ejaan ilmiah formal. |
| **`smartdoc`** | Ingest dokumen (PDF/DOCX), ekstraksi tabel, OCR, dan rendering manuskrip terkunci ke format PDF/DOCX. | Kepemilikan klaim akademik dan konten ilmiah tetap di `penulis-ilmiah` atau `academic`. |
| **`research`** | Penelusuran dokumentasi perpustakaan/API pihak pertama dan data web/sosial. | Bukan untuk penulisan akademik berkaidah EYD. |

---

## 3. Komponen & Arsitektur Sistem

Modul terdiri dari dua komponen utama:

1. **Skill Overlay (`skills/penulis-ilmiah/`)**:
   - `SKILL.md`: Alur kerja draf → `cek_ejaan` & `cek_baku` → `verifikasi_rujukan` → `format_sitasi` → laporan terpisah (dokumen, daftar pustaka, laporan temuan).
   - `references/`: Panduan operasional EYD V (`eyd/`), pasangan kata baku KBBI (`kata_baku.md`), panduan gaya tulisan (`gaya_tulisan.md`), gaya sitasi (`gaya_sitasi.md`), dan frasa terlarang AI (`frasa_terlarang.md`).

2. **MCP Server First-Party (`mcp/penulis-ilmiah/`)**:
   - Runtime: TypeScript (Node.js 20+), transport **stdio**.
   - Dependensi ter-pin: `@modelcontextprotocol/sdk`, `zod`, `citation-js` (dengan plugin CSL APA/IEEE), `tsx`.
   - **5 Tools Wajib**:
     - `cek_ejaan`: Heuristik ejaan EYD V (kata depan *di/ke/dari* menempel vs imbuhan pasif, spasi tanda baca, elipsis, integrasi opsional Hunspell `id_ID`).
     - `cek_baku`: Pemeriksaan kata baku terhadap kamus lokal (≥100 entri), cache lokal (`~/.cache/penulis-ilmiah/kbbi-cache.json` dengan TTL 30 hari), dan lookup KBBI eksternal dengan pembatasan frekuensi (rate limit, default 20/menit).
     - `cari_rujukan`: Pencarian rujukan ke Crossref (polite pool via header `mailto`), OpenAlex, dan Semantic Scholar.
     - `verifikasi_rujukan`: Verifikasi ketat DOI melalui Crossref, pencocokan skor kemiripan judul (ambang 0.85), pencocokan nama keluarga penulis, tahun terbit, dan verifikasi status aktif URL. Status: `VALID`, `TIDAK_COCOK`, `TIDAK_DITEMUKAN`.
     - `format_sitasi`: Pemformatan sitasi APA 7 atau IEEE via `citation-js` dengan proteksi `wajib_terverifikasi` (menolak memformat rujukan yang belum `VALID`).

---

## 4. Integrasi OCH (`FOREIGN_ON_DEMAND`)

Mengikuti pola integrasi Wave 0.1.11 (`scrapling`):
- CLI OCH: `opencode-he penulis-ilmiah enable|disable`.
- Konfigurasi OpenCode 2 (`mcp.servers.penulis-ilmiah`):
  - `type: "local"`
  - `command: ["npx", "tsx", "mcp/penulis-ilmiah/src/index.ts"]`
  - `disabled: false`
  - `environment: {"CROSSREF_MAILTO": "{env:CROSSREF_MAILTO}"}`
- Diagnostik `opencode-he doctor`:
  - Menampilkan `OPTIONAL_ABSENT mcp:penulis-ilmiah` saat belum diaktifkan (status hijau).
  - Menampilkan `CONFIGURED mcp:penulis-ilmiah` saat aktif dengan konfigurasi valid.
  - Menolak dan melaporkan `FAIL` apabila ditemukan binding jaringan publik (`0.0.0.0`), protokol `--http`, atau spesifikasi tak berizin.

---

## 5. Kebijakan Keamanan & Integritas Ilmiah

1. **Anti-Halu Rujukan (*Fail-Closed*)**:
   - Dilarang keras mengarang DOI, judul, penulis, tahun, nomor halaman, atau data statistik.
   - Rujukan yang berstatus `TIDAK_COCOK` atau `TIDAK_DITEMUKAN` tidak boleh dimasukkan ke dalam daftar pustaka akhir.
2. **Tidak Menjanjikan Evasion Plagiarisme**:
   - Modul ini bukan untuk menghindari deteksi Turnitin atau pemalsuan skor similaritas.
3. **Pemberian Atribusi & Hak Cipta**:
   - Tidak melakukan dump kamus KBBI secara massal ke dalam repositori. Hanya lookup per-kata sesuai kebutuhan pengguna.
4. **Privasi & Rahasia**:
   - Tidak ada token API atau kunci rahasia yang disimpan di repositori.
   - Variabel lingkungan yang didukung: `CROSSREF_MAILTO`, `OPENALEX_API_KEY`, `S2_API_KEY`, `KBBI_RATE_PER_MIN`, `PENULIS_CACHE_DIR`.
