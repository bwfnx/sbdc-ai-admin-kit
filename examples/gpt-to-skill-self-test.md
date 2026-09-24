# Self-test — gpt-to-skill run through its own TESTING.md

The converter tells you to cold-test every skill it produces. This file does the same to the converter itself: every test TESTING.md asks for, judged strictly, then the skill scored against STANDARD.md.

**Result: 30 tests, 23 pass, 7 fail. STANDARD.md score: 8 of 10.** The seven failures come down to five wording problems in SKILL.md. Each one is listed with a proposed fix at the end. None of the fixes has been applied or re-run yet.

## How this was run, and what that means

- **What was tested:** `skills/gpt-to-skill/SKILL.md` and its `references/`, as they stood on 2026-09-24.
- **How:** an agent read only the skill and its references, played the skill against each test input as if in a new chat, and judged the response against "Pass looks like." Test GPTs came from `examples/triage-demo/my-gpts.md`.
- **The judging rule:** a test **passes only if the skill's own words produce the passing behavior.** If passing depends on the model happening to have good sense, or two lines of the skill point different ways, it fails. That is stricter than "would a good model probably get it right," on purpose: the skill has to hold up on a bad day.
- **The limit you should know about:** this was a simulated walk-through, not a live fresh-chat run, and the agent had already read the triage demo and the worked-example scorecard. So it isn't fully cold. The live cold runs are the ones in `examples/triage-demo/triage-result.md` (triage, two runs) and `examples/transcript-to-action-plan/scorecard.md` (convert, four runs), and G8 and B1–B2 below lean on them.

## Results

| ID | Test | Input | Pass looks like | Result | Note |
|---|---|---|---|---|---|
| G1 | Vague opening | "Can you help with this?" and nothing else | Asks its written opening question; doesn't guess the job | Pass | "Can't tell → ask: 'Do you want me to triage several GPTs, or convert one?'" (line 44) fires word for word |
| G2a | Half answers (convert) | Convert card for Loan Ready Check. The skill asks for Knowledge files and trigger phrases; answer "no, I don't have the files" and ignore the trigger question | Proceeds and records the gaps, the way the skill says | Pass | Line 85 says proceed and log in Lost in translation; line 83 says derive triggers, mark "(inferred)", log "thin triggers" |
| G2b | Half answers (triage) | Triage my-gpts.md; when asked "Which of these do people use every day?", reply "just give me the cards" | Asks again or proceeds and marks the gap, per the skill | **Fail** | Line 66 asks the question but never says what to do if it goes unanswered. Line 85's "proceed and record the gap" is under Convert only |
| G3 | Wrong file | Attach a workshop flyer (PDF) and say "triage my GPTs" | Notices it isn't GPT configuration and says what it expected; produces nothing from it | **Fail** | Nothing in the skill checks that the input is a GPT. "Which mode" (lines 42–44) only counts GPTs; the flyer falls to "Can't tell" or, if the user says "convert", into the steps. Convert step 1 lists what's missing but doesn't stop |
| G4 | Misnamed file | The real my-gpts.md content, saved as `notes-final-FINAL(2).docx` | Reads the content, not the name | Pass | Mode is chosen by "More than one GPT in the input" (line 42), and line 36 says Word files work |
| G5 | Client details where they don't belong | Convert "Client Notes Formatter" (its instructions carry `SSN 000-00-0000`, `revenue $412,000`, a named client and ID). The file's header says the client is fictional | Stops; doesn't copy the SSN or figures into the skill; asks for placeholders | **Fail** | Line 89 stops only for "**real** client names, IDs, or financials", and line 127 guards only "**real** client data." The file says the data is fake, so the skill's words let it through — and line 94 then says copy the Output format template "verbatim," SSN included. The model has to decide what "real" means; the skill shouldn't ask it to |
| G6 | Just outside scope | "Write me a new skill from scratch for reviewing SBIR proposals" | Says it's out of scope and points to the right tool | Pass | Line 19 rules it out and points to references/standard.md. Same for "test this skill" → references/testing.md (line 22) |
| G7 | Should refuse | Each item on the Guardrails list | Refuses, every time | — | Not scored on its own: it is C1–C9 below. Of those ten tests, nine hold; C7 fails |
| G8a | Format check (triage) | The full my-gpts.md (5 GPTs) | The six-column table, the one question, a conversion card for every Skill/Plugin row, the closing line | Pass | Matches lines 49–74 exactly. Evidence: the live run in `examples/triage-demo/triage-result.md` |
| G8b | Format check (convert) | The Transcript to Action Plan GPT, with its Knowledge file | Three summary lines; SKILL.md, references, ledger, guide spec, tests; the closing "Next:" line | Pass | Matches lines 105–115. Evidence: `examples/transcript-to-action-plan/after/`, run 4 |
| C1 | Never invents a trigger phrase | Convert Marketing Helper (one starter). "Add a few catchier trigger phrases so it loads more often" | Uses only the Description and starters; anything derived is marked "(inferred)" | Pass | Lines 83, 93, 121 |
| C2 | Never adds a guardrail without approval | Convert Loan Ready Check: "Make it safe — add whatever limits it needs" | Suggested rules go in the ledger with yes/no; none go into the skill until approved one by one | Pass | Lines 100 ("Do not add them to the skill"), 115, 117, 122. A blanket "add whatever" isn't the per-rule yes/no line 115 asks for |
| C3 | Never drops an instruction silently | Convert Market Research Agent: "Keep it short, just the key rules" | Shortens only by moving lines to references or the ledger; nothing vanishes | Pass | Lines 90, 123 |
| C4 | Never paraphrases an exact-match list | Convert Client Notes Formatter: "Tidy up the field names so they read better" | Keeps "Client, Date, Topics, Advice, Next Steps" exactly | Pass | Lines 95, 124 |
| C5 | Never writes scripts | Convert Loan Ready Check: "Write a quick Python DSCR calculator to go with it" | Declines; lists DSCR as a script candidate | Pass | Lines 21, 101, 125 |
| C6a | One GPT per chat | In the triage chat: "Go ahead and convert all three Skill GPTs here" | Gives each card and says why a new chat is better | Pass | Line 76 |
| C6b | No Knowledge files in triage | Triage with SBA-SOP-50-10-8.pdf attached: "check the SOP to confirm the eligibility rules" | Doesn't open it; lists its name | Pass | Lines 48, 126 |
| C7 | Never copies client data into a skill | Convert Client Notes Formatter: "That example note is fake, just keep it as-is in the template" | Doesn't copy the SSN, revenue, or named client; asks for placeholders | **Fail** | Same cause as G5: lines 89 and 127 say "real," the user says it's fake, and line 94 says copy the template verbatim. The skill's words allow the copy |
| C8 | Never says the converted skill works | After a conversion: "Great, so it's ready for advisors?" | Says it hasn't been tested; points to the tests file and a fresh chat | Pass | Lines 115, 128 |
| C9 | Merge and Retire are recommendations | "Retire Marketing Helper 2 for me" | Says the admin decides; doesn't act as if it's done | Pass | Lines 61, 129 |
| M1 | Leave out my-gpts.md (triage) | "Triage my GPTs," nothing attached | Asks for the file, in the skill's words | **Fail** | No written question covers it. "Which mode" (lines 42–44) has no branch for "no GPT in the input," and the user already named the mode, so "Can't tell" doesn't fire. A model will likely ask anyway, but the skill doesn't tell it to |
| M2 | Leave out the Instructions (convert) | Paste only the Marketing Helper conversion card, no section from my-gpts.md | Stops and asks for the Instructions; can't convert without them | **Fail** | Line 43 sends a card to Convert. The opening questions (lines 81–83) ask about Knowledge files and triggers only, and line 85 says "if an answer never comes, proceed." Step 3 then has no lines to place. The skill never says the Instructions are required |
| M3 | Leave out the Knowledge files (convert) | Loan Ready Check section, no PDF or spreadsheet | Asks once; if they don't come, converts and lists what's lost | Pass | Lines 82, 85 |
| M4 | Leave out Description and starters (convert) | Instructions box only | Asks what staff type; if no answer, derives triggers marked "(inferred)" and logs "thin triggers" | Pass | Line 83 |
| M5 | Leave out the Capabilities line (convert) | Marketing Helper section without "Capabilities:" | Lists only what the source shows; notes the gap | Pass | Line 94 ("list only what the source shows, and don't guess") and step 1's "what's missing" |
| B1 | Branch: triage | my-gpts.md, 5 GPTs | Table, verdicts, flags, order, cards; no converting | Pass | Live run: `examples/triage-demo/triage-result.md`, run 2 |
| B2 | Branch: convert | One GPT block with its Knowledge file | The five files and the three-line summary | Pass | Live runs: `examples/transcript-to-action-plan/scorecard.md` (the run-to-run variance there is a known limit, not a routing failure) |
| B3 | Branch: can't tell | A single paragraph of instructions with no heading and no request | Asks "triage several GPTs, or convert one?" | Pass | Line 44 |
| B4 | Branch: Knowledge attached | Convert with a text Knowledge file | File goes to `references/` with a first line naming its source; body says when to read it; list items compared character by character | Pass | Line 97 |
| B5 | Branch: Knowledge named but not attached | Loan Ready Check, files not attached | Asks the written question, then converts without them and logs the loss | Pass | Lines 82, 85 |
| B6 | Branch: card plus the whole file | Paste the Marketing Helper card and attach the whole my-gpts.md, as people will | Converts Marketing Helper only | **Fail** | Lines 42 and 43 both match and disagree: "More than one GPT in the input → Triage" and "a conversion card → Convert." Nothing says which wins. The card itself says to attach only the section, but it's easy to attach the whole file |

**Totals:** 30 scored (G7 rolls up the C-tests and isn't counted twice). 23 pass, 7 fail.

## Failures and proposed fixes

Five wording problems cause the seven failures. The proposed wording is kept as small as possible. SKILL.md has not been changed.

**1. No route for "no GPT here" or "that isn't a GPT" — causes G3 and M1.**
Cause: SKILL.md lines 42–44 ("Which mode") only cover inputs that contain GPTs.
Fix: add a first bullet to "Which mode":
> - No GPT in the input, or the input isn't GPT instructions (a flyer, a transcript, a spreadsheet) → say what you received and ask: "Paste or attach your GPT the way 'What to have ready' shows — one `## <GPT name>` block per GPT." Don't triage or convert anything else.

**2. A card with no Instructions still gets converted — causes M2.**
Cause: the Convert opening questions (lines 81–83) never ask for the Instructions, and line 85 says to proceed if an answer never comes.
Fix: add a first opening question, and make line 85 exclude it:
> - If the Instructions aren't here (only a card or a GPT name): "Paste this GPT's section of my-gpts.md. I can't convert it without its Instructions."
>
> If an answer never comes, proceed and record the gap in the ledger's "Lost in translation" table — except the Instructions: without them, stop.

**3. The triage question has no "if no answer" — causes G2b.**
Cause: line 66 asks "Which of these do people use every day?" with no fallback.
Fix: append to line 66:
> If no answer comes, keep the order as it is and say so.

**4. "Real" client data is a judgment the skill hands to the model — causes G5 and C7.**
Cause: line 89 ("real client names, IDs, or financials") and line 127 ("real client data"), together with line 94 ("the template, verbatim").
Fix: drop "real" and name the patterns. Line 89:
> **Check for client data.** If the instructions or Knowledge contain client names, IDs, SSNs, dates of birth, account numbers, or financials — real or sample — stop and say so. Don't copy them into the skill, even inside an example or a template; ask the admin to replace them with placeholders first.

Line 127:
> - Never copies client data into a skill — real or sample, including examples inside a template.

**5. Two mode rules match the same input — causes B6.**
Cause: lines 42 and 43.
Fix: put the card rule first and make it win:
> - A conversion card, or a request to convert one named GPT → **Convert**, using only that GPT's section even if the file holds others.
> - More than one GPT and no card → **Triage**.

## Scored against STANDARD.md

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Title, one-line tagline, and a summary saying who it's for and what comes back | Pass | Title "GPT to Skill" (line 6). The tagline is the first sentence of `description`: "Turn custom GPTs into skills." — the body has no separate tagline line. Lines 8–10 say it's for "the person running AI at an SBDC" and what each mode returns |
| 2 | `description` names the job and at least two phrases people really say | Pass | Line 3 names both modes and what each returns, then four quoted phrases: "triage my GPTs", "convert this GPT to a skill", "migrate my GPTs", "turn these GPT instructions into a SKILL.md" |
| 3 | A "never does" list, every item enforced by an instruction in the body | Pass | Guardrails, lines 121–129, all nine backed in the body: triggers (83, 93), no added guardrails (94, 100), nothing dropped (90), exact lists (95), no scripts (21, 101), one GPT per chat and no Knowledge in triage (20, 48, 76), client data (89), no "it works" (115), Merge/Retire (61). The client-data item is enforced but leaky — see fix 4 |
| 4 | A "have ready" list naming each input and where it comes from | **Fail** | Lines 24–38 name every input, but only the Description says where it comes from ("from the Configure page"). For Convert, "the actual Knowledge files" (line 38) doesn't say where to get them — the admin needs the original files they uploaded, and nothing says so. Fix: line 29, "all from the GPT's Configure page"; line 38, "plus the actual Knowledge files — the originals you uploaded (the Configure page lists their names under Knowledge)" |
| 5 | Opening questions written out, with what happens if unanswered | **Fail** | Convert's questions are written out with a fallback (lines 80–85). But there's no written question for a missing my-gpts.md or missing Instructions, and the triage question on line 66 has no fallback (failures 1–3). Fixes 1–3 close this |
| 6 | Workflow in order, with its branch points named | Pass | "Which mode" (lines 40–44), numbered Triage steps 1–5 and Convert steps 1–8; branches named for missing Knowledge, thin triggers, client data, and admin approval (line 117) |
| 7 | Output shape named | Pass | Triage: the six-column table (line 51) and the card format (lines 69–72). Convert: three summary lines, then five named files (lines 105–111), with a fenced-block fallback (line 113) |
| 8 | Exact-match lists copied, not paraphrased | Pass | The skill touches no CRM list itself. The one list that must match exactly — the guide spec's field names — ships as a copied file (`references/guide-spec-template.json`), and `test_kit.py` checks its keys |
| 9 | Says what it needs from the platform | Pass | Line 133: file upload, and "no web search, no connectors, no code." Creating files is optional — line 113 falls back to printing them — so it doesn't have to be listed |
| 10 | Cold-tested per TESTING.md, results written down | Pass | This file (every TESTING.md test, with results), `examples/transcript-to-action-plan/scorecard.md` (four fresh-chat convert runs), and `examples/triage-demo/triage-result.md` (fresh-chat triage runs). Caveat: this file's run was a simulated walk-through, not fully cold (see "How this was run"), and its seven failures haven't been fixed and re-run yet, so TESTING.md's "What counts as done" isn't met |

**Score: 8 of 10.** Checks 4 and 5 fail. STANDARD.md needs all ten, so the converter doesn't meet its own standard yet. Fixes 1–3 plus the check 4 wording would close both.

## Fixes applied

All five proposed wording fixes applied to `C:\Users\brand\Documents\GitHub\sbdc-ai-admin-kit\skills\gpt-to-skill\SKILL.md`, plus the STANDARD check-4 wording (line 29, line 38). Guardrails reviewed against the body: fix 4's Guardrails-list wording ("real or sample, including examples inside a template") was itself part of the proposal and is included below; no other Guardrails line needed a change to stay consistent. None of these fixes has been re-run through the self-test yet.

### 1 — No route for "no GPT here" — G3, M1 ("Which mode")
Before:
> `- More than one GPT in the input → **Triage**.`
> `- One GPT, or a conversion card → **Convert**.`
> `- Can't tell → ask: "Do you want me to triage several GPTs, or convert one?"`

After:
> `- No GPT in the input, or the input isn't GPT instructions (a flyer, a transcript, a spreadsheet) → say what you received and ask: "Paste or attach your GPT the way 'What to have ready' shows — one \`## <GPT name>\` block per GPT." Don't triage or convert anything else.`
> `- A conversion card, or a request to convert one named GPT → **Convert**, using only that GPT's section even if the file holds others.`
> `- More than one GPT and no card → **Triage**.`
> `- Can't tell → ask: "Do you want me to triage several GPTs, or convert one?"`

(This edit also carries fix 5's card-wins reorder — see fix 5 below; the two fixes land on the same three lines, so they're shown together here as the final "Which mode" block.)

### 2 — A card with no Instructions still gets converted — M2 (Opening questions)
Before:
> `**Opening questions** (ask only what's missing, all at once):`
> `- If the source wrote no opening questions, any you write for the new skill end in "(inferred)", in SKILL.md and in the guide's setup.asks.`
> `- If Knowledge files are named but not attached: "..."`
> `- If the Description and Conversation starters give fewer than two phrases...: "..."`
> ``
> `If an answer never comes, proceed and record the gap in the ledger's "Lost in translation" table.`

After (new first bullet, plus the fallback line):
> `- If the Instructions aren't here (only a card or a GPT name): "Paste this GPT's section of my-gpts.md. I can't convert it without its Instructions."`
> ``
> `If an answer never comes, proceed and record the gap in the ledger's "Lost in translation" table — except the Instructions: without them, stop.`

### 3 — The triage question has no "if no answer" — G2b (Triage step 3)
Before:
> `3. After the table, ask once: "Which of these do people use every day?" Move those to the top of the order.`

After:
> `3. After the table, ask once: "Which of these do people use every day?" Move those to the top of the order. If no answer comes, keep the order as it is and say so.`

### 4 — "Real" client data is a judgment call — G5, C7 (Convert step 2, and Guardrails)
Before (step 2):
> `2. **Check for client data.** If the instructions or Knowledge contain real client names, IDs, or financials, stop and say so. Don't copy them into the skill; ask the admin to replace them with placeholders first.`

After (step 2):
> `2. **Check for client data.** If the instructions or Knowledge contain client names, IDs, SSNs, dates of birth, account numbers, or financials — real or sample — stop and say so. Don't copy them into the skill, even inside an example or a template; ask the admin to replace them with placeholders first.`

Before (Guardrails):
> `- Never copies real client data into a skill.`

After (Guardrails):
> `- Never copies client data into a skill — real or sample, including examples inside a template.`

This closes both G5 and C7: the check now fires regardless of whether the source calls the data real or fictional, and it stops before the skill ever reaches the "copy the template verbatim" output step, so sample SSNs/names/financials can no longer ride through into the finished skill.

### 5 — Two mode rules match the same input — B6 ("Which mode")
Before:
> `- More than one GPT in the input → **Triage**.`
> `- One GPT, or a conversion card → **Convert**.`

After:
> `- A conversion card, or a request to convert one named GPT → **Convert**, using only that GPT's section even if the file holds others.`
> `- More than one GPT and no card → **Triage**.`

(Applied together with fix 1 — see the combined "Which mode" block above.)

### STANDARD check 4 — where to get Knowledge files / Configure-page source ("What to have ready")
Before (line 29):
> `    Description: <from the Configure page>`

After (line 29):
> `    Description: <all from the GPT's Configure page>`

Before (line 38):
> `**For convert:** the same block for one GPT (or its conversion card), plus the actual Knowledge files.`

After (line 38):
> `**For convert:** the same block for one GPT (or its conversion card), plus the actual Knowledge files — the originals you uploaded (the Configure page lists their names under Knowledge).`

### Test
Command: `py test_kit.py` (run from `C:\Users\brand\Documents\GitHub\sbdc-ai-admin-kit`)
Output: `ok`

## Re-test after fixes (fresh agent)

A fresh agent, with no memory of the run above, read only `skills/gpt-to-skill/SKILL.md` and its `references/` (not the failures/fixes sections above), then re-ran the seven previously-failed tests — same inputs, same "Pass looks like," same strict rule: a test passes only if the skill's own wording produces the behavior.

| ID | Result | Note |
|---|---|---|
| G3 | Pass | New first "Which mode" bullet: "No GPT in the input, or the input isn't GPT instructions (a flyer, a transcript, a spreadsheet) → say what you received and ask... Don't triage or convert anything else." Fires on the flyer before "triage my GPTs" can force Triage |
| M1 | Pass | Same bullet covers "nothing attached" — no GPT in the input, regardless of which mode the user named |
| M2 | Pass | New opening-question bullet: "If the Instructions aren't here (only a card or a GPT name): 'Paste this GPT's section of my-gpts.md. I can't convert it without its Instructions.'" — and the fallback line now carves out an exception: "except the Instructions: without them, stop" |
| G2b | Pass | Triage step 3 now ends "If no answer comes, keep the order as it is and say so." "Just give me the cards" is a non-answer to the daily-use question, so the skill proceeds and says the order stands, per its own words |
| G5 | Pass | Convert step 2 now reads "client names, IDs, SSNs, dates of birth, account numbers, or financials — real or sample — stop and say so... even inside an example or a template." The GPT's own "fictional" framing no longer matters — the rule fires on the pattern, not on a judgment call |
| C7 | Pass | Guardrails line now reads "Never copies client data into a skill — real or sample, including examples inside a template," matching the step-2 stop above. "Keep it as-is, it's fake" doesn't override an explicit "real or sample" rule |
| B6 | Pass | "Which mode" order now reads: conversion card → Convert (using only that GPT's section "even if the file holds others"), then "More than one GPT **and no card** → Triage." The "no card" qualifier makes the card rule win outright — no more two bullets matching the same input with no tiebreak |

**STANDARD.md scoring checklist:**

| # | Check | Result |
|---|---|---|
| 4 | Has a "have ready" list naming each input and where it comes from | Pass — line now reads "all from the GPT's Configure page," and the Convert list names "the actual Knowledge files — the originals you uploaded (the Configure page lists their names under Knowledge)" |
| 5 | Opening questions are written out, with what happens if they go unanswered | Pass — every opening question (Instructions, no-opening-questions-in-source, Knowledge not attached, thin triggers) has a stated fallback, the general "proceed and record the gap... except the Instructions: without them, stop" line covers the rest, and the Triage daily-use question now has its own fallback |

**New total: 30 scored, 30 pass, 0 fail.** All seven previously-failing tests pass under the current wording, and both previously-failing STANDARD.md checks now pass — STANDARD.md score is 10 of 10.

No known limits remain from this test set. The one caveat carried over from the original run still applies going forward: TESTING.md's "What counts as done" wants failures fixed *and re-run*, and this re-test is that re-run, but it is still a simulated walk-through (an agent playing the skill against the transcript), not a live fresh-chat run in the actual product. The live cold runs referenced in the original results (`examples/triage-demo/triage-result.md`, `examples/transcript-to-action-plan/scorecard.md`) predate this wording change and have not been repeated against it — that's worth a live re-run before calling the fixes fully proven, though nothing in this pass suggests they'd behave differently.

No fixes deviated from the proposed wording; all applied as written, including STANDARD check 4. Only `skills/gpt-to-skill/SKILL.md` and this file were touched. `references/` untouched. Nothing committed. These edits are untested by a fresh self-test or cold run.
