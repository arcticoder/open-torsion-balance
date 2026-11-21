# TODO — agent, blocked

> Open items are in `docs/TODO-agent.md`; finished items in `docs/TODO-completed.md`.

These wait on the user's balance build (see `TODO-arcticoder.md`) or on the assembled board. The main board is no longer waiting on A5 (fab-assembled electronics, no breadboards); its JLC order is the user's task 1 in `TODO-arcticoder.md`.

## Design work waiting on the user
- [ ] Base (`base.stl`, 218 x 218 x 6 mm, the whole 220 mm bed) failed twice on 2026-11-21 at balcony 4 C (attempt 3 lifted after about 30 min): decide a fix before reslicing: smaller or split base, brim, or print on a warmer day; then reslice and run the 4 h 28 min job. Condition: the user reports a print day and the outdoor temperature.
- [ ] Slice the enclosure plates for the booked windows (grey walls, red lid; Sonnet or better, runbook step A1): the day before each window, i.e. 2026-11-21 for both Sunday windows, 11-24 for Wednesday, 11-27 for Saturday. Condition: the date.
- [ ] Printed enclosure (decided 2026-11-12: printed walls and lid, 1.2 mm plates with a 2 mm rim, no window; model `hardware/balance/enclosure_printed.py`, plan and estimates `kb/balance_design_notes.md`): print after the frame (posts, bars, base); slice each window-sized file the day before its window (runbook step A1), grey walls, red lid, black strips; update `assembly.md` and `fabrication.md` text from acrylic to printed when the first plate is printed (the CAD, params and smoke test already say printed).
- [ ] Multi-object plate settings (strips need no reprint: the H-strips' missing section is by design and none is torn; fine stringing remains from many travels between objects). Before slicing the first enclosure plate, try nozzle about 210 C and retraction about 1.0 mm and fewer objects per plate, and compare. Condition: a print window after 2026-11-21 is assigned (slice the day before it).

## Written procedures that need data or hardware to finish
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
