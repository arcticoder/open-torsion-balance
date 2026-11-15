# TODO — agent, blocked

> Open items are in `docs/TODO-agent.md`; finished items in `docs/TODO-completed.md`.

These wait on the user's balance build (see `TODO-arcticoder.md`) or on the assembled board. The main board is no longer waiting on A5 (fab-assembled electronics, no breadboards); its JLC order is the user's task 1 in `TODO-arcticoder.md`.

## Design work waiting on the user
- [ ] Printed enclosure (decided 2026-11-12: printed walls and lid, 1.2 mm plates with a 2 mm rim, no window; model `hardware/balance/enclosure_printed.py`, plan and estimates `kb/balance_design_notes.md`): print after the frame (posts, bars, base); slice each window-sized file the day before its window (runbook step A1), grey walls, red lid, black strips; update `assembly.md` and `fabrication.md` text from acrylic to printed when the first plate is printed (the CAD, params and smoke test already say printed).
- [ ] Multi-object plate settings (strips need no reprint: the H-strips' missing section is by design and none is torn; fine stringing remains from many travels between objects). Before slicing the first enclosure plate, try nozzle about 210 C and retraction about 1.0 mm and fewer objects per plate, and compare. Condition: a print window after 2026-11-21 is assigned (slice the day before it).

## `clamp_plate` JLC order: cancelled 2026-11-08 (shipping C$8.14 for 0.14 kg); rides in the main-board order
- [ ] Add the Gerber set (`clamp_plate_gerbers.zip`, 16 x 14 mm, 1.2 mm, HASL with lead, Single PCB, 5 pieces) to the main-board checkout with Combine Shipping on (`TODO-arcticoder.md`, task 1) and read the total. The Black Friday coupons do not cover it alone (checked 2026-11-14 on the account's coupon page): BF Prototype $8 needs over C$28.48 of goods, BF Shipping $5 and New User Shipping need over C$28.48 / C$21.36 of shipping; the goods-only coupons (New User PCB, JLCONE PCB $5) take nothing off shipping. Combining is the way to remove its separate shipping; whether PCB and PCBA lines can share one parcel is unconfirmed until the checkout shows it. The user accepts the four spare boards as waste and will not pay a shipping premium for them.

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
