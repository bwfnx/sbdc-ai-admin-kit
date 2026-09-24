# Cold-test checklist — <slug>

Run each test in a **fresh chat** with only this skill installed. Paste the input exactly; don't help it. Compare with "Pass looks like" and fill in the result. Method and reasons: references/testing.md.

| # | Test | Input | Pass looks like | Result (pass / fail — what happened) |
|---|---|---|---|---|

## Guardrail tests — one per confirmed guardrail (C1, C2, …)
| C1 | Try to break C1 | <a reasonable-sounding request that would break it> | <the refusal or behavior the rule requires> | |

## Missing-input tests — one per required input
| M1 | Leave out <input> | <a normal request without it> | <asks for it, or proceeds and marks the gap, per the skill> | |

## Branch tests — one per decision point in the workflow
| B1 | <branch> | <input that takes that branch> | <what that branch produces> | |

## Generic tests — G1–G8 from references/testing.md, with inputs written for this skill
| G1 | Vague opening | … | … | |
| G2 | Half answers | … | … | |
| G3 | Wrong file | … | … | |
| G4 | Misnamed file | … | … | |
| G5 | Client details where they don't belong | … | … | |
| G6 | Just outside scope | … | … | |
| G7 | Should refuse | covered by the C-tests above | — | |
| G8 | Format check | … | … | |
