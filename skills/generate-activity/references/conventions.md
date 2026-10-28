# Conventions

Conventions for the Activity List, FRD, NFRD and clarification register. Apply these within the requirements stage; detailed solution design is outside this skill.

## 1. Scope

- Input: an SOP, Activity List or informal application brief. Output: Indonesian documents in `docs/`. Preserve numbered items verbatim; for narrative input preserve the original and extract verbatim candidate fragments using the FRD guide.
- Every statement traces to an `AL-nnn` and the source or an explicitly confirmed user answer (section 5a). When both are silent, write a TBD (section 5). Never guess or pick an unconfirmed alternative.
- Targeted activity confirmation and applying user-supplied answers are in scope. Full discovery interviews, glossaries, tickets, code and SDD belong to other workflows (for example grill-with-docs).
- Clarify activity meaning as soon as an ambiguity prevents reliable mapping. Use `activity-confirmation.md`; questions come from the actual input and conversation, never from a fixed list. A complete, unambiguous input may need no OQs.

## 2. Document set (file names are fixed)

| File | Written by |
|---|---|
| `00-activity-list.md` | generate-activity |
| `FRD.md` Functional Requirements Document | generate-activity |
| `NFRD.md` Non-Functional Requirements Document | generate-activity |
| `pertanyaan-terbuka.md` open questions, activity review and answer evidence | generate-activity |
| `traceability.md` | the validator (`--matrix`), never by hand |

## 3. IDs

| Item | Format | Defined in |
|---|---|---|
| Activity | `AL-001` | 00-activity-list.md |
| Functional requirement | `FR-001` | FRD |
| Non-functional requirement | `NFR-SEC-01` (code from section 3 of the NFRD) | NFRD |
| Open question | `OQ-01` | pertanyaan-terbuka.md |

- NFR codes: FUN, PER, COM, INT, REL, SEC, MAI, FLX, SAF.
- Numbers are zero-padded and run in order of first appearance. An ID is never reused or renumbered; a new item takes the next free number.
- Write IDs one by one. Never write a range such as "FR-001 sampai FR-005".

## 4. Closed vocabularies

| Field | Allowed values |
|---|---|
| Basis | `Eksplisit`, `Turunan` |
| Verif. | `U`, `D`, `I`, `A` (several separated by commas) |
| OQ status | `Terbuka`, `Terjawab` |
| OQ priority | `Penghambat`, `Lanjutan` |
| Activity review result | `Perlu konfirmasi`, `Cukup dari sumber` |

- **Eksplisit**: you can point at the words in the source or a confirmed answer that state it. For an answer, retain the AL in Sumber and cite its OQ next to the changed fact.
- **Turunan**: not written in the source but needed to record or support an activity. Only these are allowed: an identifier, a timestamp, who did it, a status, a link between two records. Anything else is not written; it becomes an OQ. A Turunan item always carries a reason (column Alasan, or a sentence) and an OQ for confirmation. A shared OQ must request a decision per listed item; do not assume one yes approves every derived item.
- **Verif.** choice: `U` when the behaviour can be run with an input and an expected output; `I` when a document, setting or record is examined; `A` when it is settled by calculation or reasoning; `D` otherwise. Default for a functional requirement: `U`.

## 5. Unknowns: TBD and OQ

- Write `[TBD: <what is unknown>, lihat OQ-nn]` on one line, next to the sentence it completes. In explanatory text write the marker inside backticks so the validator ignores it.
- Use a TBD only when neither the source nor a confirmed answer supplies a fact needed to complete a statement: a value, an actor, a format, a threshold, a rule.
- One OQ per independently answerable decision. Reuse an OQ only when the same decision applies; actors, thresholds or exception actions that can differ by activity need separate questions. A shared question may request a mapping per listed AL; record each AL's answer explicitly before closing it.
- For an activity clarification, the Pertanyaan cell identifies its activity, the actual unclear fragment, and the mapping or interpretation it prevents, then asks for explanation or correction. Use enough context to make the question answerable without opening another file. There is no fixed wording or number of questions.
- The question register has columns `ID | Pertanyaan | Aktivitas terkait | Mempengaruhi | Prioritas | Penjawab | Status`. List every affected AL explicitly. Use `Lintas dokumen` only for matters without a specific AL (for example document ownership or another cross-document concern). Mempengaruhi lists the affected IDs or document sections. Priority is `Penghambat` when the answer changes a capability, permission, branch, required data or pass/fail criterion; otherwise `Lanjutan`. Penjawab is a proposed role from the source, or `Belum ditetapkan`; it does not grant approval authority.
- Add `## Tinjauan aktivitas`, one row per AL, with columns `Aktivitas | Hasil tinjauan | OQ terkait | Dasar tinjauan`. Use `Perlu konfirmasi` when a related question is open, or `Cukup dari sumber` when the source and any confirmed answers suffice. Cite applicable OQs, or `-` if none; explain the actual gap or sufficient evidence. Every activity-specific OQ must be linked in each affected AL's review row. Do not create a question merely to fill a quota.
- Every TBD cites an OQ. Every open OQ is cited by an affected document or an activity review row. A plain citation such as `(lihat OQ-04)` in an Alasan or a sentence also counts as a reference.
- The source's silence establishes only that a fact is unknown. If the fact is needed for requirements, quality review or an applicability decision, ask the user and cite an OQ. A statement that an area is unnecessary or outside scope needs an explicit decision with evidence. Purely descriptive source metadata can still be labelled unavailable without inventing it.
- In a table of open questions inside FRD or NFRD, write a short title (under 60 characters), not the full question; the full text lives only in pertanyaan-terbuka.md.

## 5a. Applying confirmation answers

- A proposed option, model inference, silence, or a partial answer never closes an OQ. Ask only the unanswered part, without repeating answered questions. Keep the OQ `Terbuka` until every decision/AL it covers has an explicit answer.
- In `## Catatan jawaban`, use `OQ | Jawaban | Dikonfirmasi oleh | Tanggal | Rujukan bukti`. One current row per answered or partially answered OQ. The user's reply can be the evidence; identify the actual conversation reply or supplied document section. Dates are `YYYY-MM-DD`. Do not invent a person's name, job title or date; `Pengguna dalam percakapan` identifies the actual respondent when no name is supplied. Note unresolved parts in a partial answer.
- Apply a complete answer to every affected FRD or NFRD section that exists; replace the associated TBDs, preserve IDs and cite the OQ as provenance. Update activity review rows. Mark `Terjawab` only after the answer and evidence are recorded and the affected content is consistent. Keep documents Draft until separately approved; validator status SIAP is structural readiness, not stakeholder approval.
- Keep the source file and verbatim AL text unchanged. If an answer contradicts the SOP, record the conflict and keep it open until the user explicitly decides which rule governs. Do not silently replace the source. A confirmed new requirement outside existing activities requires a user-supplied source addition before extending the AL list.
- Re-run the validator and regenerate traceability after applying answers. If a closed decision is revised, reopen the same OQ, record the prior decision and revision evidence in its answer cell, and review every affected artifact before closing it again.
- Confirm overall understanding with a concise activity mapping and an invitation to correct it at a natural checkpoint. Record actual agreement as prose in the question file if supplied; do not create an OQ solely for this checkpoint. A delivered draft, a validator pass and silence do not imply user agreement. Already confirmed understanding needs no repeated confirmation.

## 6. Wording

- A requirement statement has exactly one `harus`. Pattern: `Sistem harus ...`, `Saat <pemicu>, sistem harus ...`, `Jika <kondisi>, maka sistem harus ...`, `Selama <keadaan>, sistem harus ...`.
- State it positively. Express restrictions as a positive access or validation capability, with an observable acceptance criterion.
- No implementation detail (screens, tables, technology) in an FR or NFR.
- Banned in requirement text: cepat, lambat, mudah, ramah pengguna, memadai, optimal, andal, fleksibel, secukupnya, segera, secepatnya, jika perlu, bila perlu, sebaiknya, mungkin, dll, dsb, dan sebagainya. Replace with a number and unit, or a complete list.
- One term per thing. Same word everywhere, same spelling as the source.
- Never write document-wide counts ("sepuluh modul") in prose.

## 6a. Actors

An actor is a role or unit the activity text names as performing, approving, or (when a record is forwarded to it) acting on the activity. An external party is an actor when the activity explicitly gives it an action; a party that only supplies input or receives a result is not automatically an actor. For "memperoleh persetujuan X dan Y" the actors are the approvers X and Y, and the FR lets each of them record the approval. In the Activity List the Aktor cell lists the actors named in the activity text, in order of appearance, separated by `; `. If the text names none, write `Tidak disebut SOP`; ask who performs it only if the context does not resolve the responsibility needed for mapping.

If the source calls the same thing by two names that might be one (for example two unit names), keep each name as written in its own activity and register one OQ asking whether they are the same. Do not merge them yourself.

## 7. Modules

A module groups consecutive activities about the same business object. Start a new module when the business object changes. A module has at most 6 activities.

These are document-grouping conventions. They do not establish the real process order or resolve an ambiguous business object. Clarify an uncertain mapping before treating it as settled; provisional groupings must show the relevant OQ.

- Declared on the first non-blank line under the module heading: `Sumber aktivitas: AL-001, AL-002.`
- Group only consecutive activities. A later return to an object already used starts a new module.
- Example: requesting offers, checking they are written, and negotiating are about the object "penawaran" (one module). Approving the price is about "persetujuan harga" (the next module). Making the PO is about "PO". Receiving goods is about "penerimaan". Claims are about "klaim".
- Every activity belongs to exactly one module.
- Each FRD module has a stable number, name (`Modul <Nama>`) and declared activity set.

## 8. One home per fact

| Fact | Lives in | Other documents |
|---|---|---|
| Capability statement and acceptance criteria | FRD | cite `FR-nnn` |
| Quality target and how it is measured | NFRD | cite `NFR-...` |
| A number or list that is a quality target | NFRD | the FR cites the `NFR-...`, never restates it |
| Definitions of terms | FRD 1.4 | cite "lihat FRD 1.4" |
| Open questions | pertanyaan-terbuka.md | cite `OQ-nn` |

The validator warns when a long sentence appears in two documents.

## 9. Front matter of every document

`ID dokumen` `DOC-<FRD|NFRD>-001`; `Versi` 0.1; `Status` Draft; `Tanggal` today's date; `Penulis` "AI agent (draf, perlu ditinjau manusia)"; `Pemilik dokumen` the supplied owner, or "Belum ditetapkan" without creating an automatic OQ; `Dokumen terkait` the other documents. Delete the `<!-- ulang:... -->` markers when copying a template. Write the Daftar Isi with `--toc`.

## 10. Validator

```bash
python -I scripts/validate.py docs/ --toc --matrix              # after writing documents
python -I scripts/validate.py docs/ --source sop.md --toc --matrix   # also checks the Activity List against the source
```

`scripts/validate.py` is relative to the skill's folder. If your working directory is elsewhere, use the skill folder's absolute path and give `docs/` and `sop.md` as paths that resolve from where you run it. This validator reads only the activity list, FRD, NFRD and question register. Templates live directly in assets/. Use --intake to check extraction and questions before the full document set exists.

Status: `GAGAL` (errors: fix and rerun), `BELUM SIAP` (open OQs, TBDs or unreviewed quality gaps: documents stay Draft), `SIAP` (no errors, open questions, TBDs or unreviewed quality gaps; this is not business approval). Source silence does not settle quality applicability.
