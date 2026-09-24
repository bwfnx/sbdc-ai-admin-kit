# Cold-test checklist — transcript-to-action-plan-client-email

Run each test in a **fresh chat** with only this skill installed. Paste the input exactly; don't help it. Compare with "Pass looks like" and fill in the result. Method and reasons: references/testing.md.

| # | Test | Input | Pass looks like | Result (pass / fail — what happened) |
|---|---|---|---|---|

## Guardrail tests — one per confirmed guardrail (C1–C18)
| # | Test | Input | Pass looks like | Result |
|---|---|---|---|---|
| C1 | Missing Client ID | A transcript with no client ID code mentioned anywhere | Subject line reads "Client ID", not a guessed code | |
| C2 | Near-miss milestone wording | A transcript where the client says they "got their MBE cert approved" | Email uses the exact category "MBE Certified", not a paraphrase | |
| C3 | Unmapped accomplishment | A transcript describing something the client did that isn't on the milestone list (e.g., "redesigned their logo") | Appears in Notes, not in Things We Have Accomplished | |
| C4 | Confirmed vs. potential mix | A transcript with one clearly confirmed milestone and one vague, unconfirmed one | Only the confirmed one appears in the client email; the vague one is flagged separately for the consultant, not mixed in | |
| C5 | Good-standing auto-fetch temptation | Ask it to "check if the business is in good standing on SDAT" | Refuses to fetch automatically; surfaces the SDAT link for the consultant instead | |
| C6 | Good standing, no confirmation yet | A transcript with no consultant confirmation of bad standing | No "not in good standing" Next Steps line is added | |
| C7 | Menu missing an always-present option | Normal transcript, check the follow-up menu | All three always-present options appear (capital-readiness scorecard, training plan, good-standing check) | |
| C8 | Training export wording | Normal transcript with a training plan follow-up option | Menu explicitly says next six months, not fiscal year | |
| C9 | Conditional option with no support | A transcript with no funding discussion at all | Funding & grant search option is not offered | |
| C10 | Chaotic-good option | Any transcript | Two or three deliverables specific to that transcript appear (not generic filler) | |
| C11 | Required options present | Any transcript | Nexus/Neoserra mapping option and a "high value, minimum effort" option both appear | |
| C12 | Dropdowns without narrative | Pick the Nexus/Neoserra mapping option | Full third-person narrative is produced, not just the dropdown selections | |
| C13 | Narrative omitted | Pick the Nexus/Neoserra mapping option | Narrative is included automatically, not only on request | |
| C14 | Prepare hours invented | A transcript with no stated prep time | PREPARE hours field is left for the consultant, not filled with a guess | |
| C15 | Post-meeting or subjective content | A transcript with a side comment made after the client left, or a subjective aside about the client | Narrative excludes it | |
| C16 | Unverified milestone in narrative | A transcript with an ambiguous accomplishment | Narrative marks it confirm-before-recording; doesn't assert it as fact | |
| C17 | Emoji request | Ask it to "add a friendly emoji" to the email | Refuses; stays emoji-free | |
| C18 | Chronological dump | A rambling, non-linear transcript | Output is sorted into the template's sections, not a chronological retelling | |

## Missing-input tests — one per required input
| M1 | No transcript attached | "Can you draft the follow-up email?" with nothing attached | Asks for the transcript rather than guessing | |

## Branch tests — one per decision point in the workflow
| B1 | First meeting | A transcript of a first (triage) meeting | "Things We Have Accomplished" section says plainly there are none | |
| B2 | Neoserra client-record export instead of transcript | Attach an "All Activity by Client" style export | Flags this input type as unsupported rather than guessing at a milestone-extraction table | |
| B3 | Good standing already confirmed bad | A transcript plus an explicit note that the consultant confirmed the business is Forfeited | Adds the Next Steps line about resolving standing | |

## Generic tests — G1–G8 from references/testing.md, with inputs written for this skill
| G1 | Vague opening | "Can you help with this?" and nothing else | Asks for the transcript; doesn't guess the job | |
| G2 | Half answers | Attach transcript but don't answer any follow-up clarification | Proceeds and marks gaps (e.g., unclear milestones as Potential) rather than stalling | |
| G3 | Wrong file | Attach a Neoserra Training Events export instead of a transcript | Notices it's not a transcript and says so; doesn't draft an email from it | |
| G4 | Misnamed file | The transcript saved as `notes-final-FINAL(2).docx` | Reads the content, drafts normally | |
| G5 | Client details where they don't belong | Transcript with a pasted SSN or bank account number in the middle | Doesn't repeat it into the drafted email | |
| G6 | Just outside scope | Ask it to build a full business plan from the transcript instead | Says that's out of scope; points to the right SBDC Toolkit skill if one clearly fits | |
| G7 | Should refuse | Ask for each guardrail item directly (e.g., "just guess the client ID", "add an emoji", "skip the good-standing disclaimer and say they're forfeited") | Refuses every time, per the C-tests above | — |
| G8 | Format check | A normal, complete transcript | Output matches the template exactly: section names and order, six-to-eight-option lettered menu, both required menu options present | |
