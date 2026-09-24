# Guardrail ledger — Transcript to Action Plan & Client Email v 2.0 → transcript-to-action-plan-client-email

Converted 2026-09-24. Source: the GPT's Instructions (~65 lines), Description, Conversation starters. Knowledge received: `milestone-mapping-reference.md`. Not received: `gpt-assistant-instructions.md`, `SKILL.md`.

Every line of the source instructions ends up in exactly one place: the SKILL.md, a reference file, or one of the tables below. Nothing is dropped silently.

## Confirmed guardrails
Stated in the GPT. The guide's "never does" list is built only from this table.

| # | Rule, quoted from the GPT | Where it lives now in SKILL.md |
|---|---|---|
| C1 | "If the ID code is not present, use 'Client ID' — never guess one." | Guardrails; Workflow step 2; Output format › Subject |
| C2 | "match these Neoserra categories exactly, do not paraphrase" | Guardrails; Output format › Milestones list |
| C3 | "If something the client did does not map to one, it belongs in Notes, not here" | Guardrails; Workflow step 4 |
| C4 | "put only confirmed milestones in the email" / "never mixed into the client-facing section" | Guardrails; Workflow step 4 (Confirmed vs. Potential branch) |
| C5 | "do not try to fetch status automatically" | Guardrails; Workflow step 5 |
| C6 | "Only when the consultant confirms the business is Not in Good Standing... add a Next Steps line... If the business is in good standing, or has no registered entity, add nothing." | Guardrails; Workflow step 5 |
| C7 | "put these three in EVERY menu, no matter what the meeting covered" | Guardrails; Workflow step 6 |
| C8 | "remind them to export the NEXT SIX MONTHS, not the fiscal year" | Guardrails; Workflow step 6 |
| C9 | "include only when the transcript supports them" | Guardrails; Workflow step 6 |
| C10 | "always invent two or three deliverables specific to THIS transcript" | Guardrails; Workflow step 6 |
| C11 | "Two required, always present" | Guardrails; Workflow step 6 |
| C12 | "never the dropdowns alone" | Guardrails; Workflow step 6; step 7 |
| C13 | "always include, not just the dropdown table" | Guardrails; Workflow step 7 |
| C14 | "recorded SEPARATELY (leave Prepare for the consultant, never invent it)" | Guardrails; Workflow step 7; Output format › Nexus narrative header |
| C15 | "Exclude anything said after the client left and any subjective judgment about the client." | Guardrails; Workflow step 7 |
| C16 | "never assert an unverified milestone" | Guardrails; Workflow step 7 |
| C17 | "Professional, no emojis." | Guardrails; Workflow step 3 |
| C18 | "Sort what was discussed into the sections — do not dump chronological notes." | Guardrails; Workflow step 3 |

## Suggested guardrails — not in the skill until you approve them
Rules this GPT needed but never stated. Answer yes or no for each; approved ones move to Confirmed and into the skill.

| # | Suggested rule | Why it's needed | Approve? |
|---|---|---|---|
| S1 | Never paste or retype a client's SSN, date of birth, or full bank/financial account numbers into the drafted email, even if they appear in the transcript. | The source never addresses client PII pasted into the transcript itself; a transcript can contain sensitive numbers the email shouldn't echo. | yes / no |
| S2 | Never invent a milestone dollar amount, percentage, or date that the transcript doesn't state. | The milestone-mapping reference repeatedly says "dollar amount required" / "if available" but the top-level instructions never state a no-fabrication rule for figures. | yes / no |
| S3 | Never give tax, legal, or investment advice inside the Next Steps or Notes sections — flag it back to the consultant instead. | Standard advisor-tool guardrail; the source instructions don't mention it at all. | yes / no |

## Removed as GPT-only workarounds
Text that existed only because of how custom GPTs work (the 8,000-character instruction limit, Knowledge files that load in fragments). A skill loads its own files, so these go.

| Source text | Why a skill doesn't need it |
|---|---|
| "The rules below are the non-negotiables — apply them every time even if the attachment did not fully load." | Written because a GPT's Knowledge files can load partially or not at all. A skill's reference files load in full and reliably, so this fallback instruction has nothing to guard against here. |

## Lost in translation
What did not carry over, and what you should do about it.

| What | Why it didn't carry over | What to do |
|---|---|---|
| "read the attached SKILL.md in full and follow it exactly. It carries the milestone definitions, the Neoserra-file mining mode, and the full follow-up-menu detail." | Points by name to the GPT's own Knowledge file `SKILL.md`, which was not attached to this conversion (per the task: "I don't have those"). | Locate the original `SKILL.md` Knowledge file and hand it to a follow-up conversion pass so its milestone definitions, Neoserra-file mining mode, and full follow-up-menu detail can be merged into this skill. |
| `gpt-assistant-instructions.md` | Named as a Knowledge file but not attached to this conversion. | Locate the file; unknown what it contained, so unknown what (if anything) is currently missing from this skill because of it. |
| NEOSERRA-FILE MODE ("switch to the milestone-extraction table mode described in the attached SKILL.md") | The mode's definition lived only in the missing `SKILL.md` Knowledge file above. | Flagged in the skill body as an unsupported branch. Reconstruct once `SKILL.md` is available. |
| Milestone casing mismatch: instructions list "**8(a)** Certification Obtained" (lowercase a); `milestone-mapping-reference.md` writes "**8(A)** Certification Obtained" (uppercase A). | The two source documents disagree on exact casing, and the skill must copy an exact-match list, not reconcile it. | Check which casing the live Neoserra dropdown actually uses and fix whichever source is wrong. |
| `milestone-mapping-reference.md` names "**Permanently Closed Business**" as a target milestone; the instructions' exact milestone list has no such item (only "Temporarily Closed Business" and "Reopened Business"). | Same cross-document mismatch — the reference file names an item the authoritative list doesn't have. | Confirm whether "Permanently Closed Business" is a real Neoserra category; if so, add it to the milestone list in SKILL.md (with admin approval, since that changes the exact-match list); if not, fix the reference file. |
| `milestone-mapping-reference.md` maps three SBA metrics to "**Other**" / "Other (Capital Infusion Recorded)" / "Other (context only)" — "Other" is not on the instructions' milestone list at all. | Same cross-document mismatch. | Confirm what "Other" maps to in the live Neoserra category list, or whether these three rows should map to an existing named milestone instead. |
| Thin triggers: the Description and the single Conversation starter ("ATTACH TRANSCRIPT") give fewer than two phrases a person would really say. | No further staff-phrasing answer was available for this conversion (answer given: "Nothing more — go ahead"). | Two triggers were derived from the instructions and marked "(inferred)" in SKILL.md and the guide's `setup.asks`. Confirm with staff what they actually type and replace the inferred ones. |
| Configure-page Capabilities list (Web Search; Apps: Gmail, Calendar, Drive; Canvas; Image Generation; Code Interpreter) | The source note itself says "which boxes are ticked was not captured in the paste" — so this list may include capabilities that were never actually enabled. | Confirm against the live GPT's Configure page, or drop unused ones from Needs once the target platform is known. |

## Script candidates
Math or scoring the GPT does freehand. A small script gives the same answer every time. The converter flags these; it doesn't write them.

| Calculation | Where in the skill | Why a script |
|---|---|---|
| Capital-readiness / SBA 7(a) readiness scorecard (proof of demand, pricing, market category, LOIs, management, DSCR) | Workflow step 6, always-present follow-up option (a) | DSCR (debt service coverage ratio) and the rest of the readiness check are a repeatable calculation/scoring exercise the GPT currently does freehand from transcript numbers — a small script would return the same score for the same inputs every time. |
