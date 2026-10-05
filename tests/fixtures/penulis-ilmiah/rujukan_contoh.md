# Fixture rujukan — asli & palsu

Status resolusi dicek lewat Crossref pada 2026-10-05 (WIB) kecuali dinyatakan lain.

## DOI / metadata ASLI (harus → VALID jika judul selaras)

### R1 — Deep learning

- DOI: `10.1038/nature14539`
- Judul: Deep learning
- Penulis (family): LeCun, Bengio, Hinton
- Tahun: 2015
- Crossref: HTTP 200
- URL DOI: https://doi.org/10.1038/nature14539

### R2 — Optuna

- DOI: `10.1145/3292500.3330701`
- Judul mengandung: Optuna
- Penulis (family): Akiba, Sano, Yanase, …
- Tahun: 2019
- Crossref: HTTP 200
- URL: https://doi.org/10.1145/3292500.3330701

### R3 — Toward unique identifiers (IEEE)

- DOI: `10.1109/5.771073`
- Judul mengandung: Toward unique identifiers
- Penulis (family): Paskin
- Tahun: 1999
- Crossref: HTTP 200

### R4 — Emotions and the big picture (contoh psikologi sosial)

- DOI: `10.1016/j.jesp.2018.05.005`
- Judul mengandung: Emotions and the big picture
- Tahun: 2018
- Crossref: HTTP 200

### R5 — Contoh Crossref “silly string” (tetap DOI nyata terdaftar)

- DOI: `10.5555/12345678`
- Judul: Toward a Unified Theory of High-Energy Metaphysics: Silly String Theory
- Penulis: Carberry
- Catatan: DOI contoh resmi Crossref; boleh dipakai uji teknis, **jangan** dikutip sebagai literatur ilmiah serius di proposal mahasiswa.

## Kasus TIDAK_COCOK

### M1 — DOI benar, judul salah

```json
{
  "doi": "10.1038/nature14539",
  "judul": "A Comprehensive Survey of Blockchain Quantum Farming",
  "tahun": 2015
}
```

Harapan: `TIDAK_COCOK` (judul_score rendah).

## Kasus TIDAK_DITEMUKAN / palsu

### F1 — DOI fiktif

```json
{
  "doi": "10.9999/fake.doi.12345.never.exists",
  "judul": "Advanced Quantum Blockchain AI for Skripsi Otomatis",
  "penulis": ["Fiktif, A.", "Halu, B."],
  "tahun": 2024
}
```

Crossref: HTTP 404 (dicek 2026-10-05).

### F2 — Tanpa DOI, metadata halu

```json
{
  "judul": "Superinteligensi Bahasa Indonesia untuk Segala Jurnal SINTA Level 10",
  "penulis": ["Anonimus Quack"],
  "tahun": 2026,
  "url": "https://example.invalid/paper-halu-xyz"
}
```

Harapan: `TIDAK_DITEMUKAN` (dan/atau `url_hidup=false`).

### F3 — DOI format menyerupai arXiv palsu

```json
{
  "doi": "10.48550/arXiv.9999.99999",
  "judul": "We Trained a Model on Nothing and Got 100% Accuracy",
  "tahun": 2025
}
```

Harapan: bukan `VALID` (404 atau tidak cocok). Jika upstream berubah, catat di laporan tes.

## Aturan pemakaian di dokumen

Semua item F* dan M1 **dilarang** masuk daftar pustaka akhir. Hanya R1–R4 (dan DOI VALID lain hasil `verifikasi_rujukan`) yang boleh.
