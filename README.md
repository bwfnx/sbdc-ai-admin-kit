# SBDC AI Admin Kit

For the person who runs AI at an SBDC — the one who builds the tools, gets them in front of advisors, and answers for them when they break. Advisors never see this kit; they see the finished skills and a one-page guide for each.

> **Two caveats.** Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.

Custom GPTs are being retired (December 11, 2026 for Enterprise workspaces; Business workspaces are showing the same notice). Converting them is the easy part now. Knowing whether what came out still works is the part that needs a method, and that's what this kit is.

**New here? Open the guide site first: https://bwfnx.github.io/sbdc-ai-admin-kit/** — it says what to do, in order.

## Start here

1. **Convert.** If your ChatGPT workspace has the one-click migration, use it. Migrating everything and keeping what people actually use is a perfectly good plan.
2. **Check each result before advisors touch it.** Run it cold in a fresh chat with [TESTING.md](TESTING.md); that works on anything you can chat with, including what the Migrate button made. [STANDARD.md](STANDARD.md) (ten pass/fail lines) needs the skill's text in front of you. Want a receipt of which rules survived? Run the same GPT through [skills/gpt-to-skill](skills/gpt-to-skill/SKILL.md) too; its ledger is that receipt, and the button doesn't give you one. A migration always produces *something*; the question is whether it still asks the right questions, refuses what it should, and gives you your format.
3. **Give staff a one-page guide** for each skill: what it does, what to have ready, what to say, what comes back, what it won't do. [generator/](generator/) builds pages like [these](https://bwfnx.github.io/sbdc-toolkit/) if you want it; a plain document works too.

[examples/transcript-to-action-plan](examples/transcript-to-action-plan/) shows why step 2 matters. We converted Maryland's meeting-notes GPT and compared the result with the original skill that GPT was built from. It scored a narrow FAIL, and results varied from run to run on the same input — the scorecard ends with the list of things to check by hand on every conversion, however it was converted.

## What's in it

| Piece | What it's for |
|---|---|
| [STANDARD.md](STANDARD.md) | What every skill needs before an advisor touches it. Joe Burnes's five-part Skill Standard, how we meet it, the two rules that keep staff guides honest, and a ten-line checklist. |
| [TESTING.md](TESTING.md) | How to find out whether a skill still works: run it cold and throw the ugly stuff at it. |
| [examples/](examples/) | A real conversion scored honestly against the skill it came from, a triage run, and the converter's own test results. |
| [generator/](generator/) | Optional. Turns a guide spec into a staff page. Edit `kit.json` for your center's name, links, and contact. |
| [skills/gpt-to-skill](skills/gpt-to-skill/SKILL.md) | Optional. For when you have no migration button (Claude, older workspaces), or want a second opinion: triage all your GPTs at once, then convert one per chat, with a guardrail ledger showing what was kept, dropped, or needs your approval. |

## Using the optional pieces

**gpt-to-skill.** Install, in ChatGPT on any plan: open `skills/gpt-to-skill/SKILL.md`, click Raw, copy everything, paste it into a new Project's instructions, and upload the five files in `skills/gpt-to-skill/references` to the same Project (not a custom GPT: the file is bigger than the 8,000-character Instructions box). Other ways: in ChatGPT **Work mode** (Business and Enterprise) or Codex, say `install https://github.com/bwfnx/sbdc-ai-admin-kit`; a regular chat can't install from GitHub. Or download this repo as a zip and upload `skills/gpt-to-skill` at chatgpt.com/skills (untested here). Claude Code: `/plugin marketplace add bwfnx/sbdc-ai-admin-kit` then `/plugin install sbdc-ai-admin-kit@sbdc-ai-admin`.
- Export your GPTs into one `my-gpts.md`: for each, a `## GPT name` heading, then Description, Conversation starters, Knowledge file names, Capabilities, and the whole Instructions box. Markdown or plain text is best; Word works but adds nothing, and one file avoids upload limits. The Instructions box alone is enough for triage.
- **Already copied each GPT into its own Word file?** Paste them into one Word document with a `## GPT name` line above each and save it; Word is fine, and put all of them in. Have Python? `py tools/gpts-to-md.py "C:\Users\you\Desktop\My GPTs"` does the pasting for you: it writes `my-gpts.md` next to the folder, one section per file, lists anything it couldn't read, and runs on your computer with nothing uploaded. In ChatGPT Work mode, Codex, or Claude you can also say: "run tools/gpts-to-md.py from the sbdc-ai-admin-kit repo on my GPTs folder."
- **Triage:** new chat, "Triage my GPTs," attach `my-gpts.md`. You get a verdict for each (Skill, Plugin, Agent, Merge, Retire) and a conversion card for each one worth converting.
- **Convert:** a new chat per card; paste the card and attach that GPT's Knowledge files. Answer yes or no on the suggested guardrails, then test with the checklist it hands back.

**The guide generator.** `py generator/build.py --kit generator/kit.json --src <folder of guide specs> --out <folder>`. Python 3, nothing to install. In `kit.json`, set `only_plugin` to `null` to render every guide spec you pass in, or to your plugin's name to render only that plugin's guides — the shipped `kit.json` uses `"sbdc-toolkit"` because it reproduces Maryland's live public pages. `netlify_allowlist` is Maryland-specific (it edits a `_redirects` file for a default-closed Netlify site) and should stay `false` unless you're running that same setup.

## License

MIT. Take it, re-skin it, swap in your own CRM language.
