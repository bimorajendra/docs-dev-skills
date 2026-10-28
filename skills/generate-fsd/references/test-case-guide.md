# Test case guide

Basis: ISO/IEC/IEEE 29119-3:2021, test case specification. A test case has a unique identifier, an objective, traceability, preconditions, inputs and expected results (the standard also has a priority; the source gives none, so there is no priority column). The standard's text is paid; this guide uses its structure.

## Inputs

`FRD.md` (acceptance criteria), `NFRD.md`, `FSD.md`. Read `references/conventions.md` first.

Confirmed answers in `pertanyaan-terbuka.md` may complete test data, conditions and expected results under conventions section 5a. Cite the OQ for provenance, update dependent cases when a decision changes, and leave unanswered conditions as TBD. Never treat a proposed option as an expected result.

Use cases (`UC-nnn`, FSD 2.5 and the scenarios of chapter 3) are the FSD's own artifact and are not test cases.

## Procedure

1. **Copy the module list** from the FRD (same numbers, names, `Sumber aktivitas` lines).
2. **Derive cases, in this order, for each module.**
   - Each acceptance criterion of each FR gives one `Positif` case. An FR with two criteria has two cases.
   - A business rule that restricts or forbids something gives one `Negatif` case that breaks the rule.
   - A business rule that only requires or chooses something is added to the Rujukan of the `Positif` case of the FR it belongs to; it gets no case of its own.
   - Each validation gives one `Negatif` case that fails the check.
   - Each exception gives one case that creates the condition. Jenis is `Negatif`.
   - When a BR, a VAL and an EXC describe the same condition, one `Negatif` case cites all of them.
3. **Fill the columns.**
   - Rujukan: every FR, BR, VAL and EXC the case checks, IDs one by one.
   - Prakondisi: the starting state, in words.
   - Input dan Langkah: numbered steps separated by `<br>`. Inputs are described by condition ("permintaan pembelian yang salah satu kolom wajibnya kosong"), never by invented values or names. Use values only when the source gives them.
   - Hasil yang Diharapkan: what an observer sees. Take it from the acceptance criterion (paraphrase it, or write "sesuai kriteria penerimaan FR-nnn"), or write "sesuai Tindakan Sistem VAL-nn" or "sesuai Tindakan Sistem EXC-nn". Do not paste a sentence that already stands in another document.
   - When the rule or validation has no known system action, the expected result is a TBD citing the relevant branch-decision OQ. The validator warns on cases whose expected result is only TBD.
4. **Non-functional.** For each NFR whose Target is a number or a complete list and whose Verif. includes `U`, write one `Non-fungsional` case in chapter 4. NFRs with another Verif. (for example `I`) are not tested here.
5. **Cakupan.** One row per FR, BR, VAL and EXC listing every TC that cites it. Every item has at least one case.
6. **Numbering.** `TC-001` upward in document order (chapter 3 module by module, then chapter 4).
7. **Test data and environment.** Read the source and conversation for supplied conditions. Concrete environment details are unnecessary for conceptual cases that can be specified by condition. If nothing is supplied, state "Belum ditetapkan untuk pelaksanaan uji" in 2.2.

Done when every FR, BR, VAL and EXC is in at least one case, every case cites items of its own module (chapter 3), and the validator shows no error for TEST-CASE.
