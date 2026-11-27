# Session handoff — chat 19 final, 2026-11-27 (replace at each handoff; do not append)

## State
- **Repo is now `open-torsion-balance`** (renamed from spurious-force-balance on 2026-11-23/25 by `gh repo rename`; fresh clone at `~/Code/python/open-torsion-balance`, in `lab/lab.code-workspace`; the user kept the old folder as `~/Code/python/spurious-force-balance.bak`; old name replaced in live text everywhere except the `history.md` files). Git identity set in the clone; commits 847c970 and 10ba3ad were rewritten to the user's identity and force-pushed (now 7886066, 2b7f93c). Scope: a general torsion balance for small forces in air with a measurement-to-metrology loop; the spurious-force study is the first campaign (`docs/scope_and_rename.md`, approved by the user; second acceptance claim fixed: non-air terms below the measured floor and floor within 1/3-3 x the model, plus a lid-lifted air test).
- **Campaign loop (`docs/campaign_loop.md`, approved):** run purposes calibration/control/claim, per-run-type gates, rule D (drive-correlated witnesses dropped from gates and regression, set fixed in advance and checked on pooled controls), rule F (gates frozen per epoch after its T0), rule P, epochs = hardware states, lead geometry gets its own kappa/zeta run, provenance tables in `hardware/balance/campaign/` (empty; `config.json`: raw files `~/data/open-torsion-balance/raw`, backup `/mnt/d/open-torsion-balance-data/raw_backup`). Implemented: `hardware/instrument/host/slowdemod.py` (+ `test_slowdemod.py`, in the instrument smoke test; high-pass cut-off is f_mod/3), the logger's `--manifest`/`--bench` check, provenance smoke checks. Waits on the first T0 record (TODO-BLOCKED): the campaign writer and gate thresholds.
- **Upgrade study:** `hardware/balance/material_study.py --terms` (air is 98 % of the total in air; frame path PLA to FR4 halves the total only in vacuum; then floor tilt/acceleration via `COM_OFFSET` limit) and `eddy_vane_sim.py` (sheet-current solver: plain pad c = 5.2e-2 N s/m, 0.56x the no-return-path value so zeta may be about 0.22, not 0.40; slits only lower damping; `DAMPING_RATIO` unchanged until A5 step 4). Details in `kb/balance_design_notes.md`.
- **Orders and arrivals:** JLC `main_board` (placed 2026-11-18, Economic PCBA, U7 not placed, total US$150.32) reads SHIPPED via UPS on the orders tab (reload the tab to refresh; no tracking number kept); duty/tax/clearance at delivery: ask the user for the amount. `clamp_plate` x5 arrived 2026-11-26 (filed `FAB BOARDS`): all fab boards are now in hand except the main board. Safety glasses (`CUT + FILE`) and the 1/2/5/10/20 g set (`CALIBRATION`, not weighed, away from the N42 discs) arrived 2026-11-26. LR44 cells promised 2027-01-13 (remind the user to measure the strip and ballast then). No purchases proposed (spend-shy).
- **Printing, 2026-11-25 (window to 22:00, 21 C):** grey `px_a` (normal start 19:32:38, 61.7 min) and `px_b` (fast start 20:58:17, 43.2 min) printed well; Moonraker totals 19 jobs, 17.7 h. Printed overall: plate 1, small plate, gantry, four posts with bars, strip guide, two riders, four wall strips, two lid strips, first (obsolete) hacksaw handle, grey `nx_a`, `ny_a`, `px_a`, `px_b`. Left: `py_a` (SLICED `balance_p14_wall_py_a_20261125.gcode`), `py_b`, `nx_b`, `ny_b` (about 45 min each, `rotate [0,90,0]`), four red lid tiles, the base (parked: brim, smaller or warmer day), the redesigned hacksaw handle (about 72 min; the brass cut waits on it and a grip test). Lessons in the wsl runbook section I (first-layer look = upload + 9-11 min on the normal start).
- **Hacksaw blade:** pinned, 6 x 0.8 x 153.5 mm, sawtooth; the teeth face whichever way it is laid (a choice, not an unknown: push cut = teeth away from the handle).
- **Torsion strip:** one cut and bagged `TORSION STRIP`; a spare is cut just in time. Damper discs seated.
- **Photos and zips from the user:** look at every one once, write findings to the KB, delete the zip and loose files; never ask. **Previews:** name objects, say whether they touch, leave previewable STLs. Do not announce "nothing is committed".
- **Assembly steps startable now (user's list):** the brass cut after the new handle; most mechanics wait on the base (frame) and the walls (`kb/build_dependency_graph.md`). Electronics: wait for the main board, then `docs/bringup.md` (skip the LIS2DW12 check).

## Files that carry the state

`docs/TODO-arcticoder.md` (user tasks: return the grey spool/printer if not yet done, the brass cut, weigh the 20/10/5 g pieces, plus the en-route list), `docs/TODO-agent.md` (0 lines), `docs/TODO-BLOCKED.md` (print remainder, handle print, base fix, caliper reminder, firmware/analysis items), `docs/TODO-backlog.md`, `docs/TODO-completed.md` (newest first).

## Standing rules (see `kb/project_workflow_notes.md`)

TODO-agent.md must be 0 lines at the end of every chat (do startable work; truly blocked items go to TODO-BLOCKED.md with the condition). Never commit; propose no purchases; never add a Claude co-author in lab/open-torsion-balance commits. No quotes of the user, no tone descriptions. No tracking numbers, long order numbers, card digits, names or addresses in files or chat; never print secrets. Never state a JLC price that is not from the user, a capture or a page read through the app. Say only what the transcript shows. One order per day is the user's own limit (the agent cannot enforce it, only read order dates in the JLC list). No hand-built electronics; never EasyEDA/Spark. JLC: the BOM/CPL page of a draft is not an order (the agent may read it and upload there); Save to cart, Secure Checkout and claiming coupons are done only when the user says so in that message (done for the main-board order and the Black Friday coupons); never submit, pay or accept terms. Coupons: one per order; read the payment page, not the cart, before judging them. No printing below 8 C outdoors (the user decides print days); heat and print only on the user's explicit request in that message ("go", "begin the load sequence", "start the print" count). Clock-time visual checks only (no camera, door shut, user cannot hear it). Slicing and print prep only on Sonnet or better. Monitor notices that arrive as system events are not the user's messages. Spools live in a sealed freezer bag on a roller (no humidity advice). Park the head at about X200 Y110 for loading. The earlier rule about not asking obvious questions in print windows was removed by the user: ask when something is unclear.

## Context block for the next chat (paste this)

    I'm building a small experimental-physics lab across two repos, both open in this workspace.
      - lab (github.com/arcticoder/lab): reusable bench instruments — Raspberry Pi Pico/RP2040 circuits with
        SPICE netlists, breadboard guides and pass/fail smoke tests — plus the shared parts inventory and
        order ledger (docs/inventory.md, docs/orders.md), my filament stock and tools (docs/inventory.md,
        "Filament" and "Tools", including a Dremel 3000), the storage-bag filing plan (docs/inventory.md,
        "Filing plan"; photos in docs/img/tools_bags_2026-11-20/) and my JLC account notes (docs/jlc/:
        coupons read from my account, captures and reads of JLC's quote pages,
        docs/kb/jlc_account_and_quotes.md).
      - open-torsion-balance (github.com/arcticoder/open-torsion-balance, renamed from spurious-force-balance;
        the old folder survives as spurious-force-balance.bak, ignore it): an open, low-cost torsion balance for
        measuring small forces in air, with a documented loop that feeds each campaign's calibration data back
        into the instrument's metrology (docs/campaign_loop.md, docs/scope_and_rename.md; both approved). The
        first campaign quantifies the spurious forces (supply-lead Lorentz forces, heating, convection) that
        dominate small-thrust measurements; the next ones are materials and geometry for the frame and damper,
        chosen by simulation (hardware/balance/material_study.py --terms, eddy_vane_sim.py) and checked by
        injected-signal transfer coefficients. Printable mechanics (CadQuery), FR4 fab boards for the arm and
        electrodes, a force-noise model, and JLCPCB-assembled RP2040 electronics (KiCad 9, SKiDL, ngspice,
        MicroPython firmware tested on the host). KiCad/SKiDL is the design source: I dropped the EasyEDA/Spark
        route on 2026-11-01 (shelved; never offer EasyEDA, Spark, its MCP or the validator again). No more
        hand-built electronics: the instrument is fab-assembled boards.
        State (2026-11-27, end of chat 19): the main board (WP5, 120 x 90 mm, 4 layers) was placed 2026-11-18
        (5 PCBs + 2 Economic PCBA boards, LIS2DW12 (U7) left off the BOM and CPL; total US$150.32 including UPS
        shipping US$30.97) and now reads SHIPPED on JLC's orders page (UPS). UPS bills duty, tax and clearance
        at delivery, not in that total: ask me for the amount when it lands. JLC takes ONE coupon per order;
        unused flash coupons run to 2026-12-03 (lab/docs/jlc/coupons.md). All other fab boards are in hand
        (arm, elec_board, clamp_ground, clamp_plate). Next for the electronics: arrival, then docs/bringup.md
        (skip the LIS2DW12 check). The device card (16 x 24 mm FR4, 10 ohm, only for the lead-current runs) has
        no design and is not in the main order; a spare elec_board stands in as dummy mass (TODO-backlog). The
        safety glasses and the 1/2/5/10/20 g nickel-plated-steel weight set arrived 2026-11-26 (glasses in
        CUT + FILE, set in CALIBRATION, keep it away from the damper magnets; the set is not weighed yet, my
        task). The LR44 cells for the calipers are promised 2027-01-13 (remind me to measure the strip and
        ballast then). I cut one torsion strip (a spare is cut just in time) and seated the damper discs. The
        hacksaw blades are pinned (6 x 0.8 x 153.5 mm, a 1 x 5 mm pin near each end; teeth face whichever way it
        is laid); the redesigned handle's print waits for a print day, then a grip test, then the brass ballast
        (one 15 mm cut of the 10 mm rod in the printed saw guide). The enclosure is decided: printed PLA plates
        (1.2 mm plate flush with the outside face, 2 mm rim, no window; grey walls, red lid, black strips). The
        assembly gates are in docs/kb/build_dependency_graph.md (tell me when assembly can start). Campaign
        design (approved): calibration/control/claim runs, per-run-type gates, epochs for hardware states,
        provenance tables in hardware/balance/campaign/ (raw files ~/data/open-torsion-balance/raw, backup on
        D:); slowdemod.py and the logger's manifest check exist; the campaign writer waits on the first noise
        record. I am spend-shy: propose no purchases or carts; work with stock and printed parts. Git: my
        commits are under my identity; never put a Claude co-author trailer on any commit.
      - Printing: the K1-FA35 is on my balcony with the door shut and I work in the office: there is no camera
        and I cannot hear it, so give me clock-time visual checks, never audible ones (on the normal start the
        first layer is about 9-11 min after the upload, on the fast start 3-5 min). I will not print below 8 C
        outdoors and I watch the weather myself: I tell you when a print day starts (do not track or ask for
        temperatures). I plug it in, switch it on and feed the filament you advise (spools live in a large
        sealed freezer bag on a separate holder, not on the printer); you run heating, homing and starting only
        when I say so in that message. Slicing only on Sonnet or better. The agent drives OrcaSlicer (2.5.0
        flatpak, API on 13130) and the K1 through MCP and Moonraker (wsl workspace: connection notes,
        docs/print-session-runbook.md sections E-I, the K1 note). Printed so far: plate 1, the small plate, the
        gantry, all four posts with their bars, the strip guide, two calibration riders, the four wall strips,
        two lid strips, the first hacksaw handle (obsolete) and the grey wall plates nx_a, ny_a, px_a and px_b.
        Left: wall plates py_a (sliced) and py_b, nx_b, ny_b, four red lid tiles, the new hacksaw handle, and the
        base (failed three times at 4 C and a badly seated plate; parked until a fix: brim, smaller or a warmer
        day). A plate I lift off the printer needs a warm re-mesh before the next print.
      - Inventory: my bags are `ELECTRONICS` (inner labelled bags), `BALANCE MATERIALS`, `HAND TOOLS` and
        `BENCH + FASTENERS`, each with named sub-bags (filing plan in lab/docs/inventory.md; sorted). When
        something arrives, tell me the sub-bag, name parts by their STL/3MF object names (not shorthand) and
        quote photo items by file name plus mat coordinates. My tool photos are not a full tool list: ask me
        when a tool is not listed.
    Constraints: no hand soldering; fab boards use only JLC's machine-placed SMT parts; USB power, under
    50 V DC / 30 V AC; PLA only on my Creality K1; AliExpress for stock parts when I decide to buy (no
    single-item shipping fees), JLC PCB/PCBA/3DP/CNC when fabrication beats buying and cutting by hand; design to
    stock sizes. I'm in Canada and JLC prices on my account are in CAD on the cart and in USD on order pages. I
    will not pay a shipping premium for a tiny order, and I dislike courier customs fees.
    JLC quote, BOM/CPL, cart, message, coupon and order pages can be read and driven through my JLCONE desktop app
    when I launch it with --remote-debugging-port=9222 (recipe and gotchas in lab/docs/kb/jlc_account_and_quotes.md:
    only trust a dialog with a visible bounding box, click with Input.dispatchMouseEvent and check with a
    screenshot; an already open orders tab shows stale text until it is reloaded): text reads, paced clicks,
    uploads of this repo's own Gerber, BOM and CPL files (a draft's BOM/CPL page is not an order). Never call
    JLC's API, never touch the cookies, never accept terms for me, never submit or pay; Save to cart, Secure
    Checkout and claiming coupons only when I say so in that message: I approve and pay, and I place at most one
    order per day. Treat any JLC price not from my words, my captures or a page read through the app as an
    estimate. Never put parcel tracking numbers, long JLC order numbers, card digits, my name or address, or
    secrets in chat or files (they are redacted in the markdown files). Only say you did something if the
    transcript shows it (do not say notes are written before they are).
    docs/history.md is my chat transcript: never append to it (I paste the full summary myself), don't edit
    existing text, and don't use it as an analysis source unless I name lines to read. Pictures are lossless
    .jxl (keep them small, about 0.5-0.7 MB; the large tool-bag JPEGs are git-ignored); .jxl and .eprj2 are Git
    LFS (the .eprj2 is leftover from the dropped route; I decide whether to keep it). Photos and zips I send
    are for you: look at each, record what matters in the KB, then delete or convert them yourself, and never
    leave them lying in a repo or ask me what to do with them. When you slice, tell me which object is which
    and whether parts are meant to touch, and leave previewable STL files. Don't commit anything in these repos:
    I stage and commit everything after each chat, and you don't need to tell me nothing is committed.
    Workflow: docs/TODO-agent.md is the agent's own list and must be empty (0 lines) at the end of every chat:
    do startable items, move truly blocked ones to TODO-BLOCKED.md with the exact condition (TODO-backlog.md and
    TODO-completed.md sit beside it). My hands-on tasks live in docs/TODO-arcticoder.md as separately numbered
    tasks for me only (actions only, one-line justifications; internal notes go in docs/kb); any task or decision
    you give me in chat goes there too. Keep docs/kb/*.md (LLM-only notes) up to date with discoveries. Don't
    quote me or describe how I said things in files or chat. Watch for deals only; buy nothing unless I ask.
    Start by reading docs/kb/README.md and docs/kb/session_handoff.md in open-torsion-balance, then
    lab/docs/kb/README.md and lab/docs/kb/jlc_account_and_quotes.md. Then continue from
    docs/TODO-arcticoder.md, docs/TODO-BLOCKED.md and my feedback below.

    ## Read first

    Both `docs/kb/README.md` files, `lab/docs/kb/jlc_account_and_quotes.md` (last sections), `docs/kb/printing_state.md`, `docs/kb/build_dependency_graph.md`, `docs/campaign_loop.md`, `hardware/instrument/fab/ORDER.md`, `docs/TODO-arcticoder.md`, `docs/TODO-BLOCKED.md`, `~/Code/sysadmin/wsl/docs/kb/apps/k1-moonraker.md` and `~/Code/sysadmin/wsl/docs/print-session-runbook.md` for the printer side.
