# FSD guide

Basis (structure only; the vendor templates vary by company and are not reproduced):
- SAP functional specification (WRICEF style): business requirement, process flow, functional description, assumptions and dependencies, authorizations, error handling, test conditions.
- Microsoft Dynamics 365 functional design document (Microsoft Learn pattern "Create a functional and technical design document"): introduction with abbreviations and an index of symbols for process-flow diagrams, scope, organisation structure and functional responsibilities, description of each business process with a flow diagram and text, security requirements by role, reporting, integration, migration.
- IIBA BABOK: business rules, process models, roles and permissions matrix.
- Smartsheet functional specification: overview, scope, requirements, acceptance criteria.
- Use case specification (Cockburn style, as in the FSD template supplied by the user): per use case a name, goal in context, pre-condition, successful and failed end condition, primary actor, trigger, main flow as actor action and system response, and extensions as branching actions; plus a use case diagram and an activity diagram per module. A use case here comes from an activity; test cases are a separate later artifact (see `test-case-guide.md`).

Mapping to FSD chapters:

| FSD chapter | Comes from |
|---|---|
| 1.3 Konvensi dan simbol | Dynamics 365 introduction and symbol index |
| 2.2 Struktur organisasi dan tanggung jawab | Dynamics 365 organisation and responsibilities |
| 2.5 Daftar Use Case | Use case table of the FSD template (Definisi Use Case) |
| 3: Diagram aktivitas per use case | SAP process flow; Dynamics 365 business process description; activity diagram of the FSD template |
| 3: Skenario use case | Use case scenario table and use case diagram of the FSD template |
| 3: Input, Output | SAP functional description |
| 3: Aturan bisnis | IIBA business rules |
| 3: Validasi, Penanganan pengecualian | SAP error handling |
| 3: Aktor dan hak akses; 4.1 | Dynamics 365 security requirements; IIBA roles and permissions |
| 4.4 Laporan, 4.5 Integrasi, 4.6 Migrasi | Dynamics 365 reporting, integration, migration |
| 4.7 Desain Antarmuka | Desain Interface (UI) chapter of the FSD template |
| 4.8 Keamanan Sistem | Keamanan Sistem chapter of the FSD template |

## Inputs

`docs/00-activity-list.md`, `FRD.md`, `NFRD.md`, `pertanyaan-terbuka.md` and the source file. Read `references/conventions.md` first.

Facts come from the FRD, the NFRD, the Activity List text and answers already logged in `pertanyaan-terbuka.md` (conventions section 5a). This stage asks the user nothing and registers no new OQ: a TBD is written only with the ID of an OQ that already exists. If no such OQ exists, leave the item out.

## Where a condition is written (BR, VAL or EXC)

A condition appears once; the other tables cite it by ID.

| Type | Use for | Example |
|---|---|---|
| BR | a business decision: who, which, how many, in what priority | "memprioritaskan supplier yang disetujui" |
| VAL | a check on the content of one data item | "formulir lengkap: nomor, tanggal, ..." |
| EXC | what happens when the normal path cannot continue, as the source states it | "apabila supplier tidak dapat memenuhi kebutuhan, cari supplier baru" |

## Procedure

1. **Use the shared module list.** Take every `### 3.n Modul <Nama>` and its `Sumber aktivitas` line from the FRD. Do not change modules in the FSD alone. Keep the FRD's grouping as it is; a grouping that looks wrong is reported for `generate-activity`, never changed here. Cite the OQ of a grouping the register already marks provisional.

2. **Chapters 1 and 2.** In 1.3 define `UC-nnn`, skenario use case and diagram use case. 2.1 is one Mermaid flow, one node per AL arranged in source order. Draw execution edges only where the source or a confirmed reply supports that sequence; source numbering alone does not establish a handoff. Leave out a connection the source does not support. 2.2 is built from the Aktor column and confirmed actor answers, retaining OQ provenance. 2.3 lists each module with its ALs and FRs, IDs one by one. 2.5 lists the use cases: exactly one `UC-nnn` per AL, numbered in AL order, never renumbered. The Use Case cell is the activity's goal as a short verb phrase in the source's words, Aktor utama is the first actor of the AL (`Pelaku (aktor tidak disebut SOP)` when the source names none, as in 2.2), Sumber is that one AL. Do not merge or split activities into use cases; an activity that seems to hold two goals stays one use case and is reported for `generate-activity`.

3. **Each module, in this order, all 11 parts.**
   - **Tujuan dan lingkup modul**: two sentences in the source's words.
   - **Aktor dan hak akses**: a bullet list of the actors of the module's ALs (conventions section 6a), each with what the AL says they do and the AL ID at the end of the line. A right is written only if the source or a confirmed answer states it ("persetujuan oleh X" gives X the right to approve). A missing right stays unwritten.
   - **Prasyarat dan pemicu**: what the AL's wording requires beforehand and what starts it ("apabila ...").
   - **Skenario use case**: it only arranges what the parts below already say, so write those first, then place this part here. It opens with a sentence and one Mermaid flowchart (diagram use case): the actors of the module on the left, one node `UC-nnn <nama>` per use case, an edge from each actor to the use cases it performs. Then one block per use case in AL order, opening with the line `**UC-nnn — <nama>**`:
     - A sentence on what the use case achieves, then `Atribut | Isi` with Tujuan (the goal in the source's words), Prasyarat and Pemicu (from Prasyarat dan pemicu, per AL), Kondisi akhir berhasil (from Output), Kondisi akhir gagal (what the EXC and VAL of the AL say happens, in a sentence with the OQ; "Belum disebut dalam SOP" when the AL has none), Aktor utama.
     - `Diagram aktivitas:` a Mermaid flowchart of this use case alone: `Mulai`, one node per action, a labelled edge to a side node for each extension (the label is the condition, the side node says what happens or "Penanganan belum ditentukan (OQ-nn)"), `Selesai`. Every use case has its own diagram, with no exception, including one-step use cases.
     - `Alur utama:` a lead sentence and `No | Aksi Aktor | Respons Sistem | Rujukan`, one row per action of the AL in the order the AL states, numbered from 1 inside the use case. Aksi Aktor names the actor and the action ("CS memverifikasi nama, nomor order, dan tanggal transaksi"). Respons Sistem is a plain sentence on what the system stores, shows or makes possible, taken from the FR, VAL or EXC the step belongs to ("Sistem menyimpan keluhan sebagai tiket"). Never write "sesuai kriteria penerimaan FR-nnn" in place of the sentence, and never write a system behaviour that no FR, VAL or EXC states. When the FR gives no observable result yet, write that plainly ("Hasil yang terlihat di sistem belum ditentukan") with the TBD marker of the OQ that exists. Rujukan lists the IDs behind the row.
     - `Ekstensi:` one bullet per EXC and VAL of the AL: `- E1, pada langkah 2: Jika data tidak lolos verifikasi, <what happens> (Rujukan: EXC-01, VAL-01)`. Write "Tidak ada." when the AL has neither.
     - The block as a whole cites every FR, BR, VAL and EXC whose Sumber includes its AL, IDs one by one; the validator checks this.
   - **Input**: a lead sentence, then the data the AL names or lists (for example the fields of a form), one row each. `Wajib` is `Ya` only if the AL says the item is required or "meliputi" it; otherwise write `Belum ditentukan`, and put one line `[TBD: kolom wajib, lihat OQ-nn]` above the table.
   - **Output**: a lead sentence, then the records, documents or results the AL produces.
   - **Aturan bisnis**: a lead sentence, then each decision, minimum, priority or choice the AL states. One rule per row, in the source's words. IDs BR-nn run across the whole document.
   - **Validasi**: a lead sentence, then the checks on a data item that the AL itself states (completeness of a listed form). A check the source does not state is not written. IDs VAL-nn.
   - **Penanganan pengecualian**: a lead sentence, then only the conditions the source states that stop or change the normal path, and what the source says happens ("apabila ...", "satu jika tidak memungkinkan"). Basis is `Eksplisit` and Sumber cites the AL. Do not write an EXC for the opposite of an "apabila" or for a branch the source leaves open. For a branch the register already has an OQ for, write `[TBD: <specific unhandled condition>, lihat OQ-nn]`; for a branch with no OQ write nothing. IDs EXC-nn.
   - **Keterlacakan**: three lines as in the template.
   - **Pertanyaan terbuka**: the OQs cited in this module, as short titles.

4. **Row columns.** Every row of the Input, Output, BR, VAL and EXC tables in chapter 3 ends with `Sumber | Basis`. Sumber lists AL IDs of this module only. Basis per conventions section 4.

5. **Chapter 4.** Fill from what the modules already say; add nothing new. Rows here may cite ALs of several modules. The status model has one stateDiagram per main record (conventions: the record the AL texts create or change in turn); state names are one word without spaces, edges are labelled with plain text, and the names are Turunan. 4.7 Desain Antarmuka holds only interface designs the user supplied, mapped to `UC-nnn`; otherwise "Tidak disebut sumber". 4.8 Keamanan Sistem lists the security functions the NFRD (`NFR-SEC-nn`), 4.1 or the source state, citing them; it never adds login, session or password rules the input does not contain.

6. **Appendices**, then the Daftar Isi. Lampiran A is the AL to module table, Lampiran B the open questions that touch the document, Lampiran C the notes for `generate-activity`: mapping remarks (an AL that bundles two actions, a grouping that looks coarse) and facts the FSD needed that neither the input nor an OQ gives. Anything that talks about the document or its gaps goes there, never into chapters 1 to 4.

7. **No duplication.** Do not copy FR statements or acceptance criteria into the FSD; cite the FR ID. Do not copy NFR targets; cite the NFR ID. If a sentence would be identical to one in the FRD, delete it.

Done when every module has all 11 parts, every AL has one UC in 2.5 and one scenario with its own activity diagram, every BR, VAL and EXC has a Sumber and a Basis, and the validator shows no error for FSD.

## Writing for people

The FSD is read by business people before developers. Check each module against these rules, then run the humanizer pass.

- Write whole sentences in plain Indonesian that someone who never saw the FRD can follow. Name the actor, use active voice, one idea per sentence.
- IDs and source tags (AL, FR, BR, VAL, EXC, OQ) close a line or sit in the last column. They are never part of the sentence's grammar.
- Every table has one lead sentence above it. Two tables never follow each other with only a label between them. A table of three short rows or fewer with two columns becomes a bullet list.
- Facts about the document itself (mapping remarks, missing facts, who still has to decide) belong in Lampiran C, not in the chapters.
- Humanizer pass (skill `humanizer`, Indonesian section): after the draft is complete, edit the prose cells and paragraphs once. Remove "bukan hanya X, tetapi Y", one-line closers, stacked qualifiers, forced triads, inflated words (krusial, signifikan, komprehensif, holistik, memfasilitasi), "merupakan" where "adalah" works, dashes as connectors, bold decoration and any text addressed to the reader of a chat. Do not touch IDs, TBD markers, column names, Mermaid code or words quoted from the source, and do not add or drop a fact.

## Self-review

For each BR, VAL, EXC and scenario row ask: can I point at the source words or a confirmed answer, with an AL link? If not, delete it.
