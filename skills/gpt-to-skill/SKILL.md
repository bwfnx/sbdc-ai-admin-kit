---
name: gpt-to-skill
description: Turn custom GPTs into skills. TRIAGE mode takes every GPT's instructions at once (one my-gpts.md file, a "## GPT Name" heading over each) and sorts each into Skill, Plugin, Agent, Merge, or Retire, flags the risky ones, and writes a conversion card for each. CONVERT mode takes one GPT per chat (its Instructions, Description, Conversation starters, and Knowledge files) and returns a SKILL.md, a guardrail ledger, a staff-guide spec, and a cold-test checklist. Use when someone says "triage my GPTs", "convert this GPT to a skill", "migrate my GPTs", "turn these GPT instructions into a SKILL.md", or pastes a conversion card.
---

# GPT to Skill

Custom GPTs are being retired (OpenAI's date for Enterprise workspaces is December 11, 2026; Business workspaces show the same notice). This skill moves them to skills without losing what made them work: the questions they ask, the things they refuse, and the format they hand back. It is for the person running AI at an SBDC, not for advisors.

It has two modes. **Triage** looks at all your GPTs at once and decides what each should become. **Convert** turns one GPT into a skill, in its own chat.

> Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.

## When to use it — and when not to

Use it to migrate a custom GPT, or any long system prompt, into a skill.

Don't use it to:
- write a brand-new skill from scratch — write against references/standard.md instead;
- convert more than one GPT in one chat;
- write scripts (it flags where one belongs);
- test a skill — that's references/testing.md, in a fresh chat.

## What to have ready

**For triage:** one file, `my-gpts.md`, with every GPT in it like this:

    ## <GPT name>
    Description: <from the Configure page>
    Conversation starters: <each one>
    Knowledge files: <file names only>
    Capabilities: <web search, code interpreter, image generation, canvas, apps like Gmail or Drive, any Actions>

    <the full Instructions box, pasted as-is>

Markdown or plain text is best. Word files work but add nothing. One file avoids per-message upload limits, and GPT instructions are capped at 8,000 characters each, so even thirty GPTs fit.

**For convert:** the same block for one GPT (or its conversion card), plus the actual Knowledge files.

## Which mode

- More than one GPT in the input → **Triage**.
- One GPT, or a conversion card → **Convert**.
- Can't tell → ask: "Do you want me to triage several GPTs, or convert one?"

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

   **Flags** — any that apply: `knowledge` (depends on Knowledge files), `client-data` (handles client names, IDs, or financials), `web/apps` (uses web search, app connectors, or Actions), `no-refusals` (states nothing it won't do), `math` (calculates or scores).

   **Order** — simplest first: Skills with the fewest flags, then Plugins. Agents last.
3. After the table, ask once: "Which of these do people use every day?" Move those to the top of the order.
4. Write a **conversion card** for every Skill or Plugin row:

       Convert this GPT to a skill: <GPT name>
       Triage verdict: <Skill | Plugin> — <one-line reason>
       Flags: <flags>
       Attach: the "<GPT name>" section of my-gpts.md, and Knowledge files: <names, or "none">

5. End with: "Open a **new chat** for each card. Converting here would crowd this chat and the quality drops. If your platform has subagents, hand each card to one instead."

**Triage never converts.** If asked to convert in the triage chat, give that GPT's card and say why a fresh chat is better.

## Convert

**Opening questions** (ask only what's missing, all at once):
- If Knowledge files are named but not attached: "The GPT lists these Knowledge files: <names>. Can you attach them? If not, I'll convert without them and list what's lost."
- If there's no Description and no Conversation starters: "Is there a description or any conversation starters? They become the trigger phrases." If none come, derive triggers from the instructions and mark each "(inferred)".

If an answer never comes, proceed and record the gap in the ledger's "Lost in translation" table.

**Steps:**
1. **Inventory.** List what you received and what's missing, in three lines.
2. **Check for client data.** If the instructions or Knowledge contain real client names, IDs, or financials, stop and say so. Don't copy them into the skill; ask the admin to replace them with placeholders first.
3. **Place every line.** Walk the instructions top to bottom. Each line goes to exactly one place: a SKILL.md section, a reference file, or a ledger table. Nothing is dropped silently.
4. **Write the SKILL.md.**
   - `name`: the GPT's name as a lowercase hyphenated slug, version numbers dropped ("Transcript to Action Plan & Client Email v 2.0" → `transcript-to-action-plan-client-email`).
   - `description`: what it does, then the trigger phrases, quoted from the GPT's Description and Conversation starters. No invented triggers.
   - Body, under these headings in this order: the purpose paragraph; **When to use it — and when not to**; **What to have ready**; **Opening questions**; **Workflow** (steps, with branch points named); **Output format** (the template, verbatim); **Guardrails** (each confirmed rule); **Needs** (web search, code interpreter, connectors, Actions — they may not exist on the new platform).
   - Keep the GPT's own wording for rules. **Never paraphrase a list that has to match a system exactly** (CRM categories, form fields, legal text) — copy it.
   - **Remove GPT-only workarounds** — text that exists only because of the 8,000-character limit or unreliable Knowledge loading ("read the attached file in full", "apply these even if the attachment did not load"). Log each in the ledger. When a rule was restated inline only for that reason, keep one copy.
5. **Knowledge files → `references/`.** Text files become `.md` with a first line saying which Knowledge file they came from. PDFs and spreadsheets stay as they are. In the body, say when to read each ("Read references/<file> when …"). If a Knowledge file is itself a skill, or repeats the instructions, don't copy it twice — note it in the ledger.
6. **Write the ledger** from references/ledger-template.md.
   - **Confirmed:** every never / don't / only / do-not-guess in the source, quoted, with where it now lives.
   - **Suggested:** rules the GPT needed but never stated — handling client data pasted into the chat, no invented numbers, no legal or tax advice, anything its job obviously calls for. **Do not add them to the skill.**
   - **Removed as GPT-only workarounds**, **Lost in translation**, **Script candidates** (any calculation or scoring).
7. **Write the guide spec** from references/guide-spec-template.json. `use.say` is only the triggers in the description. `never` is only the Confirmed table. `returns` is the real output shape. Anything inferred ends in "(inferred)".
8. **Write the cold-test checklist** from references/checklist-template.md: one test per Confirmed guardrail, one per required input, one per branch, and G1–G8 with inputs written for this skill.

**Output.** Start with three lines: the skill name; counts (Confirmed N, Suggested N, Lost N, Script candidates N); the one thing the admin most needs to look at. Then the files. If you can create files, produce:

    <slug>/SKILL.md
    <slug>/references/…        ← the skill; this folder is what gets uploaded
    <slug>-ledger.md
    <slug>-guide.json
    <slug>-tests.md

Otherwise print each as a fenced block headed with its file name.

End with: "Next: answer yes or no on each Suggested guardrail. Then install the skill and run <slug>-tests.md in a fresh chat."

**When the admin approves Suggested guardrails:** add each to the SKILL.md Guardrails section, move it to Confirmed in the ledger (source: "approved by admin <date>"), add it to the guide spec's `never`, and add its test to the checklist.

## Guardrails

- Never invents a trigger phrase. Derived triggers are marked "(inferred)".
- Never adds a guardrail to the skill without the admin's approval. Suggestions stay in the ledger.
- Never drops an instruction silently. Every source line lands in the skill, a reference file, or the ledger.
- Never paraphrases a list that has to match a system exactly.
- Never writes scripts. It flags script candidates.
- Never converts more than one GPT per chat, and never opens Knowledge files during triage.
- Never copies real client data into a skill.
- Never says the converted skill works. Testing is the admin's step, in a fresh chat.
- Merge and Retire are recommendations, never decisions.

## Needs

File upload (for Knowledge files and `my-gpts.md`). Nothing else: no web search, no connectors, no code.
