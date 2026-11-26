# TODO — agent, blocked

> Open items are in `docs/TODO-agent.md`; finished items in `docs/TODO-completed.md`.

These wait on the user's balance build (see `TODO-arcticoder.md`) or on the assembled board. The main board is no longer waiting on A5 (fab-assembled electronics, no breadboards); its JLC order is the user's task 1 in `TODO-arcticoder.md`.

## Design work waiting on the user
- [ ] Print the redesigned hacksaw handle (`fixture_hacksaw_handle_body`/`_cover`, regenerated 2026-11-22 for the measured pinned blade: 6 x 0.8 x 153.5 mm, pin 1 x 5 mm at 3 mm from each end, pin holes 1.4 mm, groove 6.3 x 0.9 mm; smoke checks pass; about 72 min, 40 g like the first one, body cover-recess up, cover flat). Slice the day before a print day announced at 8 C or warmer; then the user does the grip test.
- [ ] Remind the user when the LR44 cells for the calipers arrive (AliExpress promises 2027-01-13): then measure the torsion strip's width and thickness and the ballast; the calipers are unusable until then. Condition: the user reports the cells.
- [ ] Base (`base.stl`, 218 x 218 x 6 mm, the whole 220 mm bed) failed twice on 2026-11-21 at balcony 4 C (attempt 3 lifted after about 30 min): decide a fix before reslicing: smaller or split base, brim, or print on a warmer day; then reslice and run the 4 h 28 min job. Condition: the user says a print day starts (he checks the weather; no printing below 8 C outdoors).
- [ ] Enclosure plates still to print: grey `encl_print_wall_px_a` (SLICED: `balance_p13_wall_px_a_20261122.gcode`, 1 h 3 min, 33.9 g), `py_a` (slice: probably `rotate [-90,0,0]`, check bottom_surface about 21 % and no bridge role), the four `_b` walls (two per plate, 100 x 150, slice), four red lid tiles (slice). Done 2026-11-22: `nx_a`, `ny_a`. Condition: the user announces a print day at 8 C or warmer; slice the remaining ones the day before.
- [ ] Printed enclosure (decided 2026-11-12: printed walls and lid, 1.2 mm plates with a 2 mm rim, no window; model `hardware/balance/enclosure_printed.py`, plan and estimates `kb/balance_design_notes.md`): print after the frame (posts, bars, base); slice each window-sized file the day before its window (runbook step A1), grey walls, red lid, black strips; update `assembly.md` and `fabrication.md` text from acrylic to printed when the first plate is printed (the CAD, params and smoke test already say printed).
- [ ] Multi-object plate settings (strips need no reprint: the H-strips' missing section is by design and none is torn; fine stringing remains from many travels between objects). Before slicing the first enclosure plate, try nozzle about 210 C and retraction about 1.0 mm and fewer objects per plate, and compare. Condition: the user says a print day starts at 8 C or warmer (slice the day before it).

## Written procedures that need data or hardware to finish
- [ ] Write the campaign writer (`hardware/instrument/host/campaign.py`): per run, apply the frozen gates to the manifest and logger CSV, call `slowdemod.demodulate`, write `result.json` and append the `runs.csv` row (gate values, drive-correlated witnesses); then the eight-gate checks of `docs/campaign_loop.md` section 3 with real thresholds. Condition: the first T0 record exists (the accelerometer and excursion thresholds and the first `gates_version` come from it).
- [ ] Measure the eddy vane's damping with a plain pad and a slit pad (`hardware/balance/eddy_vane_sim.py` predicts the slit pad at 0.67x the plain pad for one slit along y and 0.15x for a four-slit comb; the sketch also puts the plain pad at about 0.56x the field-integral value, i.e. zeta nearer 0.22 than the 0.40 assumed). Condition: the balance runs and A5 step 4 (decay test) is done.
- [ ] `hardware/instrument/firmware/bringup_analog.py`: scripted `[PASS]`/`[FAIL]` versions of the LED-sink, plate-driver, device-current and motor steps of `docs/bringup.md` section 4 (needs the board; the checks and limits are in that section).
- [ ] The slow-demodulation analysis script for the measurement campaign (`docs/procedures.md` section C, step 6): demodulate the logged deflection at the modulation frequency and report force per ampere or per watt with uncertainties; write it with the first real data.
- [ ] Fill the paper skeleton (`docs/paper/main.tex`): every `\todo{}` is a measurement or a figure; the results sections wait on A5 and the campaign.

## A5 — prototype noise measurement (needs the printed balance and the assembled main board with the sensor heads)
- [ ] Test the mechanics and the optical readout's displacement sensitivity on the bench: the printed/FR4 balance, the assembled main board (its optical readout and digital lock-in) and the sensor heads.
      Compare the measured resonance, Q and displacement noise, the optical photocurrent (Rf) and the trim procedure's real numbers with G2/G3; update `params.py`, rerun `tools/force_noise_budget.py`.
      A disagreement over a factor of a few sends the design back to G2/G3, not to the fab.

## WP8 remainder — needs the main board (after WP7) to test
- [ ] Device-side `hardware/instrument/firmware/main.py`: acquisition loop on DRDY, lock-in per period (`lockin.py`), sensor polling at 1 Hz, `protocol.py` packets over USB CDC (a 32-frame ADC packet every 4 ms), the safe
      start order (DAC 0 V, gates off, boost off, then enable) and a watchdog that turns the LED gates, device current and boost off if the host stops talking.
- [ ] LED modulation by PIO (a square wave on `LED1_MOD`/`LED2_MOD`, 1 kHz = 4 ADC samples on, 4 off at 8 kSPS, locked to the ADC frame count) and the DRDY-driven ADC read by PIO + DMA
      (`lab` `docs/kb/rp2040_performance_notes.md`); port `lockin.py` to viper with 16-bit input (`in_shift` 8) and compare it with the Python reference on the same samples.
- [ ] Run `bringup_adc.py` and `bringup_sensors.py` on the board and record where the real chips differ from the fakes (the lists of unverified assumptions are in the KB); verify the LIS2DW12 register values against
      ST's data sheet first (the download was blocked).
