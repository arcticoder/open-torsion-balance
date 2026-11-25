# Scope change and repo rename (2026-11-23)

Name chosen: `open-torsion-balance` (renamed on GitHub 2026-11-23; the old URL redirects). Status of the rename plan is at the end; the README rewrite waits on the scope text below being approved.

The balance was designed to size spurious forces in small-thrust measurements. The repo is now to be a general torsion balance for small forces in air. Its output is calibrated small forces at a stated resolution and cost; the improvement loop ([campaign_loop.md](campaign_loop.md)) is how it gets better at producing them. This matches how the sibling `lab` repo started (reusable instruments first). The spurious-force study stays as the first campaign, not the repo's identity.

## Scope statement

An open, low-cost torsion balance for measuring small forces in air, with a documented loop that feeds each campaign's calibration data back into the instrument's metrology.
- Calibration and characterization campaigns are chosen for what they teach the instrument (they may set parameters). Claim campaigns are chosen for the question they answer and only use the instrument's parameters; claim and control runs never set a parameter.
- G1 (20 nN at 5 sigma in 1000 s) stays as the first acceptance claim, answered by the spurious-force campaign.
- Second acceptance claim, fixed now: after the T1 transfer coefficients are measured, the budget's predicted force-noise density at f_mod (coefficients x the board's own environmental readings) matches the measured, witness-regressed force ASD within a factor of 3. Outside it, the design goes back to G2/G3 (the repo's existing line for a disagreement of a factor of a few). The factor is frozen with the gates (`campaign_loop.md` rule F): it is not revised after the T0 record is seen.

## Draft README opening (not yet applied)

> # open-torsion-balance
>
> An open, low-cost torsion balance for measuring small forces in air, with printable mechanics, a validated force-noise model, fab-assembled electronics and a documented loop that feeds each campaign's calibration data back into the instrument's metrology.
>
> **The instrument.** A horizontal arm on a taut stainless strip, read optically and calibrated electrostatically and by added inertia, with a resolution target of 0.4 nN (5 sigma on a 20 nN term) in a 1000 s measurement. Every noise term is predicted from a parameter file, and every parameter that a measurement replaces is recorded with the run that set it.
>
> **The first campaign.** The spurious forces that dominate small-thrust measurements: the Lorentz force of supply-lead currents in the ambient field, and the thermal and convective forces of a dissipating device, as functions of current, lead geometry and power.
>
> **Next campaigns.** Materials and geometry for the frame and damper, chosen by simulation and checked by injected-signal transfer coefficients, so improvements are measured in air before any vacuum work.

(The existing README text on the question, the claim and the parts cost moves under "The first campaign" unchanged.)

## Rename plan

Done 2026-11-23: GitHub rename (`gh repo rename`); the original working directory's remote changed to the new URL; a fresh clone at `~/Code/python/open-torsion-balance` (Git LFS filled); the clone added to `lab/lab.code-workspace` (the old folder entry is still there, a duplicate of the same repo); the old name replaced in the live text of this repo, `lab`, `~/Code/sysadmin/wsl` and the agent's notes (`docs/history.md` files left as written).
Open: 1. README rewrite from the draft above, after the scope text is approved. 2. `docs/plan.md` goal statement and `hardware/README.md`/`docs/paper/main.tex` titles. 3. Remove the old directory `~/Code/python/spurious-force-balance` and its workspace entry once its work is confirmed pushed (a normal commit and push: the rename needs no force-push and the history stays). 4. Run `tools/run_all_smoke_tests.py` from the new clone.
