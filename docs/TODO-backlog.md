# TODO — agent, backlog

> Open items are in `docs/TODO-agent.md`; blocked ones in `docs/TODO-BLOCKED.md`.

- [ ] WP4e — human-readable schematic sheets (a PDF for review and the paper). SKiDL's `generate_schematic` is not dependable here: flat, the 169-part main board does not finish (over 15
      CPU-minutes) and the head boards route only some of the time (`retries=6`); its drawn wiring also produces false KiCad ERC errors (the netlist is right). Options: `@subcircuit`
      hierarchical sheets, or placing symbols with kiutils from the netlist. The electrical checks do not depend on it (`schematic_test.py` runs on the netlist).
- [ ] Analysis of the experiment's results (after WP9 fixes the procedures): calibration of the plate force against weights or wire riders, lead-current and heating coupling coefficients with uncertainties, built on `host/analyze.py` (ASD, Allan deviation).
- [ ] Decisions to put to the user when reached (one line each in `TODO-arcticoder.md`): the G3 go/no-go after A5; a budget ceiling for the order.
- [ ] Purchases are on hold (user, 2026-11-20: spend-shy until the build shows progress; JLC shipping scales about linearly so bundling does not help). Work with owned stock and printed parts; no staged cart. Revisit when the balance is trimmed or a part is missing.
- [ ] Standing duties (not tasks): watch for JLC and AliExpress deals and log coupons with expiry in `lab/docs/jlc/coupons.md`; when the user reports an arrival, inventory it with a bag in `lab/docs/inventory.md`.
- [ ] Device card board (16 x 24 mm FR4 with a 10 ohm 1 W resistor, JLC-assembled; no design exists): needed only for the lead-current runs (`procedures.md` C.3); until then a dummy mass of about 2 g stands in (a spare `elec_board`). Revisit when those runs are next in the plan and spending resumes.
