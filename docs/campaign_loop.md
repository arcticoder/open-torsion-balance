# The campaign feedback loop (design, 2026-11-23)

Status: DESIGN. Nothing here is implemented except the upgrade ranking (`hardware/balance/material_study.py --terms`) and the eddy-vane sketch (`hardware/balance/eddy_vane_sim.py`). The slow-demodulation script and the provenance table are specified in sections 4 and 5 and are
written once the gates in section 3 are approved (task 2 in [TODO-arcticoder.md](TODO-arcticoder.md)).

Today the plan has one feedback step: after A5 the measured numbers go into `hardware/balance/params.py` and `tools/force_noise_budget.py` is rerun ([procedures.md](procedures.md) A.7). This design turns that into a loop in which every campaign group measures the quantities that replace the
next group's assumptions, and each group's uncertainty budget uses the measured values of the groups before it.

## 1. What the loop replaces (assumption, the run that measures it, where it lands)

| params.py value now [assume] | Measured by (procedures.md) | Replaces | Budget term it moves |
|---|---|---|---|
| `AIR_SPEED_FLUCT` 1 mm/s, `AIR_AREA` | A.5 noise ASD, A.6 lid-lifted and fan runs | the air coefficient (nN/rtHz per lid state) | air currents, 4.8 nN/rtHz (98 % of the total) |
| `TEMP_NOISE` 1 mK/rtHz | TMP117 ASD during A.5 | the temperature density | frame path 0.63, arm 0.13 |
| `PLA_EXPANSION` x `FRAME_PATH`, `ARM_EXPANSION` | heater-step transfer run (section 2, T1): nN per K of frame heating | frame and arm coefficients (nN/K, now 315 and 63) | the two temperature terms |
| `TILT_NOISE_RAD`, `SEISMIC_ACC`, `COM_OFFSET` | LIS2DW12 ASD; tilt step with the levelling screws (known urad); shake step | tilt and acceleration coefficients (now 1.0 nN/urad, 103 nN per mm/s^2) | floor terms 0.21, 0.20 |
| `B_NOISE`, `STRAY_MOMENT` | MMC5983MA ASD; a known coil field (nN per uT, now 1) | magnetic coefficient | 0.02 |
| strip `kappa`, `STRIP_SHEAR_MODULUS` | B.1 inertia-pair period shift; A.4 resonance | kappa and I | every term through k_eff |
| `DAMPING_RATIO` 0.40 | A.4 decay with 1 and 2 pads | zeta | h(f), thermal term |
| `PLATE` constant c (7.1e-10 N/V^2) | B.2 plate fit against the weights | calibration | the claim conversion |
| `F_MOD` 0.05 / 0.025 Hz, `INTEGRATION_S` | baseline ASD (section 6) | the modulation frequency | lock-in resolution |

Predicted noise after the loop is each transfer coefficient times the environmental noise the board's own sensors measured, and is checked against the measured force ASD: agreement means the budget explains the floor; a gap names a term the budget lacks.

## 2. Order of the campaign (what it can improve first)

1. **T0, noise and drift (A.5).** Force ASD at rest, Allan deviation, drift per hour, with the TMP117, LIS2DW12 and MMC5983MA channels logged. Tells which term dominates before anything else is run.
2. **T1, injected transfer coefficients** (the lock-in method of the plan, a known input at 0.025 Hz, force read per unit input): a small heater resistor on the frame (nN per K), the levelling screws (nN per urad), a coil (nN per uT). Plus the lid-lifted air test (A.6). These measure what the noise cannot resolve below the air term.
3. **T2, calibration** (B): inertia-pair kappa, plate constant, lock-in scale. Needed before any force is quoted.
4. **T3, the claim runs** (C.3 lead-current, C.4 heating) last, so their uncertainty budgets use T0-T2 values. A claim run never feeds a parameter (section 3).
5. **Controls inside every group:** the baseline runs before and after a group give noise floor and drift against time; start- and end-of-day plate calibrations give the plate constant against temperature; the leads-unplugged runs give the systematic offset.

## 3. Guardrails (to approve; the numbers are proposals)

- **Calibration data and claim data never overlap.** Runs have a `purpose` field: `calibration` (T0-T2, may update params.py) or `claim` (T3, read-only against params.py). A run is never used for both. Claim uncertainties use the parameters as frozen at the start of the claim epoch.
- **Gates are fixed before the data arrive** and every run that passes feeds back, not only the favourable ones. Proposed gates, written into the run manifest as numbers: temperature drift under 0.05 K/h over the run (TMP117 slope), lid state as recorded, no LIS2DW12 sample above 20 mm/s^2 (door slam, footsteps), no field step over 1 uT (a moved magnet), the optical DC level inside 20-80 % of its range, the day's start calibration within 5 % of the previous day's. A failed gate rejects the run and is logged with its reason; rejected runs are listed in the table, not deleted.
- **Epochs.** An epoch is a stretch with one hardware state. Any change to trim, ballast, pad count, gasket, frame material, enclosure state (lid, vacuum), strip, or board starts a new epoch; parameters carry the epoch id; pooling across epochs is not allowed except for the T0 comparison that measures the change itself.
- **Provenance.** Every `params.py` value that came from a measurement records run id, epoch, date, value, uncertainty and the script version (section 5).

## 4. Slow-demodulation script (design): `hardware/instrument/host/slowdemod.py`

(The user's note named `host/analyze.py`; it is `hardware/instrument/host/analyze.py`. The new script sits beside it and reuses `asd` and `allan_deviation`.)

Input: a run directory `runNNN_label/` with the logger's CSV (the demodulated optical output, 20 samples/s or more) and a `manifest.json` (schema in section 5). Output: `runNNN_label/result.json` plus one text report.

Algorithm:
1. Convert the channel to force with the epoch's calibration (displacement scale V/mm from A.3, kappa, lever arm, plate constant); the conversion constants and their run ids are copied into the result.
2. Cut the record into whole modulation cycles (drop the partial cycle at each end, drop the first cycle for the thermal transient unless the run is a step run); reference is the DUT_EN square wave read back from the logger's own channel, not a nominal clock, so a dropped sample cannot rotate the phase.
3. Regress, in one least-squares fit over the kept samples, the force on: in-phase and quadrature reference at f_mod and its odd harmonics up to 5 (a square wave carries them), a constant, a linear drift and a quadratic drift, and the witness channels (frame temperature, tilt, field components), each high-passed at 3 x the lowest modulation frequency so they cannot absorb the signal. Report the signal amplitude and phase before and after the witness regression (the noise reduction is itself a result).
4. Uncertainty: the fit's covariance scaled by the residual's own spectrum near f_mod (red noise makes the white-noise formula too small), cross-checked by a block bootstrap over the cycles and by the split-half scatter. The reported number is the larger. A run whose three estimates disagree by over a factor 1.5 is flagged.
5. Express the coupling per ampere (I from the logger), per watt, or per kelvin; apply the Lorentz second check (section 6) when the run is a lead-current run.
6. Tests (`hardware/instrument/host/test_host.py` pattern): synthetic runs with known amplitude, injected 1/f drift and known witness leakage; the recovered amplitude within its stated uncertainty in over 90 % of 200 realizations; a run with a leaked witness shows the regression removing it; a polarity swap flips the sign.

## 5. Provenance table (design): `hardware/balance/provenance.csv` and the run manifest

`runs.csv` (one row per run, written by the script from the manifest): `run_id, date, epoch, purpose, label, condition, T_mean_C, T_slope_K_per_h, tilt_urad, B_uT, lid, gates_passed, reject_reason, calib_id, script_version, result_path`.

`provenance.csv` (one row per measured parameter value): `param, value, unit, sigma, epoch, run_ids, date, method, supersedes`. `params.py` keeps its `[assume]` tags until a row exists; then the tag becomes `[meas: epoch E, runs a-b]` and the number in the file equals the row.
The smoke test gains two checks when the files exist: every `[meas]` tag in params.py has a provenance row with the same value, and no `claim` run id appears in a provenance row.
`epochs.csv`: `epoch, start, hardware_change, trim_state, pads, frame_material, enclosure, strip_id`, appended by hand at each change (an agent task: asked of the user when a change is reported).

## 6. Second scale check, witness regression, modulation frequency

- **Lorentz scale check.** For a lead-current run, the predicted force is B I L with B from the MMC5983MA at the leads, I from the logger and L from the lead geometry; compare it with the force read through the plate calibration. They agree within the combined uncertainty or one of the two has an error. The field and its gradient at the leads dominate the prediction's error (the magnetometer sits on the board, not at the leads): the check is a consistency test, not a calibration, until the field is mapped along the leads.
- **Witness channels.** The regression in 4.3 is the noise-reducing step; its gain is the ratio of residual ASD to raw ASD at f_mod, reported per run. Done in analysis only: no hardware change.
- **Modulation frequency and integration time.** After T0, pick f_mod and the on/off cycle count where the measured force ASD (witness-regressed) is lowest, subject to f_mod below the resonance 0.215 Hz and at least 10 cycles per run. The 0.025/0.05 Hz values stay until a measured ASD says otherwise; a change opens a new epoch for the claim runs only.

## 7. How the upgrade studies connect

`material_study.py --terms` ranks which term limits at each stage (air, then vacuum) with the model's current assumptions. Its output is a prediction to be replaced by the transfer coefficients of T1; the first heater-step result (nN per K) replaces the handbook CTE x path and re-ranks.
The ranking and the vane sketch are summarised in [kb/balance_design_notes.md](kb/balance_design_notes.md) (section "2026-11-23 upgrade study"). The repo scope and rename discussion is in [scope_and_rename.md](scope_and_rename.md).
