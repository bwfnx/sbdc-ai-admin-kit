# SBDC AI Admin Kit

For the person who runs AI at an SBDC — the one who builds the tools, gets them in front of advisors, and answers for them when they break.

> **Two caveats.** Written for Maryland and points at Neoserra — check anything that touches your own CRM, programs, or reporting rules before you lean on it. MIT and unsupported — fork it, change it, don't wait on me.

Custom GPTs are being retired (December 11, 2026 for Enterprise workspaces; Business workspaces are showing the same notice). This kit is what Maryland uses to move tools to skills and keep them honest.

## What's in it

| Piece | What it's for |
|---|---|
| [STANDARD.md](STANDARD.md) | What every skill needs before an advisor touches it. Joe Burnes's five-part Skill Standard, how we meet it, the two rules that keep staff guides honest, and a ten-line checklist. |
| [skills/gpt-to-skill](skills/gpt-to-skill/SKILL.md) | Triage all your GPTs at once, then convert them one per chat. Each conversion hands back the skill, a guardrail ledger, a staff-guide spec, and a test checklist. |
| [TESTING.md](TESTING.md) | How to find out whether a skill still works: run it cold and throw the ugly stuff at it. |
| [generator/](generator/) | Turns a guide spec into a staff page like [these](https://bwfnx.github.io/sbdc-toolkit/). Edit `kit.json` for your center's name, links, and contact. |
| [examples/](examples/) | A real conversion, scored honestly against the skill it came from, plus a triage run and the converter's own test results. |

## Start here

1. **Export your GPTs into one Markdown file.** For each GPT, open Configure and paste into `my-gpts.md`: a `## GPT name` heading, then Description, Conversation starters, Knowledge file names, Capabilities, and the whole Instructions box. Markdown or plain text is best; Word works but adds nothing — one file avoids upload limits.
2. **Install the kit.** ChatGPT: say `install https://github.com/bwfnx/sbdc-ai-admin-kit`, or download this repo as a zip and upload `skills/gpt-to-skill` at chatgpt.com/skills. Claude Code: `/plugin marketplace add bwfnx/sbdc-ai-admin-kit` then `/plugin install sbdc-ai-admin-kit@sbdc-ai-admin`. Anywhere else: paste `skills/gpt-to-skill/SKILL.md` into a project's instructions.
3. **Triage.** New chat: "Triage my GPTs," attach `my-gpts.md`. You get a verdict for each (Skill, Plugin, Agent, Merge, Retire) and a conversion card for each one worth converting.
4. **Convert, one per chat.** New chat for each card: paste the card, attach that GPT's Knowledge files. Answer yes or no on the suggested guardrails.
5. **Test** each new skill in a fresh chat with its checklist. See [TESTING.md](TESTING.md).
6. **Publish a staff guide.** `py generator/build.py --kit generator/kit.json --src <folder of guide specs> --out <folder>`. Python 3, nothing to install. In `kit.json`, set `only_plugin` to `null` to render every guide spec you pass in, or to your plugin's name to render only that plugin's guides — the shipped `kit.json` uses `"sbdc-toolkit"` because it reproduces Maryland's live public pages. `netlify_allowlist` is Maryland-specific (it edits a `_redirects` file for a default-closed Netlify site) and should stay `false` unless you're running that same setup.

## See it work first

[examples/transcript-to-action-plan](examples/transcript-to-action-plan/) converts Maryland's meeting-notes GPT and compares the result with the original skill that GPT was built from — what it kept, what it lost, and whether it told you about the losses. It scored a narrow FAIL, and results vary from run to run — use the scorecard's hand-check list on every conversion.

## License

MIT. Take it, re-skin it, swap in your own CRM language.
