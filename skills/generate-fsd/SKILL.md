---
name: generate-fsd
description: >-
  Turn an FRD and NFRD into an Indonesian FSD (module specifications plus one use case with a scenario per activity) and, on request, test cases, following the FRD and NFRD without asking new questions. Use after generate-activity for specifications, use cases, or test cases on request. Uses SAP, Microsoft Dynamics 365, IIBA, use case specification and ISO/IEC/IEEE 29119-3 structures.
metadata:
  version: "1.8"
  compatibility: Needs Python 3 to run scripts/validate.py. Works in any agent that supports Agent Skills. Expects docs/ produced by generate-activity.
---

Reads `docs/00-activity-list.md`, `FRD.md`, `NFRD.md`, `pertanyaan-terbuka.md` and writes `docs/FSD.md` (and `docs/TEST-CASE.md` only when asked), in Indonesian. It asks the user nothing: every flow, rule, check and exception comes from the FRD, NFRD and Activity List, and every unknown is carried over from an OQ that `generate-activity` already registered. Questions, answers and interviews belong to `generate-activity`.

Read `references/conventions.md` first. Paths are relative to this skill's folder.

## Steps

1. **Check the input.** From this skill's folder (or with its absolute path) run `python -I scripts/validate.py <docs>`. The Activity List, FRD, NFRD and open-question file must exist and show no error. Done when the status is not GAGAL. If they are missing, tell the user to run `generate-activity` first. Open OQs in the input are not a reason to stop or to ask: carry them into the FSD as TBDs.

2. **Write the FSD from the FRD and NFRD.** Read the ALs, the requirements and any answers already logged in `pertanyaan-terbuka.md`. Create `docs/FSD.md` from its template following `references/fsd-guide.md`: the use case list (one `UC-nnn` per AL), then per module the 12 parts, ending with the use case scenarios. Add no rule, branch, actor or derived item that the FRD, NFRD or AL text does not support. Done when every module has all 12 parts, every AL has a use case and a scenario, and every BR, VAL and EXC has a Sumber and a Basis.

3. **Test cases (optional).** Use cases belong to the FSD and are not test cases; test cases are a separate document derived afterwards. Do this step only when the user asks for test cases; otherwise skip it, and the FSD alone completes the stage. Create `docs/TEST-CASE.md` from `assets/TEST-CASE.template.md`. Fill it following `references/test-case-guide.md`. Done when every FR, BR, VAL and EXC is in at least one case.

4. **Carry unknowns, never ask.** Where the input still has an open OQ, write `[TBD: ..., lihat OQ-nn]` with that existing OQ. Create no new OQ and ask the user no question. A fact the FSD needs but the FRD and NFRD lack is left out and listed in the final report as something to resolve in `generate-activity`. Link each cited OQ in the activity review rows as they already are. Done when every TBD cites an existing OQ.

5. **Review.** Delete any BR, VAL, EXC, flow row or test case supported by neither source words nor a confirmed answer. Keep AL traceability and OQ provenance for confirmed facts. Delete any sentence copied from the FRD or NFRD.

6. **Validate.**

   ```bash
   python -I scripts/validate.py <docs> --source <sop.md> --toc --matrix
   ```

   Fix errors and rerun. `BELUM SIAP` here means the input still has open OQs; it is not an error of this stage. Done when the validator reports no error and the semantic review passes.

7. **Deliver.** Report the status, the number of open OQs inherited from the input, and the list of facts the FSD needed but the input lacks. Tell the user to answer those through `generate-activity`, then rerun this skill to refresh the FSD. Keep the documents Draft.

## Not done here

Asking questions, inventing OQ answers, full discovery interviews, glossaries, ticket breakdown, code, SDD (so no application architecture or SDLC chapter), and screens or interface layouts the user did not supply.
