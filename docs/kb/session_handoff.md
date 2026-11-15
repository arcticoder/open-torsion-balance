# Session handoff — chat 15 final, 2026-11-14 (replace at each handoff; do not append)

## State

- **Printing (K1-FA35, 192.168.1.70):** the 2026-11-14 morning window (07:30-10:00, extended by the user to 10:10, met) printed post pp's L (`balance_p7`, normal start 07:10), four wall strips (`balance_p8`, fast start 08:14) and two lid strips (`balance_p10`, fast start 09:29), all black, no errors; Moonraker totals 11 jobs, 12.03 h. Printed so far: plate 1, small plate, gantry, posts nn/np/pn/pp with their bars, strip guide, two calibration riders, six strips. **Left:** the hacksaw handle (`balance_p9_hacksaw_handle_20261113.gcode`, body + cover, 72 min, 39.5 g, RED spool, Sunday 2026-11-15 16:30-18:30, first print after a power-on = normal start), the base (`balance_p2_base_20261114.gcode`, re-sliced 2026-11-14: 4 h 28 min, 152.7 g, sparse infill 20 % so it fits Saturday 2026-11-21 07:30-12:30 with the 10-minute normal start; bed 60 in START_PRINT checked), then the enclosure wall plates (grey) and lid tiles (red). Slicing only on Sonnet or better (user rule). All details, load/fast-start sequences, the purge-area finding, the Orca 2.5.0 settings and the strip post-mortem: `kb/printing_state.md`; printer side: `~/Code/sysadmin/wsl/docs/print-session-runbook.md` (sections E and F) and `kb/apps/k1-moonraker.md`.
- **Strips (corrected 2026-11-14):** no strip is torn; the missing section in the nx/px H-strips is by design and had been misread as a print error. Only stringing and brim marks remain; the user deburrs as needed and nothing is reprinted. The multi-object settings idea (nozzle about 210 C, retraction about 1.0 mm, fewer objects per plate) is still untested (`TODO-BLOCKED.md`).
- **Orca MCP timeouts:** cause was leftover bridge processes and a second instance holding port 13130, not a dialog; preflight in the wsl runbook section G.
- **Brass ballast: DECIDED 2026-11-13.** One 15 mm cut (plus 0.5 mm to file off) of the 10 x 100 mm brass rod with a hacksaw in the printed saw guide; the Dremel route is SHELVED; the stainless weight is not pursued. The blades (150 x 6 x 0.4 mm, 24T, no handle) are in the 2026-11-10 AliExpress parcel (in transit). **Printed pad-saw handle designed 2026-11-13** (`fixtures.hacksaw_handle`: blade clamped by an end stop and friction under a cover with four M3 x 14 screws, 6.3 x 0.30 mm groove, smoke checks pass, user approved it over the Printables link). The cut waits on the glasses (in the user's AliExpress cart, C$3.48, not yet placed; the second 1 g weight, C$2.48, is the item that clears the free-shipping line), the blades and the printed handle. No Z87.1/EN 166 mark and no mask needed for a hand cut; filing makes the only fine dust (damp-wipe it, short filing, wash hands).
- **Enclosure: DECIDED printed** (1.2 mm plates with a 2 mm rim, lid tiles 2 mm, no window): `hardware/balance/enclosure_printed.py`, plan and estimates (about 10 h, 320 g, grey walls, red lid, black strips) in `kb/balance_design_notes.md`; `assembly.md`/`fabrication.md` wording still says acrylic until the first plate is printed. The strip print times are about 16 min each at the current speeds (the old 12 min estimate was low).
- **Calibration:** added inertia, confirmed; riders printed; a second 1 g weight is staged for the next AliExpress order (`TODO-backlog.md`).
- **Main board (WP5-WP7):** layout done to the DFM gate (415/415 routed, In1 GND plane only, 120 x 90 mm, one board, 45-degree Y-branches accepted); fab files in `hardware/instrument/fab/`. Now the user's task 1 (JLC main-board order, with the placement-preview check, the board-size decision and Combine Shipping with clamp_plate); the quote page is set up in their app (Gerber zip uploaded, 4-layer HASL leaded, Standard PCBA top, 3 days, PCB part C$46.13); the BOM/CPL step (Next saves to the cart) and the placement preview are theirs; do not touch the page further. Details in the lab kb last section. BF PCBA coupons end 2026-11-27, New User SMT 2026-11-25. Read `kb/main_board_layout_notes.md` (last section), `kb/main_board_assessment.md`, `hardware/instrument/layout/SPEC.md`. pcbnew works only under `/usr/bin/python3` (3.14), not the venv (3.12).
- **JLC (read through the app 2026-11-14):** arm, elec_board and clamp_ground are all Shipped; clamp_ground arrived 2026-11-14 (five boards, all alike (the apparent colour difference in the photo was lighting, user-confirmed); photos `img/clamp_ground_*_2026-11-14.jxl`); clamp_plate rides in the main-board order with Combine Shipping (no coupon covers it alone). Recipe for the read and the Add-On Services finding: `lab/docs/kb/jlc_account_and_quotes.md` (last section). Coupons: `lab/docs/jlc/coupons.md`. AliExpress order of 2026-11-10 in transit; cart: glasses plus the second 1 g weight (user's task 2).
- **Lab and wsl repos (updated this chat):** lab `docs/inventory.md` (black spool estimate, red spool role), `docs/kb/jlc_account_and_quotes.md` (failed re-read); wsl `kb/apps/k1-moonraker.md`, `kb/apps/orcaslicer-mcp-fork.md` (Orca 2.5.0), `print-session-runbook.md` (sections A5 and F).
- **`docs/history.md` (not edited, user-owned):** the agent wrongly claimed a printer password was in it (a shape check could not tell prose from a value); the user found none. Partial tracking numbers near lines 1988-1989 are redacted by the user. Rule: mask all but the prefix of any tracking number, and never claim a secret is in a file without evidence that does not print it.

## Files that carry the state

`docs/TODO-arcticoder.md` (user tasks 1-4), `docs/TODO-agent.md` (empty, 0 lines), `docs/TODO-BLOCKED.md` (enclosure printing, multi-object settings, clamp_plate in the main-board order, firmware/analysis items), `docs/TODO-backlog.md`, `docs/TODO-completed.md` (newest first).

## Standing rules (see `kb/project_workflow_notes.md`)

TODO-agent.md must be 0 lines at the end of every chat (do startable work; move only truly blocked items to TODO-BLOCKED.md with the condition). Never append to `docs/history.md` or use it as a source unless the user names lines. Never commit. No quotes of the user, no tone descriptions. No unmasked tracking numbers. Never print secrets. Never state a JLC price that is not from the user, a capture or an app read. Say only what the transcript shows. One order per day is the user's own limit (the agent cannot enforce it; it can only read order dates in the JLC list). No hand-built electronics; never EasyEDA/Spark. Heat and print only on the user's explicit request in that message (the user saying to decide counts as the request for a preheat; after a "go", start the print and use the start-up minutes for their checks). Clock-time visual checks only. **Slicing and print prep only on Sonnet or better.** Monitor notices that arrive as system events are not the user's messages. Spools live in a sealed freezer bag on a roller (no humidity advice). Park the head at about X200 Y110 for loading, not the rear-left corner. Long jobs in the background, one change per routing run.

## Context block for the next chat (paste this)

    I'm building a small experimental-physics lab across two repos, both open in this workspace.
    - lab (github.com/arcticoder/lab): reusable bench instruments — Raspberry Pi Pico/RP2040 circuits with
      SPICE netlists, breadboard guides and pass/fail smoke tests — plus the shared parts inventory and
      order ledger (docs/inventory.md, docs/orders.md), my filament stock and tools (docs/inventory.md,
      "Filament" and "Tools", including a Dremel 3000), and my JLC account notes (docs/jlc/: coupons read from
      my account, captures and reads of JLC's quote pages, docs/kb/jlc_account_and_quotes.md).
    - spurious-force-balance (github.com/arcticoder/spurious-force-balance): the first experiment — an open,
      low-cost torsion balance that quantifies the spurious forces (supply-lead Lorentz forces, heating,
      convection) that dominate small-thrust measurements. Printable mechanics (CadQuery), FR4 fab boards for
      the arm and electrodes, a force-noise model, and JLCPCB-assembled RP2040 electronics (KiCad 9, SKiDL,
      ngspice, MicroPython firmware tested on the host). KiCad/SKiDL is the design source: I dropped the
      EasyEDA/Spark route on 2026-11-01 (shelved; never offer EasyEDA, Spark, its MCP or the validator again).
      No more hand-built electronics: the instrument is fab-assembled boards.
      State (2026-11-14): the main board (WP5) is laid out to the DFM gate: 120 x 90 mm, one board, In1 ground
      plane only, all 415 connections routed, 45-degree Y-branches accepted; fab files are in
      hardware/instrument/fab/ (Gerbers, BOM, CPL, ORDER.md). I still have to check rotations and polarity in
      JLC's own placement preview and decide the board size against the price tier (remind me when I start that
      order). The calibration uses added inertia (confirmed); the two riders are printed. The enclosure is
      decided: printed PLA plates (1.2 mm with a 2 mm rim, no window; grey walls, red lid, black strips). The
      ballast is one 15 mm hacksaw cut of the 10 mm brass rod in the printed saw guide (Dremel route shelved);
      the blades have no handle, so a printed pad-saw handle of your design (approved) is sliced for Sunday
      2026-11-15 16:30-18:30, in red. The cut waits on the safety glasses (in my AliExpress cart, not yet
      placed), the blades and that handle; no dust mask, no Z87.1 mark needed.
      Ordering state (2026-11-14; JLC statuses read in the app today): the arm, elec_board and clamp_ground are shipped
      and clamp_ground arrived; clamp_plate is cancelled and will ride in the main-board order with Combine Shipping. My AliExpress order of 2026-11-10 (cells,
      JST-SH cable, hacksaw blades, washers, a 1 g weight, a 0.1 g scale, needle files) is in transit
      (lab/docs/orders.md). I claimed four JLC Black Friday warm-up coupons on 2026-11-12 (valid to 2026-11-27;
      lab/docs/jlc/coupons.md). The quote page for the next JLC order is set up only when I say the previous one
      is placed.
    - Printing: the K1-FA35 is on my balcony with the door shut and I work in the office: there is no camera and
      I cannot hear it, so give me clock-time visual checks, never audible ones. I plug it in, switch it on and
      load the filament you advise (spools live in a sealed freezer bag on a roller); you run heating, homing
      and starting only when I ask in that message. Slicing only on Sonnet or better. The agent drives
      OrcaSlicer (2.5.0 flatpak, API on 13130) and the K1 through MCP and Moonraker (wsl workspace: connection
      notes, docs/print-session-runbook.md sections E and F, the K1 note). Printed so far: plate 1, the small
      plate, the gantry, all four posts with their bars, the strip guide, two calibration riders, the four wall
      strips and two lid strips (the strips need deburring as I fit them; none is torn, the missing H section is by design). Left: the hacksaw handle (red, Sunday 16:30-18:30), the base
      (sliced 2026-11-14, 4 h 28 min, Saturday 2026-11-21 07:30-12:30), then the grey wall plates and red
      lid tiles. The first print after a power-on uses the normal start (runbook section E); later prints in the
      same session use the fast start.
    Constraints: no hand soldering; fab boards use only JLC's machine-placed SMT parts; USB power, under
    50 V DC / 30 V AC; PLA only on my Creality K1; AliExpress for stock parts (no single-item shipping fees),
    JLC PCB/PCBA/3DP/CNC when fabrication beats buying and cutting by hand; design to stock sizes. I'm in
    Canada and JLC prices on my account are in CAD. I will exceed JLC's 0.3 kg cheap-shipping line if that
    lowers the per-item shipping; I will not pay a shipping premium for a tiny order.
    JLC quote, message and coupon pages can be read through my JLCONE desktop app when I launch it with
    --remote-debugging-port=9222 (recipe and gotchas in lab/docs/kb/jlc_account_and_quotes.md): read-only text
    reads, a few paced clicks (I authorised Get Coupon on the campaign page once), uploads of this repo's own
    Gerber zips for quotes. Never call JLC's API, never touch the cookies, never accept terms for me, never
    Submit, Save to cart or pay: I approve and pay, and I place at most one order per day. Treat any JLC price
    not from my words, my captures or a page read through the app as an estimate. Never put parcel tracking
    numbers or secrets in chat or files. Only say you did something if the transcript shows it.
    docs/history.md is my chat transcript: never append to it (I paste the full summary myself), don't edit
    existing text, and don't use it as an analysis source unless I name lines to read. Pictures are lossless
    .jxl (keep them small); .jxl and .eprj2 are Git LFS (the .eprj2 is leftover from the dropped route; I decide
    whether to keep it). Don't commit anything in these repos: I stage and commit everything after each chat.
    Workflow: docs/TODO-agent.md is the agent's own list and must be empty (0 lines) at the end of every chat:
    do startable items, move truly blocked ones to TODO-BLOCKED.md with the exact condition (TODO-backlog.md and
    TODO-completed.md sit beside it). My hands-on tasks live in docs/TODO-arcticoder.md as separately numbered
    tasks for me only; any task or decision you give me in chat goes there too. Keep docs/kb/*.md (LLM-only
    notes) up to date with discoveries. Don't quote me or describe how I said things in files or chat. Keep an
    eye on the supply chain: always have a few AliExpress or JLC items in transit, and watch for deals.
    Start by reading docs/kb/README.md and docs/kb/session_handoff.md in spurious-force-balance, then
    lab/docs/kb/README.md and lab/docs/kb/jlc_account_and_quotes.md. Then continue from
    docs/TODO-arcticoder.md, docs/TODO-BLOCKED.md and my feedback below.

## Read first

Both `docs/kb/README.md` files, `lab/docs/kb/jlc_account_and_quotes.md`, `docs/kb/printing_state.md`, `docs/kb/main_board_layout_notes.md` (last section), `docs/TODO-arcticoder.md`, `docs/TODO-BLOCKED.md`, `~/Code/sysadmin/wsl/docs/kb/apps/k1-moonraker.md` and `~/Code/sysadmin/wsl/docs/print-session-runbook.md` for the printer side.
