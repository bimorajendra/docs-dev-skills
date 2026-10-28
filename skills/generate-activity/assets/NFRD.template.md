# Dokumen Kebutuhan Non-Fungsional (NFRD) — <Nama Proyek>

| Atribut | Isi |
|---|---|
| ID dokumen | DOC-NFRD-001 |
| Versi | 0.1 |
| Status | Draft |
| Tanggal | YYYY-MM-DD |
| Penulis | AI agent (draf, perlu ditinjau manusia) |
| Pemilik dokumen | Belum ditetapkan |
| Dokumen terkait | 00-activity-list, FRD, pertanyaan-terbuka |

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

> Fill: the NFRD sets measurable quality targets for the system and how each is verified.

### 1.2 Ruang Lingkup

> Fill: the qualities established by source or answers and the remaining applicability/target questions. Refer to FRD for functional capabilities and acceptance criteria. Missing information remains open until clarified.

### 1.3 Referensi

> Fill: ISO/IEC 25030 (quality requirements), ISO/IEC 25010:2023 (quality model), ISO/IEC 25023 (quality measures), OWASP ASVS, WCAG 2.2, Google SRE (SLI/SLO), and the source.

### 1.4 Konvensi Penulisan

> Fill: ID format NFR-KKK-nn; columns Ukuran, Target, Verif., Sumber, Basis; the TBD marker inside backticks; definitions of terms are in FRD 1.4; the requirement checklist is in FRD Lampiran A.

## 2. Kerangka Mutu

### 2.1 Model Mutu ISO/IEC 25010:2023

> Fill: the nine characteristics used as the frame (Functional Suitability, Performance Efficiency, Compatibility, Interaction Capability, Reliability, Security, Maintainability, Flexibility, Safety).

### 2.2 Ukuran dan Target

> Fill: distinguish established values, estimates and unanswered targets. Ask about unknown audience, usage conditions and quality expectations needed to verify the actual activities. Never turn an estimated account total into concurrent load or invent response times. Set numeric targets and standards levels only after explicit confirmation; write plain business questions when the user has no technical target yet.

## 3. Kebutuhan Mutu per Karakteristik

> Fill: review all nine subsections. Preserve supported rows; for unknown applicability or targets write "Bergantung OQ-nn" and explain the activity-specific uncertainty. "Tidak berlaku" or "Tidak ada kebutuhan" requires an explicit user decision and its answered OQ. Do not substitute "the source does not say" for clarification. There is no fixed question count.
> Columns: ID | Sub-karakteristik | Pernyataan | Ukuran | Target | Sumber | Basis | Verif.

### 3.1 Functional Suitability

### 3.2 Performance Efficiency

### 3.3 Compatibility

### 3.4 Interaction Capability

### 3.5 Reliability

### 3.6 Security

### 3.7 Maintainability

### 3.8 Flexibility

### 3.9 Safety

## 4. Kepatuhan dan Regulasi

> Fill: policies or regulations established by the source or confirmed answers. If applicability is unknown, ask the user and cite the OQ; do not invent a regulation or conclude that none applies from silence.

## 5. Keterlacakan

> Fill: table `Aktivitas | NFR`, one row for each AL that has an NFR, IDs one by one. The full matrix is generated into traceability.md.

## 6. Pertanyaan Terbuka

> Fill: table `ID | Pertanyaan` of the open questions that touch this document, each as a short title (under 60 characters).
