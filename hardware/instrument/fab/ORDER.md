# Main board — JLCPCB Standard PCBA files (generated 2026-11-12 by `layout/mainboard.py fab`)

Files: `main_board_gerbers.zip` (F/In1/In2/B copper with the filled GND plane on In1, masks, silk, paste, outline, PTH and NPTH drills), `bom.csv` (46 lines, 164 parts, every part has an LCSC number), `cpl.csv` (164 rows, top side, KiCad rotations and positions). Rebuild: `~/.venvs/lab-hw/bin/python hardware/instrument/layout/mainboard.py fab` (it fills zones with the system Python's pcbnew first; the venv cannot).

Board: 120 x 90 mm, 4 layers, 1.6 mm, one design, single board (no panel: it is over the 70 x 70 mm Standard PCBA minimum). Minimum track 0.10 mm, clearance 0.15 mm, vias 0.6/0.3 mm, copper to edge 0.2 mm; four M3 holes. Suggested quote fields: FR-4, 4 layers, 120 x 90 mm, 1.6 mm, HASL with lead or ENIG (the ADC and DAC are fine-pitch: ENIG is the safer finish; check the price difference), PCBA Standard, top side only, Confirm Production File yes. JLC prices are not stated here: they come from the quote page (read through the JLCONE app or the user's words).

## Before ordering (user steps, JLC's placement preview)
Rotations and polarity are KiCad's. Confirm in the placement preview: USB-C and the six 4-pin and four 2-pin JST-SH connectors face outward, LED polarity (status LEDs), crystal pin 1 (RP2040 and ADC), the ESD array and the SOT-23 parts. Anything JLC shows rotated is fixed in `place()` or by a per-footprint rotation offset in `fab()`.

## State of the layout (2026-11-12)
DFM gate: no blocking item. 415 connections routed, no shorts, no clearance errors. Decisions in effect: Y-branches with 45 degrees between legs accepted (user), joints inside a same-net pad and legs under 0.09 mm not counted, In1 is the only plane (the In2 power pour was dropped: `kb/main_board_layout_notes.md`). Board size against JLC's price tier: the user's decision after reading the quote.

## Order route decided 2026-11-15: Economic PCBA, U7 not placed
Decision (user): Economic PCBA, PCBA quantity 2 (PCB quantity 5, 4 layers, 1.6 mm, HASL with lead, top side), nitrogen reflow stays on (required for Economic, C$1.22). U7 (LIS2DW12TR, the floor-acceleration sensor in LGA-12) is Standard-only: it is left off `bom.csv` and `cpl.csv` (`DNP_FIRST_ARTICLES` in `layout/mainboard.py`; the footprint stays on the board, unpopulated) since 2026-11-18, so JLC's BOM page no longer asks about unselected parts and the first articles have no accelerometer (not needed for the force measurement or the calibration; a small breakout can add one later). The BOM carries C53-C55 as the basic C29823 (1206B475K500NT, 4.7 uF 50 V X7R 1206, same footprint) instead of the extended C132170. Quote read on the BOM page after these changes (2026-11-15): PCB C$45.13 + PCBA C$171.53 = C$216.66 before coupons (Standard at the same quantity would be about C$270). To change the route, re-upload `bom.csv` and `cpl.csv`, then answer the two "Do not place" dialogs.

