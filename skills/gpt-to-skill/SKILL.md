---
name: gpt-to-skill
description: Turn custom GPTs into skills. COLLECT mode takes the GPT files themselves, attached (Word, text, or Markdown, one per GPT), builds my-gpts.md, hands it back, and sorts it. TRIAGE mode takes every GPT's instructions at once (one my-gpts.md file, a "## GPT Name" heading over each) and sorts each into Skill, Plugin, Agent, Merge, or Retire, flags the risky ones, and writes a conversion card for each. CONVERT mode takes one GPT per chat (its Instructions, Description, Conversation starters, and Knowledge files) and returns a SKILL.md, a guardrail ledger, a staff-guide spec, and a cold-test checklist. Use when someone says "triage my GPTs", "convert this GPT to a skill", "migrate my GPTs", "turn these GPT instructions into a SKILL.md", or pastes a conversion card.
---

# GPT to Skill

Custom GPTs are being retired (OpenAI's date for Enterprise workspaces is December 11, 2026; Business workspaces show the same notice). This skill moves them to skills without losing what made them work: the questions they ask, the things they refuse, and the format they hand back. It is for the person running AI at an SBDC, not for advisors.

It has three modes. **Collect** turns a pile of attached GPT files into one `my-gpts.md`. **Triage** looks at all your GPTs at once and decides what each should become. **Convert** turns one GPT into a skill, in its own chat.

> Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.

## When to use it — and when not to

Use it to migrate a custom GPT, or any long system prompt, into a skill.

Don't use it to:
- write a brand-new skill from scratch — write against references/standard.md instead;
- convert more than one GPT in one chat;
- write scripts (it flags where one belongs);
- test a skill — that's references/testing.md, in a fresh chat.

## What to have ready

**For triage:** your GPT files, attached (Word, text, or Markdown; one per GPT, named for the GPT; ten per message), or one file, `my-gpts.md`, with every GPT in it like this:

    ## <GPT name>
    Description: <all from the GPT's Configure page>
    Conversation starters: <each one>
    Knowledge files: <file names only>
    Capabilities: <web search, code interpreter, image generation, canvas, apps like Gmail or Drive, any Actions>

    <the full Instructions box, pasted as-is>

Markdown or plain text is best. Word files work but add nothing. Already saved each GPT as its own Word file? Attach them and Collect mode (below) builds `my-gpts.md` for you with `scripts/gpts-to-md.py`; on your own computer the same script combines a whole folder in one step. Or paste them into one file yourself, a `## <GPT name>` heading over each. The Instructions box alone is enough for triage. One file avoids per-message upload limits, and GPT instructions are capped at 8,000 characters each, so even thirty GPTs fit.

**For convert:** the same block for one GPT (or its conversion card), plus the actual Knowledge files — the originals you uploaded (the Configure page lists their names under Knowledge).

## First reply

Open every first reply with "Here's what happens." and the one line for the mode you are in, then the two shared sentences, before any question or table:

- **Collect** (several GPT files attached): "I'll combine these into one `my-gpts.md`, hand it back, then sort it. Ten files per message; say 'more coming' between batches and 'that's all' when done. Attach only the GPT files, not their Knowledge files."
- **Triage** (several GPTs in one file): "One table saying what each should become and in what order, one question, then a conversion card per keeper. Two replies."
- **Convert** (one GPT): "I rebuild it as a skill and hand back the skill file, a ledger of what I kept, dropped, or suggest adding, a staff-guide spec, and a test list. A question first if something's missing."

In Collect and Triage, add: "**Skill** and **Plugin** are the kit's verdicts (Plugin = needs a script or ships templates), not OpenAI's Migrate button; both get a card."

Always, last: "On ChatGPT, a finished skill goes into its own Project: paste its SKILL.md into the instructions, upload its references folder, and test it there. If advisors stay on the Migrate button's plugin, test that plugin with the same list."

Then the mode's own opening.

## Which mode

Take the first line that fits, on the first message; once Collect has started, stay in it until "that's all".

- No GPT in the input, or the input isn't GPT instructions (a flyer, a transcript, a spreadsheet) → say what you received and ask: "Paste or attach your GPT the way 'What to have ready' shows — one `## <GPT name>` block per GPT, or the GPT files themselves." Don't triage or convert anything else.
- A conversion card, or a request to convert one named GPT → **Convert**, using only that GPT's section even if the file holds others. Attached files are then Knowledge files, except the one that holds the GPT's Instructions (`my-gpts.md` or the one GPT file).
- Several attached GPT files (.docx, .txt, .md), no `my-gpts` file, and no card → **Collect**, then Triage.
- One attached file holding a single GPT (not several `## <GPT name>` blocks), no card, no request to convert, and no "more coming" or "that's all" → ask: "Do you want me to convert this one GPT, or is there more to sort?"
- More than one GPT and no card → **Triage**.
- Can't tell → ask: "Do you want me to triage several GPTs, or convert one?"

## Collect

1. A batch with "more coming", or a full batch of ten with no note: give the first-reply intro if this is the first message, then only: "Got <N> so far. More coming? Send the next batch, and say 'that's all' when done." Combine nothing yet.
2. On "that's all", or a batch of fewer than ten with no note: run `scripts/gpts-to-md.py` on every GPT file attached so far in this chat, by name, with `-o my-gpts.md`. Name the files; never run it on the whole folder, which holds this skill's own files. If more files arrive after a triage, combine everything received so far and triage the whole set again; Merge only shows across the full set.
3. Hand back `my-gpts.md` as a download and say to keep it (the conversion cards attach its sections), repeat the script's "skipped:" lines verbatim if there are any, and go straight into Triage on it in the same reply.
4. No Python here? Say so in one line, print the combined file as a fenced block headed `my-gpts.md` (a `## <file name>` heading over each file's text, in the order attached, with any heading inside a file's text pushed down two levels), tell the admin to save it under that name, and triage from that text.

Collect reads only the attached GPT files. It never opens Knowledge files.

## Triage

1. Read only the instructions, descriptions, starters, and file lists. **Never open Knowledge files in triage**, even if attached — list their names. Opening them is what overflows the chat.
2. Build one table:

   | # | GPT | Purpose (one line) | Verdict | Flags | Order |
   |---|---|---|---|---|---|

   **Verdict** — pick one:
   - **Skill** — one focused, repeatable job the instructions carry on their own.
   - **Plugin** — belongs in a set with related GPTs, ships templates, or needs a script for math or scoring.
   - **Agent** — needs multi-step research, several tools used in sequence, or runs unattended.
   - **Merge** — does the same job as another GPT in the file with minor variation; name the one to keep.
   - **Retire** — superseded by a built-in feature, or so thin a plain prompt does it.

   Merge and Retire are recommendations. The admin decides.

   **Flags** — any that apply: `knowledge` (depends on Knowledge files), `client-data` (handles client names, IDs, or financials), `web/apps` (uses web search, app connectors, or Actions), `no-refusals` (its instructions contain no "don't", "never", or "only" limit on what it will do — check every GPT for this, including ones that sound harmless), `math` (calculates or scores).

   **Order** — simplest first: Skills with the fewest flags, then Plugins. Agents last. Under the table, print one line: "Flags mark what to check before advisors use it, not what to drop. Plugin is packaging advice, not a blocker: the Migrate button works on it like any other."
3. After the table, ask once: "Which of these do people use every day?" Move those to the top of the order. If no answer comes, keep the order as it is and say so. Skip this question when there is only one GPT.
4. Write a **conversion card** for every Skill or Plugin row:

       Convert this GPT to a skill: <GPT name>
       Triage verdict: <Skill | Plugin> — <one-line reason>
       Flags: <flags>
       Attach: the "<GPT name>" section of my-gpts.md, and Knowledge files: <names, or "none">

5. End with: "Have the Migrate button? Press it on each keeper, then check each result with STANDARD.md and TESTING.md; the cards are for converting without the button, or for getting a ledger of what survived. Converting without it: open a **new chat** per card, because converting here would crowd this chat and the quality drops."

**Triage never converts.** If asked to convert in the triage chat, give that GPT's card and say why a fresh chat is better.

## Convert

**Opening questions** (ask only what's missing, all at once):
- If the Instructions aren't here (only a card or a GPT name): "Paste this GPT's section of my-gpts.md. I can't convert it without its Instructions."
- If the source wrote no opening questions, any you write for the new skill end in "(inferred)", in SKILL.md and in the guide's setup.asks.
- If Knowledge files are named but not attached: "The GPT lists these Knowledge files: <names>. Can you attach them? If not, I'll convert without them and list what's lost."
- If the Description and Conversation starters give fewer than two phrases people would really say: "What do staff actually type when they use this GPT? Those become the trigger phrases." If none come, derive triggers from the instructions, mark each "(inferred)", and log "thin triggers" in Lost in translation.

If an answer never comes, proceed and record the gap in the ledger's "Lost in translation" table — except the Instructions: without them, stop.

**Steps:**
1. **Inventory.** List what you received and what's missing, in three lines.
2. **Check for client data.** If the instructions or Knowledge contain client names, IDs, SSNs, dates of birth, account numbers, or financials — real or sample — stop and say so. Don't copy them into the skill, even inside an example or a template; ask the admin to replace them with placeholders first.
3. **Place every line.** Walk the instructions top to bottom. Each line — and every clause in it — goes to exactly one place: a SKILL.md section, a reference file, or a ledger table. Nothing is dropped silently. Before writing the ledger, re-read the source against the finished SKILL.md once; anything shortened away goes back in or into Lost in translation.
4. **Write the SKILL.md.**
   - `name`: the GPT's name as a lowercase hyphenated slug, version numbers dropped ("Transcript to Action Plan & Client Email v 2.0" → `transcript-to-action-plan-client-email`).
   - `description`: what it does, then the trigger phrases, quoted from the GPT's Description and Conversation starters. No invented triggers.
   - Body, under these headings in this order: the purpose paragraph; **When to use it — and when not to** (only jobs the source says it doesn't do, or a mode it can't run because a file is missing — never narrow what the source says it does); **What to have ready**; **Opening questions**; **Workflow** (steps, with branch points named); **Output format** (the template, verbatim); **Guardrails** (each Confirmed row, and nothing else — if a step can't run because a file is missing, say so as a note in that Workflow step and log it in Lost in translation, not as a guardrail); **Needs** (web search, code interpreter, connectors, Actions — they may not exist on the new platform; list only what the source shows, and don't guess what a capability was used for).
   - Keep the GPT's own wording for rules. **Never paraphrase a list that has to match a system exactly** (CRM categories, form fields, legal text) — copy it. If a Knowledge file spells an item on that list differently, or names an item the list doesn't have, copy the instructions' version and log each mismatch in Lost in translation for the admin to check against the live system.
   - **Remove GPT-only workarounds** — text that exists only because of the 8,000-character limit or unreliable Knowledge loading ("read the attached file in full", "apply these even if the attachment did not load"). Log each in the ledger. When a rule was restated inline only for that reason, keep one copy.
5. **Knowledge files → `references/`.** Text files become `.md` with a first line saying which Knowledge file they came from. PDFs and spreadsheets stay as they are. In the body, say when to read each ("Read references/<file> when …"). If a Knowledge file is itself a skill, or repeats the instructions, don't copy it twice — note it in the ledger. Then compare every list item each Knowledge file names against the instructions' exact-match lists, character for character (capitals and punctuation count — "8(a)" is not "8(A)"). Log every difference in Lost in translation, even inside an example.
6. **Write the ledger** from references/ledger-template.md.
   - **Confirmed:** every never / don't / do not / no / only / always / do-not-guess in the source, quoted, with where it now lives. Search the source for each word; every hit is a row, including style rules ("no emojis") and scope rules ("include only when…"). Also every rule that fixes the output's shape (exact headings, their order, length, voice), even without one of those words.
   - **Suggested:** rules the GPT needed but never stated — handling client data pasted into the chat, no invented numbers, no legal or tax advice, anything its job obviously calls for. **Do not add them to the skill.**
   - **Removed as GPT-only workarounds**, **Lost in translation** (including anything the source points to only by name — "see the attached SKILL.md" or similar — for a Knowledge file that's missing or unavailable; quote the pointer), **Script candidates** (any calculation, ratio, or score the source names anywhere — workflow, menu option, or offer — even when no formula is given or you think another tool might do it; say so in "Why a script". "None" only if the source names no math or scoring at all).
7. **Write the guide spec** from references/guide-spec-template.json. `use.say` is only the triggers in the description. `never` has one line per Confirmed row, in the same order, and nothing else. `returns` is the real output shape. Every field, including plugin and version: if the source doesn't state it, leave it empty or end it in "(inferred)".
8. **Write the cold-test checklist** from references/checklist-template.md: one test per Confirmed guardrail, one per required input, one per branch, and G1–G8 with inputs written for this skill.

**Output.** Start with three lines: the skill name; counts (Confirmed N, Suggested N, Lost N, Script candidates N); the one thing the admin most needs to look at. Then the files. If you can create files, produce:

    <slug>/SKILL.md
    <slug>/references/…        ← the skill; this folder is what gets uploaded
    <slug>-ledger.md
    <slug>-guide.json
    <slug>-tests.md

Otherwise print each as a fenced block headed with its file name.

End with: "Next: answer yes or no on each Suggested guardrail. Then put the skill where you'll use it (on ChatGPT: a new Project, SKILL.md in the instructions, references/ uploaded) and run <slug>-tests.md there in a fresh chat. If advisors will stay on the Migrate button's plugin, run the same tests against that plugin instead."

**When the admin approves Suggested guardrails:** add each to the SKILL.md Guardrails section, move it to Confirmed in the ledger (source: "approved by admin <date>"), add it to the guide spec's `never`, and add its test to the checklist.

## Guardrails

- Never invents a trigger phrase. Derived triggers are marked "(inferred)".
- Never adds a guardrail or restriction anywhere in the skill without the admin's approval. Suggestions stay in the ledger.
- Never drops an instruction silently. Every source line lands in the skill, a reference file, or the ledger.
- Never paraphrases a list that has to match a system exactly.
- Never writes scripts. It flags script candidates.
- Never converts more than one GPT per chat, and never opens Knowledge files during triage.
- Never copies client data into a skill — real or sample, including examples inside a template.
- Never says the converted skill works. Testing is the admin's step, in a fresh chat.
- Merge and Retire are recommendations, never decisions.

## Needs

File upload (for GPT files, Knowledge files, and `my-gpts.md`). The Python tool, for Collect mode only; without it Collect prints the file instead. No web search, no connectors.
