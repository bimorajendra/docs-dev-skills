# Kasus Uji (Test Case) — <Nama Proyek>

| Atribut | Isi |
|---|---|
| ID dokumen | DOC-TC-001 |
| Versi | 0.1 |
| Status | Draft |
| Tanggal | YYYY-MM-DD |
| Penulis | AI agent (draf, perlu ditinjau manusia) |
| Pemilik dokumen | Belum ditetapkan |
| Dokumen terkait | FRD, NFRD, FSD |

## Riwayat Revisi

| Versi | Tanggal | Penulis | Perubahan |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | AI agent | Draf awal dari FRD, NFRD, dan FSD |

## Persetujuan

| Nama | Peran | Tanda tangan | Tanggal |
|---|---|---|---|
| | | | |

## Daftar Isi

> Fill: written by the validator (`--toc`). Leave this line until then.

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

> Fill: the document lists test cases that check every acceptance criterion, business rule, validation and exception.

### 1.2 Ruang Lingkup

> Fill: what is tested (the modules and the NFRs with a measurable target) and what is not.

### 1.3 Konvensi Penulisan

> Fill: ID format TC-nnn; the columns; Jenis (Positif, Negatif, Non-fungsional); that no priority column exists because the source gives none; the TBD marker inside backticks.

### 1.4 Referensi

> Fill: FRD, NFRD, FSD, and ISO/IEC/IEEE 29119-3 (test case specification: identifier, objective, traceability, preconditions, inputs, expected results).

## 2. Strategi Pengujian

### 2.1 Pendekatan

> Fill: how the cases are derived: each acceptance criterion gives a Positif case; each business rule that restricts gives a Negatif case; each validation gives a Negatif case; each exception gives one case; each NFR with a numeric or listed Target gives a Non-fungsional case.

### 2.2 Lingkungan dan Data Uji

> Fill: test environment and data supplied by the source or conversation. If unspecified, write "Belum ditetapkan untuk pelaksanaan uji". Inputs can be described by condition; do not invent values.

### 2.3 Kriteria Lulus dan Gagal

> Fill: a case passes when the actual result equals the expected result; otherwise it fails.

## 3. Kasus Uji per Modul

> Fill: one subsection per module (same number, name and `Sumber aktivitas` line as the FRD and FSD). Each holds one table.
> Columns: ID | Tujuan | Rujukan | Prakondisi | Input dan Langkah | Hasil yang Diharapkan | Jenis

<!-- ulang:mulai -->
### 3.n Modul <Nama>

Sumber aktivitas: AL-001.

| ID | Tujuan | Rujukan | Prakondisi | Input dan Langkah | Hasil yang Diharapkan | Jenis |
|---|---|---|---|---|---|---|
| TC-001 | <apa yang diperiksa> | FR-001, BR-01 | <keadaan awal> | <data menurut kondisi; langkah bernomor dipisah `<br>`> | <hasil yang dapat diamati> | Positif |
<!-- ulang:selesai -->

## 4. Kasus Uji Non-Fungsional

> Fill: one table with the same columns, for NFRs whose Target is a number or a complete list. Rujukan holds NFR IDs. Write "Tidak ada" if no NFR qualifies.

## 5. Cakupan

> Fill: table `Butir | Kasus Uji` with one row per FR, BR, VAL and EXC (ID in the first cell, TC IDs one by one in the second). Every item has at least one case.

## 6. Pertanyaan Terbuka

> Fill: table `ID | Pertanyaan` of the open questions that touch this document, each as a short title (under 60 characters).
