# Session handoff — chat 18 final, 2026-11-23 (replace at each handoff; do not append)

## State
- **Printing (K1-FA35, 192.168.1.70), chat 18:** the base failed three times on 2026-11-21 (attempt 1 a badly seated plate: mesh column +0.7 to +1.5 mm; attempt 2 a glob at the start; attempt 3 lifted after 30 min at 4 C), so it is parked; the user's rule is NO printing below 8 C outdoors and he tells me when a print day starts (I do not track weather). On 2026-11-22 (8 C) two grey wall plates printed fine: `encl_print_wall_nx_a` (12:52-14:00, normal start) and `ny_a` (14:17-15:19, fast start after a warm re-mesh); both looked good. A CAD fault was fixed first: the 1.2 mm plate sat centred in the 2.0 mm rim (a 0.4 mm bridge when laid flat); it is now flush with the outside face (`enclosure_printed.py`), STLs regenerated; `balance.3mf` still has the old wall plates, slice from the STLs. Left to print: `px_a` (sliced as `balance_p13_wall_px_a_20261122.gcode`, 1 h 3 min), `py_a`, four `_b` walls (two per plate), four red lid tiles, the base (fix first: brim or smaller or warmer day), and the redesigned hacksaw handle (about 72 min). Details: `kb/printing_state.md`, `~/Code/sysadmin/wsl/docs/print-session-runbook.md` (A-H) and `kb/apps/k1-moonraker.md`.
- **Hacksaw blades are pinned** (user's measurements 2026-11-22: 6 x 0.8 x 153.5 mm, a 1 x 5 mm pin through the thickness 3 mm from each end, sawtooth); the first handle failed; `fixtures.hacksaw_handle` is redesigned (groove 6.3 x 0.9, two 1.4 mm pin holes), STLs regenerated, smoke checks pass; the brass cut waits on the printed handle, the grip test and the safety glasses.
- **Torsion strip:** one cut by the user (about 58 x 4.2 mm, a shallow lengthwise knife groove, bagged `TORSION STRIP` in `STRIP SHEET`); a spare is cut just in time (scissors after scoring are fine). Damper discs are seated against the 0.6 mm lips (tape cap optional). The 2026-11-10 LR44 cells are promised 2027-01-13 (calipers unusable until then; remind the user to measure the strip and ballast then).
- **Main board:** unchanged from chat 17 (ordered 2026-11-18, in production, est. ship about 2026-11-24; duty, tax and clearance are billed by UPS at delivery: ask for the amount). `clamp_plate` shipped; the glasses and the 1-20 g weight set are in transit. No purchases proposed.
- **Repo state:** uncommitted edits of this chat: `enclosure_printed.py`, `fixtures.py`, `smoke_test.py`, regenerated wall-plate and hacksaw-handle STLs, assembly.md, KB and TODO files; `lab/docs/inventory.md` and `orders.md`. `balance.py` deletes the `encl_print_*` STLs on export: regenerate enclosure STLs with `~/.venvs/lab-hw/bin/python hardware/balance/enclosure_printed.py` and export single fixtures with a one-off script. Never commit unless told; never a Claude co-author trailer.
- **Photos and zips from the user:** look at every one once, write findings to the KB, delete the zip and the loose files (a photo is kept only as a small `.jxl` in `docs/img/` when it documents the build); never ask what to do with them; no `inbox/` folders.
- **Previews:** when slicing, say which object is which and whether objects are meant to touch; compare the `EXCLUDE_OBJECT_DEFINE` polygons for overlaps (the two riders were printed joined); leave previewable STLs and name them. Do not announce "nothing is committed" at the end of replies.
- **Assembly steps startable now (user's list):** the brass cut after the new handle; most mechanics wait on the base (frame), `clamp_plate` and the walls (`kb/build_dependency_graph.md`).

- **Chat 19 (2026-11-23) additions:** the repo is RENAMED `open-torsion-balance` (GitHub rename done by `gh`; fresh clone `~/Code/python/open-torsion-balance`, added to `lab/lab.code-workspace`; the old directory is a duplicate the user deletes, task 4; work from the new clone; old name replaced in live text, history.md files untouched; scope text and README draft in `docs/scope_and_rename.md` await approval, tasks 2-3). Chat 19 later (2026-11-24): git identity set in this clone; two commits rewritten (old hashes gone); audit items fixed (`layout/fab_route.py` now holds DNP_FIRST_ARTICLES); claim 2 restated (non-air terms, 1/3-3 band, lid test; air term not predictable without a flow witness). Gate design revised after the user's review: three run purposes, per-run-type gates, rule D (drive-correlated witnesses excluded from gates and regression), freeze rule F, epochs = hardware states, calibrated forces poolable across epochs; `docs/campaign_loop.md` (design only, nothing implemented until the user answers task 2), `material_study.py --terms` (upgrade ranking), `eddy_vane_sim.py` (sketch), three new smoke checks. The sketch suggests zeta for one plain pad is nearer 0.22 than 0.40: measure in A5 step 4 before changing params. Teeth direction of the hacksaw blade is a free choice, not an unknown. Not yet reflected in the pasted context block below (scope line, new docs).

## Files that carry the state

`docs/TODO-arcticoder.md` (user tasks: the brass cut, plus the en-route list), `docs/TODO-agent.md` (0 lines), `docs/TODO-BLOCKED.md` (print remainder, handle print, base fix, caliper reminder, firmware/analysis items), `docs/TODO-backlog.md`, `docs/TODO-completed.md` (newest first).

## Standing rules (see `kb/project_workflow_notes.md`)

TODO-agent.md must be 0 lines at the end of every chat (do startable work; truly blocked items go to TODO-BLOCKED.md with the condition). Never commit; propose no purchases; never add a Claude co-author in lab/sfb commits. No quotes of the user, no tone descriptions. No tracking numbers, long order numbers, card digits, names or addresses in files or chat; never print secrets. Never state a JLC price that is not from the user, a capture or a page read through the app. Say only what the transcript shows. One order per day is the user's own limit (the agent cannot enforce it, only read order dates in the JLC list). No hand-built electronics; never EasyEDA/Spark. JLC: the BOM/CPL page of a draft is not an order (the agent may read it and upload there); Save to cart, Secure Checkout and claiming coupons are done only when the user says so in that message (done for the main-board order and the Black Friday coupons); never submit, pay or accept terms. Coupons: one per order; read the payment page, not the cart, before judging them. No printing below 8 C outdoors (the user decides print days); heat and print only on the user's explicit request in that message ("go", "begin the load sequence", "start the print" count). Clock-time visual checks only (no camera, door shut, user cannot hear it). Slicing and print prep only on Sonnet or better. Monitor notices that arrive as system events are not the user's messages. Spools live in a sealed freezer bag on a roller (no humidity advice). Park the head at about X200 Y110 for loading. The earlier rule about not asking obvious questions in print windows was removed by the user: ask when something is unclear.

## Context block for the next chat (paste this)

    I'm building a small experimental-physics lab across two repos, both open in this workspace.
      - lab (github.com/arcticoder/lab): reusable bench instruments — Raspberry Pi Pico/RP2040 circuits with
        SPICE netlists, breadboard guides and pass/fail smoke tests — plus the shared parts inventory and
        order ledger (docs/inventory.md, docs/orders.md), my filament stock and tools (docs/inventory.md,
        "Filament" and "Tools", including a Dremel 3000), the storage-bag filing plan (docs/inventory.md,
        "Filing plan"; photos in docs/img/tools_bags_2026-11-20/) and my JLC account notes (docs/jlc/:
        coupons read from my account, captures and reads of JLC's quote pages,
        docs/kb/jlc_account_and_quotes.md).
      - open-torsion-balance (github.com/arcticoder/open-torsion-balance): the first experiment — an open,
        low-cost torsion balance that quantifies the spurious forces (supply-lead Lorentz forces, heating,
        convection) that dominate small-thrust measurements. Printable mechanics (CadQuery), FR4 fab boards for
        the arm and electrodes, a force-noise model, and JLCPCB-assembled RP2040 electronics (KiCad 9, SKiDL,
        ngspice, MicroPython firmware tested on the host). KiCad/SKiDL is the design source: I dropped the
        EasyEDA/Spark route on 2026-11-01 (shelved; never offer EasyEDA, Spark, its MCP or the validator again).
        No more hand-built electronics: the instrument is fab-assembled boards.
        State (2026-11-23, end of chat 18): the main board (WP5, 120 x 90 mm, one board, 4 layers) is ORDERED and
        in production at JLC (placed 2026-11-18: 5 PCBs + 2 Economic PCBA boards with the LIS2DW12 (U7) left off
        the BOM and CPL; total US$150.32 including UPS shipping US$30.97; UPS bills duty, tax and clearance fees
        at delivery, which are not in that total: ask me for the amount when it lands; estimated ship about
        2026-11-24). JLC takes ONE coupon per order; unused flash coupons run to 2026-12-03
        (lab/docs/jlc/coupons.md). The arm, elec_board and clamp_ground have arrived; clamp_plate is shipped.
        Next for the electronics: arrival, then docs/bringup.md (skip the LIS2DW12 check). The device card (16 x
        24 mm FR4 with a 10 ohm resistor, only for the lead-current runs) has no design and is not in the main
        order; a spare elec_board stands in as dummy mass (TODO-backlog). The 2026-11-10 AliExpress parcel
        arrived 2026-11-20 except the LR44 cells (promised 2027-01-13; the calipers have no cell yet: remind me
        to measure the strip and ballast when they arrive); the 1 g weight is not magnetic; the safety glasses
        and the 1-20 g nickel-plated-steel weight set (2026-11-14 order) are still in transit (keep the set away
        from the damper magnets). I cut one torsion strip (a spare is cut just in time, scissors after scoring
        are fine) and seated the damper discs. The 2026-11-10 hacksaw blades are PINNED (6 x 0.8 x 153.5 mm, a
        1 x 5 mm pin through each end): the first handle failed and a new one is designed (its print waits in
        TODO-BLOCKED); the brass ballast is still one 15 mm cut of the 10 mm rod in the printed saw guide, after
        the new handle, the glasses and a grip test. The enclosure is decided: printed PLA plates (1.2 mm plate
        flush with the outside face, 2 mm rim, no window; grey walls, red lid, black strips). The assembly gates
        are in docs/kb/build_dependency_graph.md (tell me when assembly can start). I am spend-shy after the UPS
        order: propose no purchases or carts; work with stock and printed parts. My last commit's author was
        reset locally to my identity (the original is on origin, so I must force-push with
        --force-with-lease); never put a Claude co-author trailer on any commit.
      - Printing: the K1-FA35 is on my balcony with the door shut and I work in the office: there is no camera and
        I cannot hear it, so give me clock-time visual checks, never audible ones. I will not print below 8 C
        outdoors and I watch the weather myself: I tell you when a print day starts (do not track or ask for
        temperatures). I plug it in, switch it on and feed the filament you advise (spools live in a large
        sealed freezer bag on a separate holder, not on the printer); you run heating, homing and starting only
        when I say so in that message. Slicing only on Sonnet or better. The agent drives OrcaSlicer (2.5.0
        flatpak, API on 13130) and the K1 through MCP and Moonraker (wsl workspace: connection notes,
        docs/print-session-runbook.md sections E-H, the K1 note). Printed so far: plate 1, the small plate, the
        gantry, all four posts with their bars, the strip guide, two calibration riders, the four wall strips,
        two lid strips, the first hacksaw handle (obsolete) and the grey wall plates nx_a and ny_a. Left: the base
        (failed three times at 4 C and a badly seated plate; parked until a fix: brim, smaller or a warmer day),
        wall plates px_a (sliced), py_a and the four _b walls, four red lid tiles, and the new hacksaw handle. A
        plate I lift off the printer needs a warm re-mesh before the next print.
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
    screenshot): text reads, paced clicks, uploads of this repo's own Gerber, BOM and CPL files (a draft's BOM/CPL
    page is not an order). Never call JLC's API, never touch the cookies, never accept terms for me, never submit
    or pay; Save to cart, Secure Checkout and claiming coupons only when I say so in that message: I approve and
    pay, and I place at most one order per day. Treat any JLC price not from my words, my captures or a page read
    through the app as an estimate. Never put parcel tracking numbers, long JLC order numbers, card digits, my
    name or address, or secrets in chat or files (they are redacted in the markdown files). Only say you did
    something if the transcript shows it.
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

    Both `docs/kb/README.md` files, `lab/docs/kb/jlc_account_and_quotes.md` (last sections), `docs/kb/printing_state.md`, `docs/kb/build_dependency_graph.md`, `hardware/instrument/fab/ORDER.md`, `docs/TODO-arcticoder.md`, `docs/TODO-BLOCKED.md`, `~/Code/sysadmin/wsl/docs/kb/apps/k1-moonraker.md` and `~/Code/sysadmin/wsl/docs/print-session-runbook.md` for the printer side.

