# Spesifikasi Fungsional (FSD) — <Nama Proyek>

| Atribut | Isi |
|---|---|
| ID dokumen | DOC-FSD-001 |
| Versi | 0.1 |
| Status | Draft |
| Tanggal | YYYY-MM-DD |
| Penulis | AI agent (draf, perlu ditinjau manusia) |
| Pemilik dokumen | Belum ditetapkan |
| Klasifikasi | Belum ditetapkan |
| Dokumen terkait | FRD, NFRD, TEST-CASE |

## Riwayat Revisi

| Versi | Tanggal | Penulis | Perubahan |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | AI agent | Draf awal dari FRD dan NFRD |

## Persetujuan

| Nama | Peran | Tanda tangan | Tanggal |
|---|---|---|---|
| | | | |

## Daftar Isi

> Fill: written by the validator (`--toc`). Leave this line until then.

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

> Fill: one paragraph. The FSD explains HOW each module works: use cases with their flows, input, output, business rules, validation, exceptions. Business readers approve behaviour from it; developers build from it. Add a short reading guide: chapter 3 is read use case by use case, the tables at the end of each module are reference, and the traceability, open questions and mapping notes are in the appendices (Lampiran).

### 1.2 Ruang Lingkup

> Fill: the modules covered (same modules as the FRD) and that every activity has one use case with a scenario. What it leaves to the FRD (capability statements, acceptance criteria), the NFRD (quality targets) and TEST-CASE (concrete cases).

### 1.3 Konvensi Penulisan dan Simbol Diagram

> Fill: ID formats BR-nn, VAL-nn, EXC-nn; the columns Sumber and Basis; the TBD marker inside backticks; Mermaid conventions (flowchart labels in double quotes; a rounded node is start or end, a diamond is a decision, a node "Tidak diatur sumber (OQ-nn)" marks a branch the source does not define; state diagrams use one-word state names and plain-text edge labels); the legend of symbols. Definitions of `UC-nnn` (one use case per activity), skenario use case (attributes, main flow, extensions), diagram use case (per module) and diagram aktivitas (one per use case).

### 1.4 Referensi

> Fill: FRD, NFRD, the source, and the guides used (SAP functional specification structure, Microsoft Dynamics 365 functional design document, IIBA BABOK, Smartsheet functional specification). Definitions of terms: see FRD 1.4.

## 2. Gambaran Umum Proses

### 2.1 Alur Proses Bisnis Menyeluruh

> Fill: one Mermaid flow of the process, one node per AL arranged in source order. Execution edges require support from the source or a confirmed answer; do not assume that numbering establishes execution order. No narrative (the FRD 2.2 holds it).

### 2.2 Struktur Organisasi dan Tanggung Jawab Fungsional

> Fill: table `Peran | Aktivitas yang dilakukan | Modul`, built from the Activity List and confirmed actor answers. Cite the OQ for roles an answer confirmed; preserve verbatim source extraction.

### 2.3 Peta Modul

> Fill: table `Modul | Sumber AL | FR` with one row per module; the Modul cell starts with the module number (`3.1 Modul <Nama>`), IDs one by one.

### 2.4 Asumsi dan Ketergantungan

> Fill: table `Jenis | Isi | Dampak jika salah`. Only what affects functional behaviour. Write "Tidak ada" if none.

### 2.5 Daftar Use Case

> Fill: table `ID | Use Case | Modul | Aktor utama | Sumber`, one row per activity (one use case per AL), IDs `UC-001` upward in AL order. The Use Case cell is the activity's goal as a short verb phrase in the source's words; Modul starts with the module number (`3.1`); Sumber is that one AL; Aktor utama is the first actor of the AL, or `Pelaku (aktor tidak disebut SOP)`.

## 3. Spesifikasi Fungsional per Modul

> Fill: one subsection per module of the FRD (same number, same name, same `Sumber aktivitas` line). All 11 parts are required, in this order: the use case scenarios come first because a reader needs them first, the data and rule tables after them as reference. A part with nothing to say states "Tidak ada" or "Belum ditentukan, lihat OQ-nn" and why. Every rule table row carries Sumber (AL IDs of this module) and Basis. Every table has one lead sentence above it. Do not restate FR statements; cite FR IDs.

<!-- ulang:mulai -->
### 3.n Modul <Nama>

Sumber aktivitas: AL-001.

#### Tujuan dan lingkup modul

> Fill: two sentences at most, in the source's words.

#### Aktor dan hak akses

> Fill: a bullet list, one line per actor of this module's ALs: `- <Aktor>: what the AL says the actor does (AL-nnn).` No table. A right the source does not state stays unwritten.

#### Prasyarat dan pemicu

> Fill: what must exist before the module runs, and what starts it, as the AL states.

#### Skenario use case

> Fill: one sentence that introduces the use cases of this module, then one Mermaid flowchart (the diagram use case): actors on the left, one node `UC-nnn <nama>` per use case, an edge from each actor to the use cases it performs. Then one block per use case, in AL order, starting with the line `**UC-nnn — <nama>**` (the same name as in 2.5), followed by:
> 1. a sentence on what the use case achieves, then table `Atribut | Isi` with the rows Tujuan, Prasyarat, Kondisi akhir berhasil, Kondisi akhir gagal, Aktor utama, Pemicu;
> 2. the line `Diagram aktivitas:` and one Mermaid flowchart of this use case alone: start, one node per step, a labelled branch for each extension, end. Every use case has one;
> 3. the line `Alur utama:`, a lead sentence, and table `No | Aksi Aktor | Respons Sistem | Rujukan`, one row per action of that AL in the order the AL gives them (No counts from 1 inside the use case). Respons Sistem is a plain sentence about what the system does or shows;
> 4. the line `Ekstensi:` and a bullet list `- E1, pada langkah n: Jika <kondisi>, <apa yang terjadi> (Rujukan: EXC-nn)` with one bullet per EXC and VAL of that AL, or the words "Tidak ada.".
> Values come only from this module's other parts (rules in `references/fsd-guide.md`); the block cites every FR, BR, VAL and EXC of its AL.

#### Input

> Fill: one lead sentence, then table `Data | Wajib | Keterangan | Sumber | Basis`. Wajib is `Ya` only if the activity says the item is required; otherwise `Belum ditentukan`, with one line `[TBD: kolom wajib, lihat OQ-nn]` above the table.

#### Output

> Fill: one lead sentence, then table `Keluaran | Keterangan | Sumber | Basis`.

#### Aturan bisnis

> Fill: one lead sentence, then table `ID | Aturan | Sumber | Basis`, IDs BR-nn. One rule per row, in the source's words.

#### Validasi

> Fill: one lead sentence, then table `ID | Data | Aturan Validasi | Tindakan Sistem | Sumber | Basis`, IDs VAL-nn. Write "Tidak ada" and why when the module has none.

#### Penanganan pengecualian

> Fill: one lead sentence, then table `ID | Kondisi | Tindakan Sistem | Sumber | Basis`, IDs EXC-nn. Only conditions the source states that stop or change the normal path, with what the source says happens; Basis is Eksplisit. For branches the source leaves open write one line `[TBD: penanganan kondisi yang tidak diatur sumber, lihat OQ-nn]` instead of rows.

#### Keterlacakan

> Fill: three lines: `- Sumber AL: ...`, `- FR: ...`, `- NFR: ...`. The FR line lists every FR of the same FRD module, IDs one by one. Write `- NFR: -` if none apply.

#### Pertanyaan terbuka

> Fill: the OQs touching this module, or "Tidak ada".
<!-- ulang:selesai -->

## 4. Kebutuhan Lintas Modul

### 4.1 Peran dan Hak Akses

> Fill: table `Peran | Modul | Hak | Sumber | Basis`. Use source-supported or confirmed rights. Leave other rights unspecified.

### 4.2 Model Status

> Fill: statuses of the main record and their transitions (Mermaid stateDiagram plus a table `Dari | Ke | Pemicu | Pelaku | Sumber | Basis`). Statuses the source does not name are Turunan.

### 4.3 Model Data Konseptual

> Fill: entities and attributes at business level, from the Input and Output tables (table `Entitas | Atribut | Sumber`). No database schema.

### 4.4 Laporan dan Keluaran

> Fill: reports or documents the source says are produced. Write "Tidak disebut sumber" if none.

### 4.5 Integrasi dan Antarmuka Eksternal

> Fill: other systems or parties the source names and what is exchanged. Write "Tidak disebut sumber" if none.

### 4.6 Migrasi Data

> Fill: data to bring in from older systems when the source or conversation mentions migration. Otherwise write "Tidak disebut sumber". Do not create a migration question.

### 4.7 Desain Antarmuka

> Fill: only interface designs the user supplies (a file, link or description), as table `Use Case | Layar atau menu | Rujukan desain`. Otherwise write "Tidak disebut sumber". Never invent screens, fields or layouts.

### 4.8 Keamanan Sistem

> Fill: table `Fungsi keamanan | Rujukan | Keterangan` for login and logout, automatic logout, password policy, access levels and activity log, but only those the NFRD (`NFR-SEC-nn`), 4.1 or the source state; Rujukan cites the NFR ID or 4.1 and Keterangan never repeats an NFR target. Write "Tidak disebut sumber" for a function nothing states. A missing security decision is an OQ in the NFRD, not an invented function.

## Lampiran A. Keterlacakan

> Fill: a lead sentence, then table `Aktivitas | Modul`, one row per AL. The full matrix is generated into traceability.md.

## Lampiran B. Pertanyaan Terbuka

> Fill: a lead sentence, then table `ID | Pertanyaan` of the open questions that touch this document, each as a short title (under 60 characters).

## Lampiran C. Catatan untuk Tahap Requirement

> Fill: two short bullet lists for `generate-activity`, kept out of the chapters above. "Catatan pemetaan": places where the FRD mapping looks wrong or too coarse, with the AL and FR IDs. "Fakta yang belum tersedia": facts the FSD needed but the input does not give and no OQ covers, one line each. Write "Tidak ada." under a list that is empty. Nothing here is an OQ and nothing here is asked of the user.
