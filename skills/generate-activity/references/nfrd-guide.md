# NFRD guide

Basis:
- ISO/IEC 25030: how quality requirements are classified (with the 25010 model) and made measurable. It prescribes no particular measure.
- ISO/IEC 25010:2023: the nine product-quality characteristics.
- ISO/IEC 25023: measures for those characteristics. It assigns no value ranges; the targets come from the source.
- OWASP ASVS: security verification levels (L1 to L3). WCAG 2.2: accessibility conformance levels (A, AA, AAA). Google SRE: service level indicators (SLI) and objectives (SLO).

The standards' full texts are paid or large; this guide uses their structure. Check section names against a licensed copy before an audit. Only the first four 25010 characteristics and the name "Interaction Capability" were cross-checked online; the rest are from general knowledge.

| Code | Characteristic | Sub-characteristics |
|---|---|---|
| FUN | Functional Suitability | Functional completeness, Functional correctness, Functional appropriateness |
| PER | Performance Efficiency | Time behaviour, Resource utilization, Capacity |
| COM | Compatibility | Co-existence, Interoperability |
| INT | Interaction Capability | Appropriateness recognizability, Learnability, Operability, User error protection, User engagement, Inclusivity, User assistance, Self-descriptiveness |
| REL | Reliability | Faultlessness, Availability, Fault tolerance, Recoverability |
| SEC | Security | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, Resistance |
| MAI | Maintainability | Modularity, Reusability, Analysability, Modifiability, Testability |
| FLX | Flexibility | Adaptability, Scalability, Installability, Replaceability |
| SAF | Safety | Operational constraint, Risk identification, Fail safe, Hazard warning, Safe integration |

## Procedure

Create `docs/NFRD.md` from `assets/NFRD.template.md`. Confirmed user answers may supply missing quality targets under conventions section 5a; keep the AL source and OQ provenance. Then, for each of the nine characteristics in table order, decide:

1. **Known.** Preserve correct rows and write new rows only for facts established by the source or user replies. An explicit answer may supply a quality requirement even when the original brief has no quality cue. Keep AL traceability and answer provenance.
2. **Unknown.** Review what is still needed to specify and verify the actual application: its audience and operating context, usage load, relevant quality targets, operational constraints and consequences of failure. If applicability, a measure or a target is unknown, ask the user in the context of the affected activities and write `Bergantung OQ-nn.` with a short explanation of the missing decision. Do this even when the brief is silent. A subsection can contain a correct row and an unresolved question about a different aspect; do not delete the row.
3. **Not applicable.** Conclude that an area needs no additional requirement only when the user has explicitly decided that it is outside scope or unnecessary. Cite the answered OQ and explain the decision. Silence is not a decision. If the user is unsure, leave the question open; an explicitly labelled proposal can help them choose, but no proposed value becomes a target until accepted.

When a confirmed answer settles the relevant context or quality decision without defining a separate measurable NFR, write `Keputusan mutu terkonfirmasi:` followed by the decision and its answered OQ. For example, a user may explicitly require recovery without a time guarantee for the initial phase. Retain existing measurable requirements and any applicable FR references. This is not a declaration that the characteristic is inapplicable; never invent a target or ask again solely to satisfy a table. Every cited decision must have recorded answer evidence.

Review all nine characteristics for actual gaps without treating them as nine mandatory questions. Combine only the same decision shared by activities, reuse answered facts, and ask manageable groups in the order that informs later decisions. Explain the business effect of an unanswered item rather than asking users to choose standards jargon. A sample table below supplies possible evidence, not a fixed questionnaire.

| Cue in an AL text | Characteristic | Row allowed when |
|---|---|---|
| A named approver or a restriction to named roles | SEC (Authenticity, Accountability) | the roles are named in the AL |
| Records that must be kept, filed, archived | REL (Recoverability) or SEC (Integrity) | the AL names what is kept |
| A response or processing duration for a system operation | PER (Time behaviour) | the duration is established by the source or an answer |
| Data taken from another system | COM (Interoperability) | the AL names the other system |
| A change marked on a record ("Revisi") | SEC (Accountability) | the AL states the marking |

Not performance NFRs: a business completion deadline, a minimum or maximum business count/amount, and the fields of a form. Capture established business limits with the relevant functional requirement, acceptance criteria or scope constraints. If an answer to a response-time question instead describes a business deadline, clarify which activities it governs and keep the response-time target unresolved. An illustrative date is not a final date or a recurring rule.

Distinguish data volume, account totals and concurrent usage. Approximate participant and account counts remain planning estimates until a measurable capacity target is established; a statement that concurrency is lower than account totals does not supply an exact concurrency limit.

## Row rules

- Columns: `ID | Sub-karakteristik | Pernyataan | Ukuran | Target | Sumber | Basis | Verif.`. The ID code equals the section's characteristic code.
- Pernyataan: one `harus`, no implementation detail.
- Ukuran: what is counted or observed (for example "jumlah percobaan persetujuan oleh peran selain yang disebut sumber yang berhasil").
- Target: a number, a threshold, or a complete list that the source gives. When the AL says "setiap" or "seluruh", the Target may be written "100% dari <objek>" and the measure counts the exceptions. A Target that is only a TBD is not allowed: the row is not written (outcome 2).
- Example of a list Target: for an Integrity row about final status, Target `resolved; cancel; partial`, copied from the AL.
- Verif.: conventions section 4. A check that a listed field is present: `U`.
- A Turunan row has a sentence under the table: `Alasan NFR-XXX-nn: <why>, lihat OQ-nn.`
- A level of OWASP ASVS, a WCAG level, or an SLO is never invented. A general cue alone does not justify a question about a standard. Ask only when a specific unresolved quality expectation in the source or conversation prevents a requirement or verification criterion from being mapped. Explain that activity's ambiguity in business terms. Otherwise leave the level unspecified; a named approver alone is no reason to ask for an ASVS level.

## Regulations

Chapter 4 lists only policies or regulations established by the source or confirmed replies. When applicability is unknown, ask which organisational, privacy, retention or delivery policies govern the activity and cite its OQ. Do not invent a law or conclude that none applies because the brief is silent. An explicit user decision may establish that no additional compliance requirement is in scope.

Done when every characteristic has supported requirements, an explicit applicability decision with evidence, or a contextual open question. Every requirement row has a measurable Target. Unknown audience, applicability or quality targets keep the draft BELUM SIAP; a structural pass alone does not settle them.
