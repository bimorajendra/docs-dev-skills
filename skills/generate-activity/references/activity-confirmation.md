# Activity review and confirmation

Use while first reading activities, before committing to a mapping, and again when requirements or later answers reveal ambiguity. This is a reasoning workflow, not a question bank. Derive questions from the actual activity list and conversation. Conventions sections 5 and 5a define the register, review rows and answer log.

## Decide whether clarification is needed

Read each activity with its neighbours and any supplied definitions or answers. Identify what it says, the interpretation supported by that context, and any ambiguity that would change the mapping. An unclear actor, object, term, condition, sequence or result matters only when it prevents an accurate statement about this activity. These are possible sources of ambiguity, not mandatory question topics.

- If the source and conversation support a clear interpretation, map it and note its basis. Do not ask again merely because another activity needed clarification.
- If two plausible readings would produce different mappings, ask before choosing. If no interpretation is defensible, ask what the fragment means rather than offering invented alternatives.
- If a fact is irrelevant to the current task, leave it unspecified. If its relevance is itself unknown, or it is needed to define the audience, operating context, quality expectations or verification of an activity, ask the user. Absence from the brief is not evidence that a requirement is unnecessary. A blank heading alone does not justify inventing a feature or target.
- If the user explicitly wants a draft without interruption, retain the ambiguity as an OQ/TBD and label the dependent mapping provisional.

## Ask about the activity's meaning

In plain Indonesian, identify the activity and quote or precisely point to the fragment that is unclear. Explain the uncertainty and why it changes the interpretation, then ask the user to explain or correct that part. Write the question naturally; there is no required sentence pattern or fixed question count.

- Keep one independently answerable uncertainty per question. A shared question is appropriate when the same interpretation affects several activities; identify which ones.
- Offer alternatives only when the text actually supports them. Make room for a different explanation. Do not preselect an answer or introduce an unstated process as a likely fact.
- Ask the most consequential ambiguity first, and revisit remaining gaps after the reply. A reply may resolve several questions or make earlier questions irrelevant.
- Do not copy questions from bundled examples. Derive questions from the actual activities and remaining uncertainties, including missing quality expectations. Reuse established answers, group related gaps and explain why each answer affects the requirements. No topic list or question count is mandatory.

One illustration of reasoning, not reusable wording: if a user supplies `Admin memproses pengajuan yang sesuai`, the fragment `yang sesuai` does not identify what is being checked. Explain that the activity cannot yet be mapped to a specific check, and ask what `sesuai` refers to in this process. If a neighbouring activity already defines that check, use it instead and ask nothing about it. If the user later supplies a complete activity with an actor, comparison and observable result, map it without replaying this question.

## Apply replies and verify understanding

Ask a blocking clarification during intake or mapping, even when the user has not separately requested an interview. Do useful independent work while awaiting an answer; do not fill the blocked detail by guessing. Use the latest answer to update the interpretation and all affected artifacts under conventions section 5a. Ask a follow-up only when that reply leaves a meaningful gap. Never turn a partial answer or silence into agreement.

Reflect the resulting interpretation back as a short flow or activity mapping, showing who does what and any relevant condition and result. Invite the user to correct it once at a natural checkpoint. Reuse prior agreement; do not make the user approve every document or every activity. This is confirmation of meaning, not a request for permission to generate files. If there are no ambiguities, provide the clear mapping and invitation to correct it without manufacturing an OQ. Record explicit agreement when supplied; a draft can be delivered while the overall understanding remains unconfirmed.

Completion review: every activity is accounted for; its meaning and mapping follow the source or an actual reply; dependent flows and outcomes agree; every unresolved gap has a contextual OQ; answered gaps are not asked again; and an activity that is clear has no artificial question. Validator success checks structure and links, so also perform this semantic review before reporting the outcome.

A clear functional activity does not by itself settle its quality requirements. Review unknown quality applicability and targets separately. Preserve correct capabilities, rows, IDs and prior answers while adding those gaps; report the unresolved quality review even when the functional mapping is complete.

## Run the clarification cycle

Use `scripts/clarify.py <docs> next` after the first gap review, after each user reply, and before delivering a result. It reads actual OQs and the persistent `.clarification-state.json`; it has no question bank. Its `--limit` controls batch size, not how many questions the project requires. Ask related questions and cover all unasked gaps before repeatedly pursuing a partial answer that the user cannot yet quantify.

Follow the returned action, not merely the validator's exit code:

| Action | What the agent does |
|---|---|
| `repair` | Fix invalid links/documents or create OQs for untracked quality gaps, then run `next` again. |
| `apply_reply` | Read the actual user reply and evidence, update the answer log and all affected content, then record `applied` and run `next` again. |
| `ask` | Ask the returned unresolved decisions in natural language. After actually sending them, record `asked` with the delivery reference. |
| `wait` | The batch has been sent; wait for its answer while doing independent work. Do not resend it or call the document complete. |
| `draft` | The decisions are resolved but outputs are missing. Generate the current stage's outputs, validate them and run `next` again. |
| `deliver_draft` | All remaining decisions were explicitly deferred by the user. Deliver only a draft and show those decisions; they remain open. |
| `complete` | Run strict validation and the semantic review, then deliver the completed stage. |

Commands, relative to the skill folder:

```bash
python -I scripts/clarify.py <docs> next --limit <batch-size>
python -I scripts/clarify.py <docs> asked OQ-01 OQ-02 --evidence <actual-question-message-reference>
python -I scripts/clarify.py <docs> reply OQ-01 --evidence <actual-user-reply-reference>
python -I scripts/clarify.py <docs> applied OQ-01 --evidence <updated-answer-and-document-reference>
python -I scripts/clarify.py <docs> defer OQ-02 --evidence <explicit-user-decision> --reason <what-the-user-deferred>
```

Receive the reply before recording `reply`. Do not use `applied` until the answer and its evidence have been logged and affected documents updated. A partial answer keeps the OQ open and returns it to the follow-up queue; rewrite any follow-up to ask only the remaining gap. Already applied historical answer logs can be imported with `applied` after checking their affected documents. A new reply to an old decision requires recording its new evidence, not silently reusing the previous answer.

The loop continues through the remaining OQs without waiting for the user to point out an omitted section. Recording an OQ is discovery, not completion. `BELUM SIAP` is a work state: move to the next action or wait on an already asked question. Never report the whole task complete because validation returned zero in its default draft-checking mode. Final checking uses `validate.py <docs> --require-ready`; exit 3 means decisions are still open.

If the user changes the active task, preserve received replies and runner state, then follow that instruction. Resume the domain interview only when it is again the active task. Do not send queued questions during a request to repair the harness itself. The runner chooses and gates actions; the agent still interprets replies and sends questions through the available user-input tool. It does not create a background automation.
