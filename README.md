# SBDC AI Admin Kit

For the person who runs AI at an SBDC — the one who builds the tools, gets them in front of advisors, and answers for them when they break. Advisors never see this kit; they see the finished skills and a one-page guide for each.

> **Two caveats.** Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.

Custom GPTs are being retired (December 11, 2026 for Enterprise workspaces; Business workspaces are showing the same notice). Converting them is the easy part now. Knowing whether what came out still works is the part that needs a method, and that's what this kit is.

The same screen is on the site: https://bwfnx.github.io/sbdc-ai-admin-kit/

<!-- doors:start -->
## Which one is you?

- [I have the Migrate button](#door-1-you-have-the-button)
- [I have thirty GPTs to sort, or no button](#door-2-thirty-to-sort-or-no-button)

### Door 1: You have the button

1. **Press Migrate** on the GPTs people use; try a spare one first to see what comes out. One click each.
2. **Test each one cold** before advisors touch it: fresh chat, [TESTING.md](https://github.com/bwfnx/sbdc-ai-admin-kit/blob/main/TESTING.md), throw the ugly stuff at it. About ten minutes per GPT.
3. **Want a receipt** of which rules survived? Run the same GPT through [GPT to Skill](https://bwfnx.github.io/sbdc-ai-admin-kit/gpt-to-skill.html); its ledger is a receipt for the kit's own conversion and a checklist of the rules to test for in the button's plugin; the button doesn't give you one. About ten minutes per GPT, plus five to set up the first time.

This is what you get for each GPT. The full one is in the [worked example](https://github.com/bwfnx/sbdc-ai-admin-kit/blob/main/examples/transcript-to-action-plan/after/transcript-to-action-plan-client-email-ledger.md).

| # | Rule, quoted from the GPT | Where it lives now |
|---|---|---|
| C1 | "If the ID code is not present, use 'Client ID' — never guess one." | Guardrails; Workflow step 2; Output format |
| C2 | "match these Neoserra categories exactly, do not paraphrase" | Guardrails; Output format › Milestones list |
| S1 | Suggested: never paste a client's SSN, date of birth, or account numbers into the drafted email | Not in the skill until you say yes |
| Lost | "read the attached SKILL.md in full and follow it exactly" | Points at a Knowledge file that wasn't attached; attach it and re-run |

**You'll have:** the migrated plugins your advisors use, a pass/fail sheet per GPT, and, if you did step 3, a ledger per GPT.

Advisors stay on the button's plugin, and step 2 is the check on that one. The converted skill is your receipt and your test sheet: run its test list against the plugin.

### Door 2: Thirty to sort, or no button

1. **Put the skill where you work:** paste [skills/gpt-to-skill/SKILL.md](https://github.com/bwfnx/sbdc-ai-admin-kit/blob/main/skills/gpt-to-skill/SKILL.md) into a new ChatGPT Project's instructions and upload its `references` and `scripts` folders. About five minutes. Details on the [GPT to Skill](https://bwfnx.github.io/sbdc-ai-admin-kit/gpt-to-skill.html) page.
2. **Attach your GPT files** (Word is fine; one per GPT, named for the GPT), ten per message, and say *Triage my GPTs*; more than ten? say *more coming* on each batch and *that's all* on the last. The skill builds `my-gpts.md`, hands it back (keep it), then sorts it. No file comes back? It prints the combined file instead; save it as `my-gpts.md`.
3. **Read the table.** Skill and Plugin are keepers; Agent means it needs more than a skill, park it; Merge and Retire are your call. Have the button? Press it on the keepers and go to door 1, step 2. No button? Convert one per chat with the cards; each comes back with a receipt. Flags mark what to check, not what to drop: `no-refusals` means the GPT never says what it won't do.

**You'll have:** a 30-row table with a verdict per GPT, a card per keeper, and `my-gpts.md` to keep.

**The shelf:** [STANDARD.md](https://github.com/bwfnx/sbdc-ai-admin-kit/blob/main/STANDARD.md) (ten pass/fail lines; needs the skill's text in front of you) · [TESTING.md](https://github.com/bwfnx/sbdc-ai-admin-kit/blob/main/TESTING.md) · [the worked example](https://github.com/bwfnx/sbdc-ai-admin-kit/tree/main/examples/transcript-to-action-plan) (a real conversion, scored honestly: a narrow FAIL, and the list of what to check by hand) · [the guide generator](https://github.com/bwfnx/sbdc-ai-admin-kit/tree/main/generator) (optional) · Written for Maryland and points at Neoserra; check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported; fork it, change it, don't wait on me.
<!-- doors:end -->

Then give staff a one-page guide for each skill: what it does, what to have ready, what to say, what comes back, what it won't do. [generator/](generator/) builds pages like [these](https://bwfnx.github.io/sbdc-toolkit/) if you want it; a plain document works too.

[examples/transcript-to-action-plan](examples/transcript-to-action-plan/) shows why the check matters. We converted Maryland's meeting-notes GPT and compared the result with the original skill that GPT was built from. It scored a narrow FAIL, and results varied from run to run on the same input — the scorecard ends with the list of things to check by hand on every conversion, however it was converted.

## What's in it

| Piece | What it's for |
|---|---|
| [STANDARD.md](STANDARD.md) | What every skill needs before an advisor touches it. Joe Burnes's five-part Skill Standard, how we meet it, the two rules that keep staff guides honest, and a ten-line checklist. |
| [TESTING.md](TESTING.md) | How to find out whether a skill still works: run it cold and throw the ugly stuff at it. |
| [examples/](examples/) | A real conversion scored honestly against the skill it came from, a triage run, and the converter's own test results. |
| [generator/](generator/) | Optional. Turns a guide spec into a staff page. Edit `kit.json` for your center's name, links, and contact. |
| [skills/gpt-to-skill](skills/gpt-to-skill/SKILL.md) | Optional. For the receipt, for sorting thirty GPTs before you migrate any, or when you have no button: attach your GPT files, triage them all at once, then convert one per chat, with a guardrail ledger showing what was kept, dropped, or needs your approval. |

## Using the optional pieces

**gpt-to-skill.** Install, in ChatGPT on any plan: open `skills/gpt-to-skill/SKILL.md`, click Raw, copy everything, paste it into a new Project's instructions, then download the repo zip (green Code button, Download ZIP; the GitHub folder pages have no download), unzip it, and upload the files from `skills/gpt-to-skill/references` and `skills/gpt-to-skill/scripts` to the same Project (not a custom GPT: the file is bigger than the 8,000-character Instructions box). Other ways: in ChatGPT **Work mode** (Business and Enterprise) or Codex, say `install https://github.com/bwfnx/sbdc-ai-admin-kit`; a regular chat can't install from GitHub. Or download this repo as a zip and upload `skills/gpt-to-skill` at chatgpt.com/skills (untested here). Claude Code: `/plugin marketplace add bwfnx/sbdc-ai-admin-kit` then `/plugin install sbdc-ai-admin-kit@sbdc-ai-admin`.
- Export your GPTs into one `my-gpts.md`: for each, a `## GPT name` heading, then Description, Conversation starters, Knowledge file names, Capabilities, and the whole Instructions box. Markdown or plain text is best; Word works but adds nothing, and one file avoids upload limits. The Instructions box alone is enough for triage.
- **Already copied each GPT into its own Word file?** Attach them to the chat, ten per message, and say "Triage my GPTs" (more than ten? say "more coming" on each batch and "that's all" on the last). The skill builds `my-gpts.md` and hands it back, then sorts it. Attach all of them: triage can only spot duplicates it can see. No file comes back? It prints the combined file instead; save it, or paste your files into one Word document with a `## GPT name` line above each. On your own computer, `py tools/gpts-to-md.py "C:\Users\you\Desktop\My GPTs"` (or a list of files) does the same thing and uploads nothing.
- **Triage:** new chat, "Triage my GPTs," attach `my-gpts.md`. You get a verdict for each (Skill, Plugin, Agent, Merge, Retire) and a conversion card for each one worth converting.
- **Convert:** a new chat per card; paste the card and attach that GPT's Knowledge files. Answer yes or no on the suggested guardrails, then test with the checklist it hands back.

**The guide generator.** `py generator/build.py --kit generator/kit.json --src <folder of guide specs> --out <folder>`. Python 3, nothing to install. In `kit.json`, set `only_plugin` to `null` to render every guide spec you pass in, or to your plugin's name to render only that plugin's guides — the shipped `kit.json` uses `"sbdc-toolkit"` because it reproduces Maryland's live public pages. `netlify_allowlist` is Maryland-specific (it edits a `_redirects` file for a default-closed Netlify site) and should stay `false` unless you're running that same setup.

## License

MIT. Take it, re-skin it, swap in your own CRM language.
