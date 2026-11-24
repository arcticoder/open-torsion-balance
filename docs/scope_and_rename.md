# Scope change and repo rename (open, 2026-11-23)

The balance was designed to size spurious forces in small-thrust measurements. The repo is now to be a general torsion-balance instrument whose purpose is to improve itself: each campaign is chosen for what it teaches the instrument, and the results feed the next version
([campaign_loop.md](campaign_loop.md)). This matches how the sibling `lab` repo started (reusable instruments first). The spurious-force study stays as the first campaign, not the repo's identity.

## What changes in the repo's description (draft for the README, after the name is chosen)

- One-line: an open, low-cost torsion balance with a built-in loop from measurement to metrology improvement: noise budget, injected transfer coefficients, calibrated forces, provenance for every parameter.
- Campaigns are listed as studies (spurious forces; material and geometry studies; damper patterns), each with the parameters it can change.
- G1 (20 nN at 5 sigma) stays as the first acceptance claim; the plan gains a second claim: the budget's predicted noise matches the measured floor within a stated factor, after the T1 coefficients.

## Name candidates (criteria: short, a valid GitHub repo name, not tied to one effect, no clash with the `lab` repo)

| Candidate | For | Against |
|---|---|---|
| `open-torsion-balance` | plain, searchable, matches the README's opening words | says nothing about self-improvement |
| `forcebal` | already the name of the parameter set (`FORCEBAL`), short | cryptic to a stranger |
| `torsion-metrology-loop` | names the loop | long; "loop" is jargon |
| `microforce-bench` | scope-neutral, matches `lab` style | not specific to torsion |

Recommendation: `open-torsion-balance`, with the loop described in the README. (Decision: task 3 in [TODO-arcticoder.md](TODO-arcticoder.md).)

## Rename plan (executed after the decision; nothing is renamed yet)

1. GitHub: rename the repo (redirects remain for the old URL); update the local remote. 2. Rename the local directory and update `lab.code-workspace`. 3. Replace the old name in: `README.md`, `hardware/README.md`, `docs/**/*.md`, the `lab` repo's links (`docs/inventory.md`, `docs/orders.md`, `docs/kb/*`), `~/Code/sysadmin/wsl` notes that mention the repo, `docs/paper/main.tex`, and the user's memory notes.
4. Rewrite the README's opening and the plan's goal statement (new scope above); keep the history intact. 5. Run `tools/run_all_smoke_tests.py`. The user commits and force-pushes himself.
