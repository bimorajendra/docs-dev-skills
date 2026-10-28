---
name: generate-activity
description: >-
  Interpret an SOP, business activity list or informal application brief, clarify wording that cannot be mapped confidently, and produce an Activity List, FRD and NFRD in Indonesian. Use when asked for requirements from activities or an app idea, to check activity understanding, or to apply clarification answers. Questions follow the supplied input and conversation. Uses requirement structures from ISO/IEC/IEEE 29148, Volere, NASA and ISO/IEC 25010/25030/25023.
metadata:
  version: "1.6"
  compatibility: Needs Python 3 to run scripts/validate.py. Works in any agent that supports Agent Skills.
---

Turns a source into these files in `docs/`: `00-activity-list.md`, `FRD.md`, `NFRD.md`, and `pertanyaan-terbuka.md` for unresolved decisions and activity review. Documents are in Indonesian. Record answers supplied by the user; never supply business answers yourself. Stay at the level of functional capabilities, acceptance criteria and quality requirements.

Read `references/conventions.md` and `references/activity-confirmation.md` first. The former defines document conventions; the latter defines when and how to clarify meaning. Paths are relative to this skill's folder. Templates define document structure, not questions to ask.

## Steps

1. **Get the source.** Use the SOP, activity list or informal brief already supplied; ask only if there is no source. Save it unchanged as `sumber.md` (or retain an existing `sop.md`) next to `docs/`. Follow the intake mode in `references/frd-guide.md`; do not demand that the user convert a narrative into a numbered SOP.

2. **Understand the activities.** Extract `docs/00-activity-list.md` verbatim, following "Intake" in `references/frd-guide.md`. Read each activity in context and distinguish what is explicit, what the conversation already clarifies, and what cannot yet be mapped. Start `docs/pertanyaan-terbuka.md` with only actual gaps. Ask about blocking ambiguities now, without waiting for a separate request to confirm. Explain the activity fragment and the mapping it leaves uncertain. Continue independent work while awaiting answers; keep the dependent mapping provisional. If the user explicitly requests a draft without questions, record unresolved gaps and proceed with TBDs.

3. **Check the interpretation and map modules.** Reflect the understood activities back to the user in a concise flow or mapping, preserving the business terms. Invite correction once; reuse agreement already given. Follow "Modules" in `references/frd-guide.md` for the clear parts. Do not guess an object, actor or sequence merely to complete the mapping. Done when each mapping is supported or explicitly marked provisional with its OQ.

4. **FRD.** Create `docs/FRD.md` from `assets/FRD.template.md` (same headings and tables), following "Functional requirements" in `references/frd-guide.md`. Done when every AL has at least one FR and every FR has an acceptance criterion.

5. **NFRD.** Create `docs/NFRD.md` from its template following `references/nfrd-guide.md`. Review audience, operating context and relevant quality expectations, not just the facts mentioned in the brief. Ask about missing applicability, measures or targets; preserve established requirements and answers. Done when every characteristic has supported rows, an evidenced user decision that it needs no additional requirement, or a contextual OQ. Silence cannot establish that an area has no requirement.

6. **Check coverage.** Revisit every AL against the resulting requirements and the latest conversation. Maintain `docs/pertanyaan-terbuka.md` using its template and conventions section 5. Done when every AL has a review row and each TBD cites its OQ. A question register can be empty.

7. **Review.** Run the self-review in `references/frd-guide.md`. Delete any requirement that has no AL in Sumber or adds a rule, field or screen supported by neither the source nor a confirmed answer.

8. **Validate.** From this skill's folder (or with its absolute path):

   ```bash
   python -I scripts/validate.py <docs> --source <source-file> --toc --matrix --require-ready
   ```

   Run full validation once the set exists. Structural errors require repair; exit 3/BELUM SIAP requires continuing the clarification cycle. Done when strict validation returns zero and the semantic review passes, or the user explicitly requests a draft with the remaining decisions deferred.

9. **Continue or deliver.** Run `scripts/clarify.py <docs> next` and follow the action loop in `references/activity-confirmation.md`. After every reply, apply it and advance to the next unresolved decisions without needing a user reminder. Deliver the completed stage only on `complete` plus strict validation; `wait` means a question is already pending, and `deliver_draft` requires explicit user deferral.

## Not done here

Detailed solution design, implementation, full discovery interviews, glossaries and ticket breakdown. Targeted confirmation of these requirement documents and applying user-supplied answers are in scope.
