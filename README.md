# generate-activity and generate-fsd

Two [Agent Skills](https://agentskills.io) that turn a business process (SOP, activity list or app brief) into requirement and specification documents in Indonesian, each checked by a validator.

| Skill               | Reads                       | Writes                                                                                   |
| ------------------- | --------------------------- | ---------------------------------------------------------------------------------------- |
| `generate-activity` | SOP, activity list or brief | `00-activity-list.md`, `FRD.md`, `NFRD.md`, `pertanyaan-terbuka.md`                      |
| `generate-fsd`      | the four files above        | `FSD.md` with a use case and scenario for every activity; `TEST-CASE.md` only on request |

`generate-activity` asks when an activity is ambiguous and records your answers. `generate-fsd` asks nothing: it follows the FRD and NFRD and leaves open questions as TBDs. Neither invents a business answer. All output is a draft for a human to review.

## Install

Install both skills; `generate-fsd` needs the files `generate-activity` writes.

**One command** (after the repository is on GitHub; replace `<owner>/<repo>`):

```bash
npx skills add <owner>/<repo> -g -a claude-code
# or, with the GitHub CLI, once per skill:
gh skill install <owner>/<repo> generate-activity --agent claude-code --scope user
gh skill install <owner>/<repo> generate-fsd --agent claude-code --scope user
```

Change the agent name for other tools (Codex, Cursor, GitHub Copilot and more).

**By hand:** copy `skills/generate-activity` and `skills/generate-fsd` into your agent's skills folder, then restart the agent.

| Harness                                                                 | Personal folder     | Project folder    |
| ----------------------------------------------------------------------- | ------------------- | ----------------- |
| Claude Code                                                             | `~/.claude/skills/` | `.claude/skills/` |
| Shared path (reported for Codex, Gemini CLI, Copilot, Cursor, OpenCode) | `~/.agents/skills/` | `.agents/skills/` |

Only the Claude Code row was tested here. Other tools also have their own folders (for example `.cursor/skills/`, `.gemini/skills/`) and these change between versions, so check your tool's documentation. An agent without skill support can still use them: tell it to read `<path>/generate-activity/SKILL.md` and follow it. Requires Python 3 (standard library only).

## Use

Put the SOP in your project and ask the agent:

```
/generate-activity   buat requirement dari sop.md
/generate-fsd        buat FSD dari docs/
```

Output goes to `docs/`. If `generate-fsd` leaves TBDs, answer them in `generate-activity`, then rerun `generate-fsd`. Add "dan test case" to the second request if you want test cases.

## Output

| File                    | Holds                                                                                                                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00-activity-list.md`   | Source activities verbatim, with `AL-nnn` IDs and actors                                                                                                                                                 |
| `FRD.md`                | Functional requirements (`FR-nnn`) with acceptance criteria, grouped into modules                                                                                                                        |
| `NFRD.md`               | Quality requirements (`NFR-XXX-nn`) per ISO/IEC 25010 characteristic                                                                                                                                     |
| `pertanyaan-terbuka.md` | Open questions (`OQ-nn`), a review row per activity, log of confirmed answers                                                                                                                            |
| `FSD.md`                | Per module: actors, flow, input, output, business rules, validations, exceptions, use case scenarios. Also the use case list (`UC-nnn`, one per activity), status model, security and interface chapters |
| `TEST-CASE.md`          | Optional test cases (`TC-nnn`)                                                                                                                                                                           |
| `traceability.md`       | Written by the validator; never edit by hand                                                                                                                                                             |

A use case describes how an actor and the system work through one activity and lives in the FSD. A test case checks one expected result and is a separate, optional document.

## Rules the skills follow

- Nothing is guessed: an unknown becomes `[TBD: ..., lihat OQ-nn]` plus an open question. A question closes only after an explicit answer, its source and date are recorded.
- The source stays verbatim; one numbered item is one activity.
- One home per fact: criteria in the FRD, quality targets in the NFRD, rules and flows in the FSD. Other files cite the ID.
- Fixed ID formats and vocabularies; exactly one `harus` per requirement.

## Validate

```bash
python -I skills/generate-activity/scripts/validate.py docs/ --source sop.md --toc --matrix
python -I skills/generate-fsd/scripts/validate.py docs/ --source sop.md --toc --matrix
```

| Status       | Meaning                                      |
| ------------ | -------------------------------------------- |
| `GAGAL`      | Structural errors; fix and rerun (exit 1)    |
| `BELUM SIAP` | No errors, but open questions or TBDs remain |
| `SIAP`       | No errors, no open questions, no TBDs        |

`SIAP` is structural readiness only, not approval; documents stay `Draft` until a person approves them. `generate-activity` also has `--intake` (check extraction before the FRD exists) and a clarification runner, `skills/generate-activity/scripts/clarify.py`.

## Tests

```bash
python -I -B -m unittest discover -s tests -v
```

## Limits

- Output is an AI-written draft; review use case names, goals and scenarios.
- The validator checks structure, coverage and links, not whether the business content is right.
- Tested on Windows with Python 3.13, Codex and Claude Code only.
