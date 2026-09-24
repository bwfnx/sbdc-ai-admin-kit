# Scorecard — converting "Transcript to Action Plan & Client Email v 2.0"

Note: gpt-to-skill was tightened again after this run, by the self-test (examples/gpt-to-skill-self-test.md). This file shows the run as it happened.

**Result: FAIL, narrowly.** Every loss that changes what the skill does is flagged in the ledger. Two small descriptive phrases were trimmed without a note, and the pass bar allows no unflagged losses. Four runs of the converter also gave noticeably different results. Check the items at the end by hand on every conversion.

**What went in:** the GPT's Instructions, Description, and Conversation starter, plus one Knowledge file (milestone-mapping-reference.md). **What was held back:** the GPT's other two Knowledge files — one *is* the original skill and the other is a copy of the instructions, so including them would have handed the converter the answer.

**What it's scored against:** the original toolkit skill this GPT was ported from.

The converter ran four times, each time in a fresh chat. Its own instructions were tightened between runs (see the last section). This scores the **fourth and final run**, which is what's in `after/`. The GPT was already a shortened copy of the original skill, so some things were gone before the converter saw them. Those are in their own table, **Lost before conversion**, and don't count against the converter. Everything in **Lost** was either in what the converter received or pointed to by it, so the ledger should have flagged it.

## Recovered
| In the original skill | In the converted skill | Match (exact / close / partial) |
|---|---|---|
| Opening paragraph: this email *is* the Neoserra record, and a missed milestone is data that never gets counted | Purpose paragraph | Close |
| Voice: first person as the consultant, professional, no emojis, wording fitted to the meeting, sorted into sections instead of chronological notes | Workflow step 3; Guardrails | Close |
| The email template (Subject, greeting, Next Steps, Notes, Things We Have Accomplished Since Our Last Meeting, Relevant Links, signature block) | Output format | Exact — the fill-in hints in brackets differ by a word or two |
| Subject line: client ID if it's in the transcript, otherwise "Client ID", never a guess | Workflow step 2; section notes; Guardrails | Exact |
| What goes in Next Steps, Notes (detailed checklists, "not a one-line summary"), Things We Have Accomplished, and Relevant Links | Output format › section notes; Workflow step 4 | Close |
| Maryland good-standing click-through: don't fetch it, give the SDAT link, add a Next Steps line only when the consultant confirms a problem | Workflow step 5; Guardrails | Close |
| The Neoserra milestone list, matched exactly | Output format, milestone list | Partial — 34 of the original's 35 names, copied word for word from the GPT. The ledger flags the one spelled differently (see Lost) |
| "If it doesn't map to a milestone, it goes in Notes"; confirmed milestones only in the email, possible ones in a separate note | Workflow step 4; Guardrails | Exact |
| Pointer to references/milestone-mapping-reference.md | What to have ready; after the milestone list; the file itself copied into references/ with a line saying where it came from | Exact |
| Follow-up menu: six to eight lettered options, "so the consultant can continue by naming a letter" | Workflow step 6 | Exact |
| The three always-present options (capital-readiness scorecard "as a proactive check", training plan with the six-month export, good-standing check) | Workflow step 6; Guardrails | Close — names and key reminders kept; the how-to detail isn't (see Lost) |
| The conditional options: funding search run live through the Maryland Community Business Compass connector when it's there, and hand-off to another toolkit skill | Workflow step 6; Guardrails | Close |
| Two or three "chaotic-good" options invented for this transcript, and the two required options (map to Nexus/Neoserra; "high value, minimum effort") | Workflow step 6; Guardrails | Close |
| The Nexus/Neoserra session narrative: header fields, Contact and Prepare hours separate, Prepare never invented, nothing said after the client left, no judgment of the client, milestones *and referrals* confirm-before-recording | Workflow step 7; Guardrails | Close — nearly word for word |
| Mining milestones from a Neoserra client file (a second mode for when there's no transcript) | "When to use it — and when not to"; Workflow step 8 | Partial — the skill says plainly it can't do this mode yet, and the ledger says why |

## Lost
Things the converter received, or that the GPT pointed to by name. Each should be flagged in the ledger.

| In the original skill | Why it was lost | Did the ledger flag it? |
|---|---|---|
| How to mine a Neoserra client file: the table's columns, one row per milestone, "[unknown]" for missing dates, a separate table of possible milestones, working through a long PDF ten pages at a time | The GPT pointed to the held-back file for it | **Yes** — Lost in translation, rows 1 and 3, quoting the GPT's pointers |
| A running table of client testimonials found in the file | Part of the same mode; the reference file also mentions a "Testimonials Table" | **Yes, in general** — covered by the Neoserra-file mode rows, not named |
| How to run the always-present menu options in depth: the scorecard's "fix this before you see a lender" list, investor use, and the hand-off to the Underwriter and Capital Coach skill; the training plan's top-ten list with dates, reasons, and a client-ready version; hand-offs limited to the one or two that fit | The GPT kept only the option names and pointed to the held-back file for "the full follow-up-menu detail" | **Yes** — row 1, quoting that phrase |
| One milestone name: "Responded to SBA Impact Survey (CY 2015)" | The GPT's list left it out and pointed to the held-back file for "the milestone definitions" | **Yes, in general** — row 1 quotes "the milestone definitions"; it doesn't warn that a name might be missing |
| The spelling "8(A) Certification Obtained" (the converted skill says "8(a)") | The GPT wrote "8(a)"; the reference file writes "8(A)" | **Yes** — row 4. Rows 5–6 also flag names in the reference file that aren't on the list |
| The range of ways to start the skill (flag milestones, draft a next-steps email, summarize a meeting, map to Neoserra dropdowns) | The GPT had one conversation starter and a one-line description | **Yes** — row 7 ("thin triggers"); two added phrases are marked "(inferred)" |
| "This is where the skill earns its keep" (about the chaotic-good options), and "~700 Maryland programs" (what the funding connector searches) | The converter trimmed these phrases. The rules around them are kept | **No** — minor. Neither changes what the skill does |

## Lost before conversion
In the original skill, but the GPT's instructions never mentioned it or pointed to it. No converter could recover these. They're listed so you know what to add back by hand, and they don't count against the pass bar.

| In the original skill | What the GPT did with it |
|---|---|
| What the skill is *not* for: internal meeting notes, or a re-engagement email to a lapsed client | Left out |
| Word milestones plainly rather than in transcript jargon | Left out |
| Notes "focus on what the client should do next" | Left out |
| The Maryland Business Express web address for filing late reports | Kept the name, dropped the address |
| Returning *or referred* clients attach to their existing record | Kept "returning" only |
| Examples of economic impact (jobs, capital, sales, business formed) | Left out |
| The funding-search hand-off: the original sends grant-readiness work to the Funding Match skill *as well as* running the live search | Changed it to a fallback only when the connector isn't there |
| The author's note about two spellings of the accomplishments heading | Left out — it was a note to the author, not an instruction, so nothing is lost in practice |

## Added
| In the converted skill, not in the original | Good or bad |
|---|---|
| "When to use it — and when not to": the GPT's own "never" rules, plus a plain note that Neoserra client-record exports aren't supported yet | Good — nothing here narrows the job beyond what the GPT said. The first four bullets repeat the Guardrails rather than naming neighboring jobs, which is harmless |
| An opening question asking for the transcript, marked "(inferred)" | Good |
| A numbered 8-step Workflow with its branch points named | Good |
| Guardrails: 18 rules, every one traced to the GPT's own words, no made-up ones | Good |
| The capital-readiness scorecard and DSCR flagged as a script candidate | Good |
| Three suggested guardrails in the ledger (don't repeat SSNs or account numbers; don't invent figures; no tax, legal, or investment advice), kept out of the skill until approved | Good |
| "A first meeting has no milestones — say so plainly"; "if there's no registered entity, add nothing"; "resolve garbled referral names" | Good — from later edits to the GPT, carried over faithfully |
| A Needs section listing the GPT's Configure-page capabilities, clearly labeled as unconfirmed | Mostly good. It leaves out the Maryland Community Business Compass connector, which the Workflow uses and the guide lists |
| The guide's trigger list includes the GPT's one-line Description sentence as if it were something people type, and leaves out the two inferred phrases the skill's description adds. The ledger says those phrases went into the guide's opening questions, which isn't so | Bad, minor — fix the guide's trigger list by hand |

## Verdict
The converted skill drafts the client email, follows the milestone rules, builds the follow-up menu, and writes the Nexus narrative almost exactly as the original does. Its ledger honestly flags the missing Neoserra-file mode, the missing menu detail, the thin trigger phrases, the milestone-name mismatches, and the DSCR math. A Maryland admin would still need to rebuild the Neoserra-file mode once the original file is found, check "8(a)" against Neoserra, fix the guide's trigger list, add the connector to Needs, and add back the "Lost before conversion" items by hand. Because results vary from run to run, the checks below are not optional.

## Converter fixes made because of this scorecard
- **Round 1 (six changes):** script candidates cover any math or scoring; thin trigger phrases get asked about and logged; the Confirmed table needs a row for every never / don't / no / only / always; list mismatches between a Knowledge file and the instructions get logged; guide fields and Needs say only what the source states; pointers to missing Knowledge files get quoted in the ledger.
- **Round 2 (four changes):** compare every list item in each Knowledge file character by character; nothing goes in Guardrails but Confirmed rules, and gaps from missing files become Workflow notes; every clause, not just every line, has to land somewhere, with a re-read at the end; the guide's "never" list covers every Confirmed rule that forbids something.
- **Round 3 (four changes):** script candidates are any ratio or score the source names anywhere, including menu options; "When not to use it" may only list what the source rules out, and no restriction goes anywhere without approval; the guide's "never" list has one line per Confirmed row; converter-written opening questions are marked "(inferred)".

**What the fourth run showed.** All mechanical checks passed: the guide spec parses, the ledger has its five sections, the GPT-only workaround is gone, the 34 milestone names are copied word for word, the Neoserra-file mode is in Lost, and DSCR is a script candidate. For the first time, none of the bigger problems showed up in the same run: no made-up restriction, the "always" rules are in the Confirmed table, referrals and "not a one-line summary" are kept, and the opening question is marked "(inferred)". What's left is small: two trimmed phrases, the guide's "never" list at 16 lines for 18 rules (one "always" rule missing and two near-duplicates merged), the guide's trigger list, and the connector missing from Needs.

**Variance between runs.** The same converter, given the same input, gave these results:

| | Run 1 | Run 2 | Run 3 | Run 4 |
|---|---|---|---|---|
| Confirmed guardrails | 9 | 15 | 18 | 18 |
| "Always" rules in the Confirmed table | No | Yes | No | Yes |
| Script candidates (DSCR / scorecard) | 0 | 1 | 0 | 1 |
| Rows in Lost in translation | 4 | 4 | 8 | 8 |
| 8(a)/8(A) mismatch flagged | No | No | Yes | Yes |
| Made-up rule or restriction in the skill | No | Yes (a guardrail) | Yes (a "when not to use" line) | No |
| "Referrals" kept in confirm-before-recording | Yes | No | Yes | Yes |
| Guide lists "exclude anything said after the client left" | Yes | No | No | Yes |
| Converter-written opening questions marked "(inferred)" | Yes | Yes | No | Yes |
| Small phrases trimmed without a note | None found | 4 | 1 | 2 |
| Pass bar | FAIL | FAIL | FAIL | FAIL (narrowly) |

The run's own summary line gave a different Lost in translation count than its table in runs 3 and 4 (it said 7; each table has 8 rows). Count the table, not the summary.

## Known limits
- **Results vary from run to run.** A fix that holds in one run can slip in the next. Two examples: the "always" rules made the Confirmed table in 2 of 4 runs, and DSCR was flagged in 2 of 4. The last round of wording changes was tested by only one run.
- **Small trims happen.** Every run after the first dropped a phrase or two without a note, and it was a different phrase each time. So far none has been a rule in the final run, but check.
- **The guide's "never" list and trigger list drift from the ledger.** Check them against the Confirmed table and the skill's description.
- **Anything the GPT had already dropped can't come back.** That's the "Lost before conversion" table. Only the original source can restore it.
- **One GPT.** This is one worked example. It shows how the converter behaves; it doesn't prove it on every GPT.

## Check these by hand on every conversion
1. **Script candidates:** every ratio, score, or scorecard the GPT names anywhere, menu options included, should have a row.
2. **"When to use it — and when not to":** nothing should narrow what the GPT said the skill does.
3. **The Confirmed table:** every never / don't / only / always rule in the GPT should have a row. Pay particular attention to the "always" rules.
4. **The guide's "never" list:** one line for each Confirmed row.
5. **The guide's trigger list:** only phrases people actually type, matching the skill's description.
6. **Trimmed wording:** read the GPT's instructions against the converted skill once, looking for dropped clauses.
7. **Lost in translation:** act on every row, especially missing Knowledge files.
8. **Exact-match lists** (milestones, dropdowns): check them against the live Neoserra screen.
9. **Needs:** every connector the Workflow uses should be listed.
10. **The cold-test checklist:** run it in a fresh chat before anyone relies on the skill.
