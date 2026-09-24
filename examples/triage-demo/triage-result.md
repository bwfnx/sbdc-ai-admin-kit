# GPT Triage — my-gpts.md (5 GPTs)

| # | GPT | Purpose (one line) | Verdict | Flags | Order |
|---|---|---|---|---|---|
| 1 | Client Notes Formatter | Formats advisor session notes into a fixed CRM-ready structure | Skill | `knowledge`, `client-data`, `no-refusals` | 1 |
| 2 | Marketing Helper | Writes 5 social posts for a small business from name/audience/tone | Skill | none | 2 |
| 3 | Marketing Helper 2 | Writes 5 Facebook/Instagram posts for a small business | Merge — keep **Marketing Helper**, retire this one | `no-refusals` | 3 |
| 4 | Loan Ready Check | Calculates DSCR from client financials and calls it against an SBA SOP | Plugin | `knowledge`, `client-data`, `math`, `no-refusals` | 4 |
| 5 | Market Research Agent | Multi-step web/census research that builds a spreadsheet and a 5-page report | Agent | `web/apps`, `no-refusals` | 5 |

Notes on the calls:
- **Marketing Helper vs. Marketing Helper 2** — same job, minor variation. Marketing Helper is the one to keep: it asks for business name, audience, and tone (Marketing Helper 2 only asks what the business does and who the customers are), and it's the only one of the pair with a stated limit ("Do not make claims about results the business can't prove"). Marketing Helper 2 has none. Recommendation only — the admin decides.
- **Client Notes Formatter** carries a worked example inside its own instructions that includes an SSN and a specific revenue figure attached to a named client. Even flagged as synthetic in this demo file, that's exactly the pattern Convert mode stops on ("Check for client data") — before this one is converted, replace the example with placeholder data.
- **Loan Ready Check** does a real calculation (DSCR = income ÷ debt payments) and then makes an eligibility call from it — that's why it's a Plugin, not a Skill: the math belongs in a script, not in prose the model re-derives each time.
- **Market Research Agent** chains web search, code interpreter, and multiple sequential outputs (spreadsheet, charts, 5-page report) unattended — Agent territory, not a single-shot skill.
- `no-refusals` is flagged wherever the instructions contain no "don't," "never," or "only" limit — that includes Loan Ready Check, Marketing Helper 2, Client Notes Formatter, and Market Research Agent. Only Marketing Helper has a stated limit.

Which of these do people use every day? **Client Notes Formatter** — moved to the top of the order above.

## Conversion cards

Convert this GPT to a skill: Client Notes Formatter
Triage verdict: Skill — one focused, repeatable formatting job the instructions carry on their own
Flags: knowledge, client-data, no-refusals
Attach: the "Client Notes Formatter" section of my-gpts.md, and Knowledge files: note-format.docx

Convert this GPT to a skill: Marketing Helper
Triage verdict: Skill — one focused, repeatable job the instructions carry on their own
Flags: none
Attach: the "Marketing Helper" section of my-gpts.md, and Knowledge files: none

Convert this GPT to a skill: Loan Ready Check
Triage verdict: Plugin — needs a script for the DSCR math and ships with knowledge files (SOP + lender matrix)
Flags: knowledge, client-data, math, no-refusals
Attach: the "Loan Ready Check" section of my-gpts.md, and Knowledge files: SBA-SOP-50-10-8.pdf, lender-matrix.xlsx

Open a **new chat** for each card. Converting here would crowd this chat and the quality drops. If your platform has subagents, hand each card to one instead.

## Converter fixes from this test

Run 1 missed the `no-refusals` flag on Loan Ready Check, whose only guidance is "Be encouraging." The flag's definition in gpt-to-skill/SKILL.md was tightened from "states nothing it won't do" to: its instructions contain no "don't", "never", or "only" limit on what it will do, checked on every GPT including ones that sound harmless. This file is run 2, after that fix, and it meets every check.
