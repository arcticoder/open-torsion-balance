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

**Run purposes (three).** `calibration` (T0-T2: may set parameters), `control` (baselines, leads-unplugged runs, plate checks and no-current hours during claim days: the claim analysis uses them for offset subtraction, they never set parameters), `claim` (T3: read-only against the parameters). A run has exactly one purpose and is never reused under another.

**Rule D (drive-correlated witnesses).** A witness channel that the run drives, or that responds to the drive, is excluded from that run's gates AND from that run's witness regression. "Responds to the drive" is tested, not assumed: the script correlates each witness with the run's reference (the DUT_EN or heater square wave) at f_mod and its odd harmonics up to 5, in the same high-passed form as the regression; a witness whose in-phase or quadrature amplitude exceeds 3 times its own noise there is flagged drive-correlated and dropped, and the amplitude is reported (it is a result: the board's field reading of 300 mA at about 1 cm is about 6 uT). The manifest also lists the channels the run is designed to drive (`driven`), which are excluded without the test. A high-pass does not replace this rule, because the 3rd and 5th harmonics of a square wave pass it.

**Gates are per run type.** Proposed values (revisable once, rule F):

| Run type | Drives (`driven`) | Gates that apply (all others excluded) |
|---|---|---|
| T0 noise baseline, control baseline, leads-unplugged control | none | all gates below |
| T1 heater step; C.4 heating | frame or device temperature | no temperature-slope gate; tilt, field, optical DC, accelerometer (if fitted) apply |
| T1 tilt step | tilt | no tilt gate; temperature, field, optical DC, accelerometer apply |
| T1 coil run; C.3 lead-current | field (C.3 also device temperature if the card heats) | no field gate (no temperature gate if the card heats); the others apply |
| B calibration, plate steps | plate voltage only | all gates below |

The gates: temperature slope under 0.05 K/h over the run (TMP117, where not driven); field step under 1 uT between 60 s blocks (where not driven); the optical DC level inside 20-80 % of its range; no more than N excursions above a band-limited rms threshold of the accelerometer (a block rms in 0.01-1 Hz, over 60 s blocks); for calibration runs, the B.2 fit's residuals under 2 %.
- **The accelerometer gate is optional** until the LIS2DW12 is fitted (it is not placed on the first articles). Its threshold is derived from the first T0 record (proposal: 5 times the median block rms) and frozen with the gates; a fixed 20 mm/s^2 per sample is not used, because the sensor's own noise over 1000 s at a high sample rate can exceed it.
- **No agreement gate on the calibration.** The day's calibration is gated on its own quality (residuals under 2 %). Day-to-day change in the plate constant and kappa is logged as a trend; a jump triggers investigation or a new epoch, never a silent rejection of that day's claim runs.
- A failed gate rejects the run, with the gate name and value in `runs.csv`; rejected runs are kept in the table.

**Rule F (freeze).** The gates may be revised once, after the T0 record shows the real noise, and are then frozen with a `gates_version` before the first claim run. `script_version` is frozen the same way. If claim data are reanalysed with a later version, both results are reported.

**Rule P (parameters and the force scale).** Two rules: (1) model parameters (transfer coefficients, zeta, the form of kappa) are frozen for the epoch; (2) the force scale of a claim run comes from that day's bracketing `calibration` runs (B.3: start and end of day, and after a 2 C change). A claim run's own data never enter either.

**Epochs are hardware states, not conditions.** A new epoch starts at: a change to ballast or pad count (moves I and the centre of mass; "trim" means only these); the dummy mass swapped for the device card; a change of Rf or LED current (A.2 allows both); a change to the firmware's acquisition or lock-in code; the strip re-clamped or replaced; the gasket, enclosure or frame material changed; the board replaced; the apparatus moved. Not epochs: the lid state for A.6, the choice of f_mod, a torsion-head re-zero (a setpoint), the day, the lead geometry. These are conditions in `runs.csv`.

**Pooling.** Raw signals and parameter fits are never pooled across epochs. Calibrated forces (newtons, each from its own epoch's calibration) may be pooled across epochs with epoch as a grouping term, and the scatter between epochs is reported next to the pooled value. This keeps C.2's five repeats on different days possible across a mid-campaign epoch break.

## 4. Slow-demodulation script (design): `hardware/instrument/host/slowdemod.py`

(The user's note named `host/analyze.py`; it is `hardware/instrument/host/analyze.py`. The new script sits beside it and reuses `asd` and `allan_deviation`.)

Input: a run directory `runNNN_label/` with the logger's CSV (the demodulated optical output, 20 samples/s or more) and `manifest.json` (section 5). Output: `result.json` and a text report in the same directory.

1. Convert the channel to force with the day's bracketing calibration (displacement scale V/mm from A.3, kappa, lever arm, plate constant); the constants and their run ids are copied into the result.
2. Cut the record into whole modulation cycles (drop the partial cycle at each end, drop the first cycle for the thermal transient unless the run is a step run); the reference is the DUT_EN or heater square wave read back from the logger's own channel, not a nominal clock, so a dropped sample cannot rotate the phase.
3. Regress, in one least-squares fit over the kept samples: in-phase and quadrature references at f_mod and its odd harmonics up to 5, a constant, a linear and a quadratic drift, and the witness channels that rule D leaves in (temperature, tilt, field components), each high-passed at 3 times the lowest modulation frequency. Report amplitude and phase before and after the witness regression (the noise reduction is itself a result).
4. Uncertainty: the fit covariance scaled by the residual's own spectrum near f_mod (red noise makes the white-noise formula too small), cross-checked by a block bootstrap over cycles and by the split-half scatter. The reported number is the largest; a run whose three estimates differ by over a factor 1.5 is flagged.
5. Express the coupling per ampere, per watt or per kelvin; apply the Lorentz check (section 6) on lead-current runs.
6. Tests (the `test_host.py` pattern): synthetic runs with known amplitude, injected 1/f drift and known witness leakage; recovered amplitude within its stated uncertainty in over 90 % of 200 realizations; a leaked witness is removed by the regression; a driven witness (field on a lead-current run) is dropped by rule D and the signal is NOT reduced; a polarity swap flips the sign.

## 5. Provenance and the run manifest (design)

**Where files live.** In git, under `hardware/balance/campaign/`: `runs.csv`, `epochs.csv`, `provenance.csv`, and per run `runs/runNNN_label/manifest.json` and `result.json`. The raw logger CSVs stay outside git (they are large; Git LFS bandwidth is already used by the pictures) in a directory named in `epochs.csv`'s header comment, with their SHA-256 in the manifest, so a result can be checked against the file that produced it.

**`manifest.json`** (written by the logger at the start of a run, completed at its end; the analysis reads it):
`run_id, label, purpose (calibration|control|claim), run_type (T0|T1_heater|T1_tilt|T1_coil|B_cal|C3|C4|control), epoch, start, end, operator_absent, condition {lid, enclosure, lead_geometry, polarity, current_A, device_power_W, f_mod_Hz, duty}, device_config (dummy|card|leads_only), hardware {rf_ohm, led_mA, firmware_version, board_serial}, driven [channel names], channels {name: unit, source}, reference_channel, calibration_ids {start, end}, gates_version, script_version, raw {path, sha256, samples, fs_Hz}, notes`.
The logger refuses to start a run unless `epoch` is present in the manifest and exists in `epochs.csv`, and unless `purpose`, `run_type` and `gates_version` are set: a forgotten epoch entry surfaces when the run starts, not during analysis.

**`runs.csv`** (one row per run, written by the script): `run_id, start, end, epoch, purpose, run_type, label, condition (lid state and lead geometry are fields of the condition, not extra columns), device_config, rf_ohm, led_mA, firmware_version, gates_version, script_version, calib_id_start, calib_id_end, T_mean_C, T_slope_K_per_h, tilt_mean_urad, tilt_rms_urad, B_mean_uT, B_rms_uT, drive_correlated (list), gate_values (one number per gate, with its limit), gates_passed, reject_reason, result_path`. Tilt and field are given as both mean and rms; no column holds an unlabelled one.

**`provenance.csv`** (one row per measured parameter value): `param, value, unit, sigma_stat, sigma_sys, epoch, run_ids, date, method, supersedes`. Both sigmas are 1 sigma; the calibration budget in the paper needs the statistical and the systematic part separately. `params.py` keeps its `[assume]` tag until a row exists; then the tag is `[meas: epoch E, runs a-b]` and the number in the file equals the row.
Smoke checks (when the files exist): every `[meas]` tag in params.py has a provenance row whose value agrees to the number of significant figures stated in the row (not as an exact float); no `claim` or `control` run id appears in `provenance.csv`; every `runs.csv` epoch exists in `epochs.csv`.
**`epochs.csv`**: `epoch, start, trigger, ballast_g, pads, strip_id, frame_material, enclosure, device_config, rf_ohm, led_mA, firmware_version, location_note`; a row is appended (by the agent, when the user reports a change) before the next run; the logger check above catches a miss.

## 6. Second scale check, witness regression, modulation frequency

- **Lorentz scale check.** For a lead-current run the predicted force is B I L with B from the MMC5983MA at the leads (the field channel is driven in that run and is excluded from the regression by rule D, but it is read here as a measurement), I from the logger and L from the lead geometry; compare it with the force read through the plate calibration. Agreement within the combined uncertainty or one of the two has an error. The field and its gradient at the leads dominate the error (the magnetometer sits on the board, not at the leads): a consistency test, not a calibration, until the field is mapped along the leads.
- **Witness channels.** The gain of the regression is the ratio of residual ASD to raw ASD at f_mod, reported per run; analysis only, no hardware change.
- **Modulation frequency and integration time.** After T0, pick f_mod and the cycle count where the measured, witness-regressed force ASD is lowest, with f_mod below the resonance (0.215 Hz) and at least 10 cycles per run. f_mod is a condition, not an epoch; a change of the claim runs' f_mod after rule F needs a new `gates_version` entry and is reported.

## 7. How the upgrade studies connect

`material_study.py --terms` ranks which term limits at each stage (air, then vacuum) with the model's current assumptions. Its output is a prediction to be replaced by the transfer coefficients of T1; the first heater-step result (nN per K) replaces the handbook CTE x path and re-ranks.
The ranking and the vane sketch are summarised in [kb/balance_design_notes.md](kb/balance_design_notes.md) (section "2026-11-23 upgrade study"). The repo scope and rename discussion is in [scope_and_rename.md](scope_and_rename.md).
