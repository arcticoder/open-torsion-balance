# Session handoff — chat 16 final, 2026-11-20 (replace at each handoff; do not append)

## State
- **Printing (K1-FA35, 192.168.1.70):** printed so far: plate 1, small plate, gantry, posts nn/np/pn/pp with their bars, strip guide, two calibration riders, four wall strips, two lid strips, and (2026-11-15, 16:15-17:37, red spool, normal start, no errors, user: matches the STL files) the hacksaw handle body and cover. Moonraker totals 12 jobs, 14.06 h. **Left:** the base (`balance_p2_base_20261114.gcode`, re-sliced 2026-11-14 on Sonnet: 4 h 28 min, 152.7 g, sparse infill 20 % so it fits Saturday 2026-11-21 07:30-12:30 with the 10-minute normal start; sliced extents reach 218.9 x 219.9 mm of the 220 mm bed; black filament must be loaded back over the red: a swap needs about 110 mm of push at 225 C), then the grey wall plates and red lid tiles (slice the day before each window). The first print after a power-on uses the normal start. Details, load sequence and the Orca settings: `kb/printing_state.md`; printer side: `~/Code/sysadmin/wsl/docs/print-session-runbook.md` (A-G) and `kb/apps/k1-moonraker.md`. Slicing only on Sonnet or better.
- **Strips:** none is torn; the missing section of the nx/px H-strips is by design (it had been misread as a print error). Only stringing and brim marks remain; the user deburrs as needed; no reprint. The multi-object settings idea (nozzle about 210 C, retraction about 1.0 mm, fewer objects per plate) is untested and waits for the first multi-object enclosure plate (`TODO-BLOCKED.md`).
- **Orca MCP timeouts:** the cause was leftover `uvx orcaslicer-mcp` bridges and a second instance holding port 13130, not a dialog: preflight in runbook section G. `new_project` needs `if_unsaved: "discard"` and keeps the print/filament edits.
- **Brass ballast: DECIDED 2026-11-13.** One 15 mm hacksaw cut (plus 0.5 mm to file off) of the 10 x 100 mm brass rod in the printed saw guide; the Dremel route is SHELVED. The printed pad-saw handle (`fixtures.hacksaw_handle`) is printed. The cut waits on the safety glasses and the 1-20 g weight set (AliExpress order placed 2026-11-14) and the blades (2026-11-10 parcel, in transit); first test that the blade holds under hand pressure in the handle. No mask or Z87.1 mark needed.
- **Enclosure: DECIDED printed** (1.2 mm plates, 2 mm rim, lid tiles 2 mm, no window; grey walls, red lid, black strips): `hardware/balance/enclosure_printed.py`, estimates in `kb/balance_design_notes.md`; `assembly.md`/`fabrication.md` still say acrylic until the first plate is printed.
- **Calibration:** added inertia; riders printed; the weight set (1/2/5/10/20 g, listing 1005005974937195, C$2.73) was ordered with the glasses on 2026-11-14 (weights' diameters unknown; the rider seat is 10 mm).
- **Main board: ORDERED 2026-11-18 (user), IN PRODUCTION at JLC since 2026-11-20 05:50** (order label Y11; long order numbers are redacted everywhere): PCB 5 pcs ($31.70) + Economic PCBA 2 pcs ($120.86, U7 left off the BOM/CPL via `DNP_FIRST_ARTICLES` in `layout/mainboard.py`, 45 parts), merchandise $152.56, UPS Worldwide Express Saver $30.97 (0.76 kg), discount -$33.21 (JLCONE 20% Off, Max $200, chosen at the payment page), total $150.32 (about C$215; order pages are USD). File approved 2026-11-18 20:34; status Data Preparation. Duty, tax and UPS clearance fees are billed at delivery and are NOT in the total: ask the user for the amount when it lands and log it. Next: arrival (cart estimate said about 2026-11-24, UPS 3-5 days after build), then `docs/bringup.md` (skip the LIS2DW12 check).
- **Why UPS:** Global Standard Direct Line is refused for orders over US$99 of merchandise ("the express delivery method requires the order amount to be less than 99.00$"; the C$24.06 figure I had quoted was only the cart estimate); JLC will not split one order into parcels (user asked support); splitting into several orders repeats about C$50 of fixed fees per order and the PCBA line alone (C$172.79) exceeds the cap; splitting the board into two boards was analysed (about break-even in cost with two coupons, several sessions of redesign) and not chosen. Possible reason for the cap (insurance or declared-value limit) is unconfirmed. A PCBWay/Seeed assembly quote was offered as an optional comparison and was not pursued.
- **Coupons (one per order):** checkout takes ONE coupon per order (terms agree); the cart shows only its own pick, the payment page's selector lets the user choose a better one (the 20% beat the cart's -C$42.91). Black Friday campaign 2026-11-18 to 12-02; flash coupons claimed 2026-11-18 on the user's instruction (button.ticket-btn): PCBA $50 off $100, $30 Off $50 (ALL and PCB), JLCONE 26 BF PCB $20 Mega, JLCONE 26 BF 10% Off (to 2026-12-03), JLCONE PCBA $20 (to 12-15) still unused; used: JLCONE 20% Off, JLCONE PCB $5, JLCONE $8 PCB Coupon. A coupon never takes a goods line to $0 (customs: the `clamp_plate` order got only US$1.20 off). Ledger: `lab/docs/jlc/coupons.md`.
- **clamp_plate: ordered alone 2026-11-15 (C$9.64 total), Shipped (read 2026-11-20).** The arm (arrived 2026-11-18, 5 boards, photos `docs/img/arm_*_2026-11-18.jxl`), `elec_board` (arrived 2026-11-16: 10 boards for 5 ordered, all intact, spares; photos `docs/img/elec_board_electrode_*`) and `clamp_ground` (arrived 2026-11-14) are all in hand. AliExpress: two orders in transit (2026-11-10, 2026-11-14; `lab/docs/orders.md`). With the main board and clamp_plate parcels something is en route on every line.
- **Driving the JLCONE app (hard lessons, details in `lab/docs/kb/jlc_account_and_quotes.md`, last sections):** only trust a dialog that has a bounding rect with height (the "Terms" dialog I once reported was a hidden DOM element); use `Input.dispatchMouseEvent` at an element's centre after `scrollIntoView` (plain `.click()` often does nothing) and check with a screenshot; the quote page's PCB build time resets to "3 days PCBA Only" on each edit (click the `3-4 days` icon, maybe twice); SAVE TO CART silently does nothing until the Product Description cascader has a value; a BOM row cannot be deleted in JLC's table, so a part not to be placed is removed from the uploaded BOM/CPL and re-uploaded; the user authorised claiming coupons and going as far as the app lets in that message; never submit, pay or accept terms.
- **Privacy:** the checkout and order pages print the user's name, address, phone and card digits: never copy them. JLC order and batch numbers (W…, SMT…) and tracking numbers are redacted in every markdown file (user instruction 2026-11-20); use the short labels (Y3, Y11), dates and contents.
- **Repo state:** repository audit of 2026-11-17 fully actioned (host logger/analyzer fixes, smoke-test hardening, doc refresh; system Python runs both smoke tests with `[SKIP]`s; the venv run rewrites `hardware/balance/boards/fab/arm_cnc.dxf`, `git checkout` it). `docs/spark_application.md` is in `docs/archive/`; stray root `result.json` and `schematic_test.*` removed and ignored. The last commit's author was reset to the user's identity and its Claude trailers dropped locally; the original was already on origin, so the user must `git push --force-with-lease` (a plain `git pull` shows divergence). Commit messages in these repos never carry a Claude co-author trailer (that is what made Claude a GitHub contributor).
- **Docs refreshed 2026-11-15/17:** README, `docs/plan.md`, `fabrication.md`, `procedures.md` say printed enclosure, no breadboard A5, A5 runs on the assembled board; `assembly.md` still says acrylic until the first plate is printed.
- **Where the how-to lives:** `lab/docs/kb/jlc_account_and_quotes.md` (the app recipe, coupon rules, shipping findings, the order read of 2026-11-20), `lab/docs/jlc/coupons.md`.
- **`docs/history.md` (user-owned):** never append, edit or use as a source unless the user names lines.

## Files that carry the state

`docs/TODO-arcticoder.md` (user tasks: 1 print windows, 2 brass cut, plus the en-route list with the main board), `docs/TODO-agent.md` (0 lines), `docs/TODO-BLOCKED.md` (enclosure printing, multi-object settings, firmware/analysis items), `docs/TODO-backlog.md`, `docs/TODO-completed.md` (newest first).

## Standing rules (see `kb/project_workflow_notes.md`)

TODO-agent.md must be 0 lines at the end of every chat (do startable work; truly blocked items go to TODO-BLOCKED.md with the condition). Never commit; never add a Claude co-author in lab/sfb commits. No quotes of the user, no tone descriptions. No tracking numbers, long order numbers, card digits, names or addresses in files or chat; never print secrets. Never state a JLC price that is not from the user, a capture or a page read through the app. Say only what the transcript shows. One order per day is the user's own limit (the agent cannot enforce it, only read order dates in the JLC list). No hand-built electronics; never EasyEDA/Spark. JLC: the BOM/CPL page of a draft is not an order (the agent may read it and upload there); Save to cart, Secure Checkout and claiming coupons are done only when the user says so in that message (done for the main-board order and the Black Friday coupons); never submit, pay or accept terms. Coupons: one per order; read the payment page, not the cart, before judging them. Heat and print only on the user's explicit request in that message ("go", "begin the load sequence", "start the print" count). Clock-time visual checks only (no camera, door shut, user cannot hear it). Slicing and print prep only on Sonnet or better. Monitor notices that arrive as system events are not the user's messages. Spools live in a sealed freezer bag on a roller (no humidity advice). Park the head at about X200 Y110 for loading. The earlier rule about not asking obvious questions in print windows was removed by the user: ask when something is unclear.

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
        State (2026-11-20): the main board (WP5, 120 x 90 mm, one board, 4 layers) is ORDERED and in production at
        JLC (I placed it 2026-11-18: 5 PCBs + 2 Economic PCBA boards with the LIS2DW12 (U7) left off the BOM and
        CPL, C53-C55 on the basic C29823; JLCONE 20% Off applied; total US$150.32 including UPS shipping US$30.97;
        UPS bills duty, tax and clearance fees at delivery, which are not in that total: ask me for the amount
        when it lands). Global Standard Direct Line is refused over US$99 of merchandise and JLC will not split an
        order, so UPS it is. The arm, elec_board (10 boards arrived for 5 ordered) and clamp_ground have arrived;
        clamp_plate (ordered alone 2026-11-15) is shipped. JLC takes ONE coupon per order and the payment page's
        selector, not the cart, shows the best one; unused flash coupons run to 2026-12-03 (lab/docs/jlc/coupons.md).
        Next for the electronics: arrival, then docs/bringup.md (skip the LIS2DW12 check). The calibration uses
        added inertia (confirmed); the riders are printed; a 1-20 g weight set came with the glasses order. The
        enclosure is decided: printed PLA plates (1.2 mm with a 2 mm rim, no window; grey walls, red lid, black
        strips). The ballast is one 15 mm hacksaw cut of the 10 mm brass rod in the printed saw guide; the printed
        pad-saw handle is done (red, matches the STL); the cut waits on the safety glasses and weights (AliExpress
        order of 2026-11-14, in transit) and the blades (2026-11-10 parcel, in transit); test the blade grip first.
        My last commit's author was reset locally to my identity (the original is on origin, so I must force-push
        with --force-with-lease); never put a Claude co-author trailer on any commit.
      - Printing: the K1-FA35 is on my balcony with the door shut and I work in the office: there is no camera and
        I cannot hear it, so give me clock-time visual checks, never audible ones. I plug it in, switch it on and
        load the filament you advise (spools live in a sealed freezer bag on a roller); you run heating, homing
        and starting only when I ask in that message. Slicing only on Sonnet or better. The agent drives
        OrcaSlicer (2.5.0 flatpak, API on 13130) and the K1 through MCP and Moonraker (wsl workspace: connection
        notes, docs/print-session-runbook.md sections E, F and G, the K1 note). Printed so far: plate 1, the small
        plate, the gantry, all four posts with their bars, the strip guide, two calibration riders, the four wall
        strips and two lid strips (no strip is torn; the strips' missing H section is by design) and the hacksaw
        handle. Left: the base (sliced, 4 h 28 min at 20 % infill, Saturday 2026-11-21 07:30-12:30, black filament
        loaded back over the red with about 110 mm of push), then the grey wall plates and red lid tiles. The first
        print after a power-on uses the normal start (runbook section E); later prints in the same session use the
        fast start.
      Constraints: no hand soldering; fab boards use only JLC's machine-placed SMT parts; USB power, under
      50 V DC / 30 V AC; PLA only on my Creality K1; AliExpress for stock parts (no single-item shipping fees),
      JLC PCB/PCBA/3DP/CNC when fabrication beats buying and cutting by hand; design to stock sizes. I'm in
      Canada and JLC prices on my account are in CAD on the cart and in USD on order pages. I will not pay a
      shipping premium for a tiny order, and I dislike courier customs fees.
      JLC quote, BOM/CPL, cart, message, coupon and order pages can be read and driven through my JLCONE desktop app
      when I launch it with --remote-debugging-port=9222 (recipe and gotchas in lab/docs/kb/jlc_account_and_quotes.md:
      only trust a dialog with a visible bounding box, click with Input.dispatchMouseEvent and check with a
      screenshot): text reads, paced clicks, uploads of this repo's own Gerber, BOM and CPL files (a draft's BOM/CPL
      page is not an order). Never call JLC's API, never touch the cookies, never accept terms for me, never submit
      or pay; Save to cart, Secure Checkout and claiming coupons only when I say so in that message: I approve and
      pay, and I place at most one order per day. Treat any JLC price not from my words, my captures or a page read
      through the app as an estimate. Never put parcel tracking numbers, long JLC order numbers, card digits, my
      name or address, or secrets in chat or files (they are redacted in the markdown files). Only say you did
      something if the transcript shows it.
      docs/history.md is my chat transcript: never append to it (I paste the full summary myself), don't edit
      existing text, and don't use it as an analysis source unless I name lines to read. Pictures are lossless
      .jxl (keep them small, about 0.5-0.7 MB); .jxl and .eprj2 are Git LFS (the .eprj2 is leftover from the
      dropped route; I decide whether to keep it). Don't commit anything in these repos: I stage and commit
      everything after each chat.
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

Both `docs/kb/README.md` files, `lab/docs/kb/jlc_account_and_quotes.md` (last sections), `docs/kb/printing_state.md`, `hardware/instrument/fab/ORDER.md`, `docs/TODO-arcticoder.md`, `docs/TODO-BLOCKED.md`, `~/Code/sysadmin/wsl/docs/kb/apps/k1-moonraker.md` and `~/Code/sysadmin/wsl/docs/print-session-runbook.md` for the printer side.
