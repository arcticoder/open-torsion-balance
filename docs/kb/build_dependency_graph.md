# KB: balance build dependency graph (written 2026-11-20)

Audience: future LLM sessions. Purpose: decide when to tell the user that assembly (`docs/assembly.md`) can start, and in what order the user's tasks go in `TODO-arcticoder.md`. The user relies on this graph and does not start assembly until told. Update the status column whenever a parcel lands or a print finishes.

## Gates (status 2026-11-20)

| Gate | What it unlocks | Status |
|------|-----------------|--------|
| G-base | base print | Sat 2026-11-21 window |
| G-P1 | AliExpress 2026-11-10 parcel: stainless M3 washers (none in inventory), LR44 cells (calipers, scale), hacksaw blades, needle files, JST-SH cable, scale, 1 g weight | arrived 2026-11-20 except the LR44 cells (calipers unusable until they land; the files are flat) |
| G-P2 | AliExpress 2026-11-14 parcel: safety glasses, 1-20 g weights | ARRIVED 2026-11-26 (glasses in `CUT + FILE`, weights in `CALIBRATION`; weights not yet weighed) |
| G-CP | `clamp_plate` (JLC, 5 boards) | ARRIVED 2026-11-26 (in `BALANCE MATERIALS` > `FAB BOARDS`) |
| G-walls | 8 enclosure wall plates printed (strips are done) | not booked |
| G-lid | 4 lid tiles printed | not booked |
| G-MB | main board (JLC, 2 assembled) | in production, est. ship about 2026-11-24 |
| G-tools | craft knife (X-acto), 30 cm steel ruler, bubble level owned; ground wire: the pre-cut 0.5 mm (24 AWG) tinned copper wires with 1.3 mm insulation (they fit the 1.6 mm plated tab hole; jump wires are not inventoried); the user's nearest Phillips driver fits an M3 head (nothing more to inventory) | nearly clear |

## Assembly steps and what each needs

| Step (assembly.md) | Needs | Earliest |
|--------------------|-------|----------|
| 2a strip cut | strip guide (printed), sheet (in hand), craft knife + steel rule + file edges | G-tools, G-P1 (files) |
| 2b ballast cut | printed saw guide and handle (done), blades, glasses, 4 x M3x14 | G-P1 and G-P2 (blade grip test first) |
| 3 damper discs | printed holder (done), discs, foam tape (in hand) | startable now; can wait for step 4 |
| 4 frame | base printed, M3x12 and nuts (in hand), washers | G-base, G-P1 |
| 5 hang strip and arm | step 4, strip (2a), `clamp_plate`, `clamp_ground` (in hand), arm (in hand), M3x10, stainless nuts, ground wire | G-CP, G-tools |
| 6 ballast, vane, device card | ballast (2b), vane pad (in hand), step 5 | see device-card gap |
| 7 trim and zero | steps 4-6, enclosure wall plates in place (lid off), bubble level, scale | G-walls |
| 8 calibration electrodes | elec_board (in hand), JST-SH cable, step 7 | G-P1 |
| 9 enclosure | all walls, lid tiles, strips, foam tape | G-walls, G-lid |
| bringup.md | main board, USB-C cable, multimeter, 10 ohm 1 W and 2.2 kohm resistors | G-MB; independent of the mechanics |

G-P1 cleared 2026-11-20. Remaining blockers: base (G-base), G-CP for step 5, G-P2 for the cut, G-walls for the trim. The electronics bring-up (G-MB) is likely the first hands-on task after Saturday's base. Tell the user when G-base, G-CP and the screwdriver pick are done; that is the signal to move assembly steps 2-5 into `TODO-arcticoder.md`.

## Device-card gap (found 2026-11-20)

`fabrication.md` says the 16 x 24 mm device card is "with the main order", but the main board order (placed 2026-11-18) does not contain it, and no Gerber, BOM or CPL exists for it (only the `dut_card.stl` placeholder and a silkscreen note on the arm board). It matters only for the lead-current runs (`procedures.md` C.3), where a 10 ohm resistor on the arm is used. Stand-in for the first trim and the noise run: a dummy of about 2 g at the card position (a spare `elec_board`, 24 x 34 x 1.2 mm FR4, about 1.8 g by volume estimate; weigh it on the scale when it arrives), re-trimmed when a real card goes on. The card needs to be a JLC SMT-assembled board (no hand soldering) and should ride in a JLC order that is not tiny (no shipping premium for a small order). Parked in `TODO-BLOCKED.md`.

## Print remainder (estimates from `balance_design_notes.md`)

After the base only the enclosure is left: 4 wall plates of 148 x 150 (about 46 min, 26 g), 4 of 100 x 150 (two per plate, about 62 min per plate), 4 lid tiles (about 58 min, 30 g, one per plate). About 9 h of printing in 10 plates; bed under 40 C before removal adds about 10 min per plate. Walls are needed at the trim, the lid only at the final enclosure step.

## Booked print windows (user, 2026-11-20) and the assignment

The user's windows are availability, not a quota (more print days follow; do not push). Planned fill: Sun 11-22 07:30-09:30: 2 big wall plates (10 min start + 46 + about 10 swap + 46). Sun 13:00-16:30: 2 big plates + 1 small pair (62). Wed 11-25 19:30-22:00: second small pair + 1 lid tile. Sat 11-28 07:30-12:00: 3 lid tiles. Walls done by Wed 11-25; lid done 11-28. Grey loaded for Sunday, red for the Wednesday lid tile. Slice the day before each (TODO-BLOCKED).

Ballast fit: the user pushed the uncut 10 mm rod through the arm's 10.2 mm hole, snug but not tight (2026-11-20); no caliper work until the cells arrive.

## Spending stance (2026-11-20)

The user is spend-shy after the UPS main-board order; JLC shipping scales about linearly, so bundling JLC items saves nothing. Propose no purchases; work with stock and prints.
