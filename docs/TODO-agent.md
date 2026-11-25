# TODO-agent

Repository audit, 2026-11-24, commits `c201d3e..847c970` (everything since the last audit's fixes). Verified: read every changed `.py` and `.md` file in that range; ran
`hardware/balance/smoke_test.py` (system Python plus numpy/scipy/magpylib: all non-CAD checks pass, the eddy-vane and J2 checks included), `hardware/instrument/smoke_test.py`
(passes, with skidl/kiutils/ngspice/jlcparts checks skipped) and `material_study.py --terms`; checked that the committed `fab/bom.csv` and `fab/cpl.csv` contain no U7.
Not verified: the CadQuery checks (cadquery is not installed here, so the new hacksaw-handle pin holes and the outside-flush wall plates were not rebuilt or checked
against the committed STLs), the KiCad layout tests, and the physics of `eddy_vane_sim.py` beyond the smoke checks' sanity properties.

- [ ] **README.md:23 and docs/plan.md:4 — stale main-board order status.** Both still say the main-board order is in the JLC cart and held for the Black Friday sale,
  but `docs/fabrication.md:105` records it as placed 2026-11-18 and in production since 2026-11-20.
  Steps: change the README status cell to "placed 2026-11-18, in production at JLC (Economic PCBA, 2 assembled, LIS2DW12 not placed)" and the plan.md sentence to
  match; grep the user-facing docs for "held for the Black Friday" and "in the JLC cart" and update any other live (non-history) mention.

- [ ] **hardware/instrument/fab/ORDER.md:14 — last sentence contradicts the new DNP handling.** It still says to re-upload `bom.csv` and `cpl.csv` "then answer the two
  'Do not place' dialogs", but the same paragraph now says U7 is left out of both files so the dialogs no longer appear, and switching to the Standard route needs a code change.
  Steps: replace the sentence with: "To change the route (Standard PCBA with U7), remove `U7` from `DNP_FIRST_ARTICLES` in `layout/mainboard.py`, rerun its `fab()`
  step to regenerate `bom.csv` and `cpl.csv`, and re-upload both."

- [ ] **docs/campaign_loop.md:27 (and :16), docs/procedures.md:51 — the LIS2DW12 is listed as a logged channel, but it is not fitted.** T0 says the TMP117, LIS2DW12
  and MMC5983MA channels are logged, and procedures C.1 lists "floor acceleration (LIS2DW12)" for every run, while U7 is not placed on the first articles
  (`ORDER.md:14`, `mainboard.py:649`; `campaign_loop.md:50` itself says so).
  Steps: in campaign_loop.md T0 and the row at line 16, mark the LIS2DW12 channel "(when fitted; a breakout until then)"; in procedures.md:51 add "(if fitted;
  not on the first articles)" after "floor acceleration (LIS2DW12)". Note that the tilt/acceleration transfer coefficients in T1 then need another tilt sensor or the breakout.

- [ ] **hardware/balance/smoke_test.py:267 — unguarded `import jlc_parcel_mass` crashes the whole test without numpy.** `tools/jlc_parcel_mass.py:15` imports numpy at
  module level, so with a Python lacking numpy the test dies with a traceback and `tools/run_all_smoke_tests.py` reports it failed. This contradicts
  `hardware/README.md:27-28` ("with the system Python the CAD checks are skipped, not failed"); reproduced in this audit before numpy was installed.
  Steps: either wrap the parcel-mass block in `try: ... except ImportError as _e: print(f"[SKIP] parcel-mass checks need numpy: {_e}")` like the arm-DXF block above it,
  or replace the numpy use in `jlc_parcel_mass.py` with `struct`/plain Python (it only parses STL volumes); then rerun `tools/run_all_smoke_tests.py` with a bare Python.

- [ ] **hardware/balance/smoke_test.py:245 — the "study restores params.py" check hardcodes the parameter values.** It compares `P.PLA_EXPANSION`, `P.AIR_AREA` and
  `P.FRAME_PATH` against literals 70e-6, 2e-3 and 0.10, so a legitimate edit of `params.py` fails the check, and it does not cover `ARM_EXPANSION` or `AIR_SPEED_FLUCT`
  (which `material_study.main_terms` also swaps).
  Steps: snapshot `(P.PLA_EXPANSION, P.ARM_EXPANSION, P.AIR_AREA, P.FRAME_PATH, P.AIR_SPEED_FLUCT)` before the J2 block, run `MS.upgrade_stages()` and a few `terms_for(...)`
  what-ifs, then check the tuple is unchanged.

- [ ] **hardware/balance/material_study.py:154 — leftover unused variable.** `main_terms()` starts with `k = None`, which is never read.
  Steps: delete the line and rerun `python3 hardware/balance/material_study.py --terms` to confirm the output is unchanged.

- [ ] **hardware/instrument/layout/mainboard.py:649 — `DNP_FIRST_ARTICLES` has no test.** The committed `fab/bom.csv` and `fab/cpl.csv` currently omit U7 (checked), but
  nothing fails if a regeneration or a hand edit puts it back, which would bring back the Standard-only "unselected parts" prompt on an Economic order.
  Steps: add a check to `hardware/instrument/smoke_test.py` that reads both CSVs and asserts no designator in `mainboard.DNP_FIRST_ARTICLES` (if importing
  `mainboard` needs kiutils, move the set to a small module both files import) appears
  in the BOM's Designator lists or the CPL's Designator column, and that every other BOM designator has a CPL row.
