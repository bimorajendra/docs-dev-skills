# FRD guide

Basis: ISO/IEC/IEEE 29148 (requirement characteristics, SRS content), Volere (the requirement "shell": identifier, description, rationale, originator, fit criterion), NASA Systems Engineering Handbook appendix C (one "shall" per requirement, rationale, no implementation detail, verifiable). The Volere template and the 29148 text are copyrighted; this guide uses their structure, not their wording. The mapping into the FRD columns:

| FRD column | Comes from |
|---|---|
| ID | unique identifier (29148, Volere) |
| Pernyataan | requirement description, one "shall" (NASA, 29148 singular) |
| Sumber | originator / traceability to the source (Volere, 29148) |
| Alasan | rationale (Volere, NASA) |
| Kriteria Penerimaan | fit criterion (Volere), verifiability (29148, NASA) |
| Basis | explicit versus derived, for confirmation |
| Verif. | verification method (29148) |

## Intake: build the Activity List

Input is the source text. Output is `docs/00-activity-list.md`, created from `assets/00-activity-list.template.md`, with the table `ID | Ref SOP | Aktivitas | Aktor`.

1. For a numbered activity list, one source item = one AL. Never split or merge those supplied items. For an informal brief, extract distinct activity fragments as candidate ALs, keeping each fragment verbatim. Preserve the original brief; a candidate extraction is not a confirmed workflow.
2. Ref SOP: the source clause number without parentheses (`4.1`), or `-` if there is none. For narrative fragments write `Narasi`; the validator checks that each fragment occurs in the preserved source.
3. Aktivitas: copy the item or narrative fragment exactly, without a list or clause number. Do not silently convert uncertain phrases into concrete features. Put any proposed interpretation in the requirements or review, clearly labelled as provisional. Vague words stay in the extraction.
4. Aktor: apply conventions section 6a. If no actor is stated, keep `Tidak disebut SOP` in this source-extraction column. Read neighbouring activities and the conversation before deciding whether responsibility remains ambiguous. Ask only when that uncertainty prevents a reliable mapping. After a reply, record the clarified actor in the affected requirements and OQ answer log; preserve the source extraction.
5. Vague source words ("dsb.", "memahami", "sesuai") are not fixed. If one blocks an acceptance criterion, a TBD on that criterion cites an OQ for it.
6. The source's title and version go in FRD 1.5. If the source has none, write "Tidak disebut sumber".

Done when every numbered item is preserved, or each narrative fragment is traceable to the brief. Review narrative coverage semantically: substring checks cannot prove that every intent was extracted. If clarification is needed before generating requirements, run `validate.py <docs> --source <source-file> --intake`; this checks the extraction and question register without requiring completed documents.

## Modules

Apply conventions section 7. Walk the ALs in source order; keep the same module while the business object stays the same; start a new module when it changes. If a term or activity cannot be assigned to an object confidently, clarify its meaning before settling the grouping. Name the module after the object (`Modul Permintaan Pembelian`). Write the declaration line under each heading. Source numbering determines document order, not necessarily execution order.

Done when every AL is in exactly one module and no module has more than 6 ALs.

## Functional requirements

For every AL, apply in order. Where these rules refer to the source, an answer confirmed under conventions section 5a may also supply the fact; retain AL traceability and cite its OQ. Unconfirmed proposals do not count.

1. **One FR per distinct action.** An action is a verb with its own object.
   - Verbs that share one object stay in one FR (mengarsipkan, menyimpan, dan memelihara seluruh catatan = one FR).
   - One verb with several objects joined by "dan", "serta" or commas stays in one FR that lists every object (memberikan penjelasan awal serta estimasi waktu = one FR).
   - Verbs with different objects are separate FRs (mengajukan klaim dan melakukan negosiasi = two FRs).
   - A manner clause "dengan <kata kerja> ..." (dengan mengupayakan ...) is not a separate action. Keep the stated condition with the main capability and its acceptance criterion.
2. **Alternatives stay together.** "melalui surat atau email", "PO dan/atau Formulir": one FR that names every alternative.
3. **Conditions.** "apabila X" becomes `Jika X, maka sistem harus ...`.
4. **Statement form.** `Sistem harus memungkinkan <Aktor> <kata kerja> <objek>.` for every activity a person performs. Use the plain form `Sistem harus <kata kerja> ...` only for a Turunan behaviour. Never write that the system sends, calls or negotiates unless the source says the system does it. For `Tidak disebut SOP` actors, write `Pelaku`. For "memperoleh persetujuan X dan Y", write one FR per approver: `Sistem harus memungkinkan X mencatat persetujuan ...`.
5. **Keep the source nouns.** Reuse the object, list items and channel names of the AL text as written. A number or list that is also a quality target goes in the NFRD; the FR cites the NFR ID instead of repeating it.
6. **Alasan.** For Eksplisit: the clause of the AL that states why ("untuk memperoleh ...", "agar ...", "sebagai bahan ...", "guna ..."), copied. A clause with "untuk" that names an object or beneficiary ("untuk barang atau jasa yang ...", "untuk transaksi tunai") is not a purpose. Write `-` when there is no purpose clause or when the statement already contains it. For Turunan: one sentence naming the AL it supports and why the record is needed, and the confirming OQ as `(lihat OQ-nn)`.
7. **Kriteria Penerimaan.** At least one. The first is the normal case of the AL. Add another only for each "atau" or "dan/atau" alternative and each "apabila" condition, and only when its observable outcome differs from the first. A list joined by "dan" is one criterion. Form: `Diberikan <kondisi>, ketika <aksi>, maka <hasil yang dapat diamati>.` Observable means a verb such as tercatat, tersimpan, tampil, ditolak, terbentuk. Values not in the source: `[TBD: ..., lihat OQ-nn]`. Separate several criteria with `<br>`.
   - **Human-only steps** (the SOP says a person phones, meets, inspects, explains): distinguish the human action from any system support the source or conversation actually specifies. If recording the result is supported, the criterion checks that record; use its supplied contents. Ask about record contents or system boundaries only when the missing detail prevents an observable criterion, and cite that specific OQ. Do not automatically add a recording feature or a boundary question to every human action.
8. **Basis and Verif.** Per conventions section 4. A restriction to named roles that the AL states is Eksplisit.
9. **Order.** FRs follow AL order, then the order of actions inside the AL. Number them in that order.
10. **System boundary.** Use the source and confirmed replies to distinguish human actions from system behaviour. If a specific activity leaves that boundary ambiguous and the ambiguity changes the requirement, ask about that activity's unclear fragment and explain the competing interpretations. Cite its OQ in 2.4 Asumsi dan Ketergantungan. Do not ask a project-wide boundary question when the supplied activities already explain it.
11. **Derived behaviour.** Add a Turunan FR only for: an identifier for each main record, who recorded it and when, the status of the main record, the link between two records. A main record is a record that the AL texts create or change in turn (for example the purchase request, the PO, the claim). Each Turunan FR cites a confirming OQ; a shared OQ must list the items and request a decision for each.

Done when every AL has an FR, every FR has at least one acceptance criterion, and no FR holds more than one `harus`.

## Self-review before validating

For each FR, answer from the list in FRD Lampiran A: needed (an AL and, where applicable, a confirmed answer support it), singular, unambiguous (no banned word), verifiable (the criterion can fail), correct (matches the source and confirmed decisions), conforming (pattern and columns). Delete or fix any that fails. Run the activity review in `activity-confirmation.md` before validation.
