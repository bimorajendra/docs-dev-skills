# Dokumen Kebutuhan Fungsional (FRD) — <Nama Proyek>

| Atribut | Isi |
|---|---|
| ID dokumen | DOC-FRD-001 |
| Versi | 0.1 |
| Status | Draft |
| Tanggal | YYYY-MM-DD |
| Penulis | AI agent (draf, perlu ditinjau manusia) |
| Pemilik dokumen | Belum ditetapkan |
| Dokumen terkait | 00-activity-list, NFRD, pertanyaan-terbuka |

## Riwayat Revisi

| Versi | Tanggal | Penulis | Perubahan |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | AI agent | Draf awal dari sumber |

## Persetujuan

| Nama | Peran | Tanda tangan | Tanggal |
|---|---|---|---|
| | | | |

## Daftar Isi

> Fill: written by the validator (`--toc`). Leave this line until then.

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

> Fill: one paragraph. State the functional capabilities and observable acceptance criteria, keeping them separate from detailed solution design.

### 1.2 Ruang Lingkup

> Fill: the source activities covered, what remains provisional, and which quality requirements belong to NFRD.

### 1.3 Pemangku Kepentingan dan Aktor

> Fill: table `Aktor | Peran dalam sumber`. Only roles named in the source. Add external parties in a separate table `Pihak luar | Peran`.

### 1.4 Definisi dan Singkatan

> Fill: table `Istilah | Arti`. Terms and abbreviations used in the source, plus `Pelaku` (the person who does an activity whose actor the source does not name; see OQ). Other documents cite this section.

### 1.5 Referensi

> Fill: the source (title and version as the source gives them; write "Tidak disebut sumber" if it gives none), ISO/IEC/IEEE 29148, Volere, NASA SE Handbook appendix C.

### 1.6 Konvensi Penulisan

> Fill: ID format FR-nnn; the EARS pattern; meaning of columns Sumber, Alasan, Kriteria Penerimaan, Basis (Eksplisit/Turunan), Verif. (U/D/I/A); the TBD marker written inside backticks; that no priority column exists because the source gives no priority.

## 2. Gambaran Umum

### 2.1 Latar Belakang dan Tujuan Bisnis

> Fill: purpose of the process as the source states it. Quote the source; add nothing. If the source states no purpose, write "Tidak disebut sumber".

### 2.2 Ringkasan Proses

> Fill: one paragraph summarizing the source-supported business activities and their purpose. Do not invent execution order.

### 2.3 Batasan

> Fill: constraints the source states (legal, organisational, technology). Write "Tidak disebut sumber" if none.

### 2.4 Asumsi dan Ketergantungan

> Fill: table `Jenis | Isi | Dampak jika salah`. Include only actual unresolved assumptions and their OQs. Write "Tidak ada" if none; no boundary question is required when the source is clear.

## 3. Kebutuhan Fungsional

> Fill: one group per module (rule in conventions section 7). Under each heading, the line `Sumber aktivitas: AL-...` and then one table.

<!-- ulang:mulai -->
### 3.n Modul <Nama>

Sumber aktivitas: AL-001.

| ID | Pernyataan | Sumber | Alasan | Kriteria Penerimaan | Basis | Verif. |
|---|---|---|---|---|---|---|
| FR-001 | Sistem harus memungkinkan <aktor> <kata kerja> <objek>. | AL-001 | <tujuan dari sumber atau -> | Diberikan <kondisi>, ketika <aksi>, maka <hasil yang dapat diamati>. | Eksplisit | U |
<!-- ulang:selesai -->

## 4. Keterlacakan

> Fill: table `Aktivitas | Modul | FR` with one row per AL; each AL's FR IDs listed one by one; the Modul cell holds the module number (for example `3.1`). The full matrix is generated into traceability.md.

## 5. Pertanyaan Terbuka

> Fill: table `ID | Pertanyaan` of the open questions that touch this document, each as a short title (under 60 characters). The full text lives in pertanyaan-terbuka.md.

## Lampiran A. Kriteria Mutu Kebutuhan

> Fill: reviewer checklist, one row per characteristic: Necessary, Appropriate, Unambiguous, Complete, Singular, Feasible, Verifiable, Correct, Conforming (ISO/IEC/IEEE 29148), each with its test question.
