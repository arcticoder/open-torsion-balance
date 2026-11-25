"""
material_study.py — the arm's material and thickness compared (Part J1): mass, moment of inertia, first bending mode, thermal drift, electrodes.

    python3 hardware/balance/material_study.py

The arm hangs on edge (faces toward +-y): the pendulum swings in the thin direction, so the arm bends in the direction where its stiffness is E h t^3 / 12. It is clamped at the
centre, so each half is a cantilever of length L = ARM_HALF_LENGTH; the first mode comes from Rayleigh's quotient with the static tip-load shape phi(x) = (3 L x^2 - x^3) / (2 L^3),
which is exact for a point load and within a few percent for the lumped masses used here:  k = 3 E I / L^3,  m_eff = integral(mu phi^2) + sum(M_i phi(x_i)^2),  f = sqrt(k / m_eff) / 2 pi.
The masses carried on each half are the CAD's (balance.py output of 2026-10-26: device card and its hardware, vane and holder on the +x half; the ballast on the -x half): estimates of
where they sit, not a CAD modal analysis. Material properties are handbook values, not measured: FR4 E 20 GPa (JLC's TG135 laminate, in-plane, glass-cloth direction), 6061 aluminium 69 GPa,
PLA 3.5 GPa (FDM, along the layers). Creep and moisture are listed, not modelled.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402

# name: (E GPa, density g/cm^3, thickness mm, CTE ppm/K, carries electrodes?, note)
CANDIDATES = {
    "FR4 1.2 mm (chosen)": (20.0, 1.85, 1.2, 14.0, True, "ENIG pads and guard on the board itself; flat to about 0.1 mm; low creep"),
    "FR4 1.6 mm": (20.0, 1.85, 1.6, 14.0, True, "JLC's default thickness: +33% mass, about +40% first-mode frequency"),
    "FR4 1.0 mm": (20.0, 1.85, 1.0, 14.0, True, "JLC offers 1.0 mm; 0.1 mm tolerance band is +-10% at 1.0 mm and over"),
    "FR4 0.8 mm": (20.0, 1.85, 0.8, 14.0, True, ""),
    "FR4 0.4 mm": (20.0, 1.85, 0.4, 14.0, True, "mass falls to a third; the first mode falls into the building-vibration band"),
    "Al 6061 sheet 0.8 mm": (69.0, 2.70, 0.8, 23.0, False, "conductive: the arm is the grounded electrode; no pads or guard; CNC or laser cut, one piece"),
    "Al 6061 sheet 1.0 mm": (69.0, 2.70, 1.0, 23.0, False, ""),
    "PLA printed 2.0 mm": (3.5, 1.24, 2.0, 68.0, False, "creeps under steady load, absorbs moisture, warps over 208 mm; electrodes would be foil"),
    "PLA printed 3.0 mm": (3.5, 1.24, 3.0, 68.0, False, ""),
}

HOLE_FILL = 26.48 / (208 * 60 * 1.2 * 1.85e-3)  # the CAD arm's mass against the solid bounding board (holes and the finger's shape)
# lumped masses on each half: (position along the half in m, mass in kg): CAD masses, positions estimated
PLUS_X = [(0.095, 6.41e-3), (P.VANE_X, 5.30e-3)]  # device card with its hardware; vane, its holder and hardware
MINUS_X = [(0.090, 10.07e-3)]  # the brass ballast


def phi(x, L):
    return (3 * L * x * x - x ** 3) / (2 * L ** 3)


def study(name):
    E, rho, t, cte, electrodes, note = CANDIDATES[name]
    L = P.ARM_HALF_LENGTH
    h = P.ARM_HEIGHT
    t_m = t * 1e-3
    mu = rho * 1e3 * h * t_m * HOLE_FILL  # kg per metre of one half
    EI = E * 1e9 * h * t_m ** 3 / 12
    k = 3 * EI / L ** 3
    out = {}
    for side, masses in (("+x", PLUS_X), ("-x", MINUS_X)):
        m_eff = mu * L * 0.2357 + sum(m * phi(x, L) ** 2 for x, m in masses)  # integral of mu phi^2 dx = 33/140 mu L
        out[side] = math.sqrt(k / m_eff) / (2 * math.pi)
    arm_mass_g = mu * 2 * L * 1e3 + 0.0
    inertia = mu * 2 * L * (2 * L) ** 2 / 12  # uniform strip about its centre
    return {"E_GPa": E, "t_mm": t, "arm_g": arm_mass_g, "arm_I": inertia, "f1_plus_Hz": out["+x"], "f1_minus_Hz": out["-x"], "f1_Hz": min(out.values()),
            "drift_um_per_K": cte * 1e-6 * L * 1e6, "electrodes": electrodes, "note": note}


def main():
    print("%-24s %7s %9s %8s %8s %8s %9s  %s" % ("candidate", "arm g", "I x1e-5", "f1 +x", "f1 -x", "drift", "electrodes", "note"))
    for name in CANDIDATES:
        s = study(name)
        print("%-24s %7.1f %9.2f %7.0fHz %7.0fHz %5.1f um/K %9s  %s" % (name, s["arm_g"], s["arm_I"] * 1e5, s["f1_plus_Hz"], s["f1_minus_Hz"], s["drift_um_per_K"], "board" if s["electrodes"] else "extra", s["note"]))
    print("CAD arm (FR4 1.2 mm, with its holes): 26.5 g, 8.84e-5 kg m^2 about z; the uniform-strip inertia above is the bare board without the finger and holes")


if __name__ == "__main__" and "--terms" not in sys.argv:
    main()


# ---------------------------------------------------------------------------------------------------------------------------------------
# Part J2 — which force-noise term limits at each upgrade stage, and what a material/geometry change buys (added 2026-11-23)
#
#     python3 hardware/balance/material_study.py --terms
#
# The arm study above never touched the force-noise budget. This part does: it recomputes `model.force_terms()` with a swapped frame-path material
# (the clamp-to-sensor path, params.FRAME_PATH, now PLA), a swapped arm material and a scaled flag area, in two environments (air; vacuum, where the air term is
# zero by assumption: residual-gas damping and radiometer forces are NOT modelled, so a vacuum row is a lower bound until they are). CTEs are handbook values
# [assume], so the ranking is only as good as they are; the first measured transfer coefficient (a heater step, nN per K) replaces them (docs/campaign_loop.md).
# Terms scale with the environment assumptions in params.py (TEMP_NOISE, AIR_SPEED_FLUCT ...), which A5 measures: the ranking is conditional on them.
# ---------------------------------------------------------------------------------------------------------------------------------------

import model as M  # noqa: E402

# name: (CTE ppm/K, note) — the frame path is the length between the strip's top clamp and the sensor bracket that carries the flag-to-sensor distance
FRAME_MATERIALS = {
    "PLA (now)": (70.0, "printed; creeps; handbook 68-70"),
    "FR4 rod/board": (14.0, "in-plane glass-cloth direction; JLC 3DP not needed, boards cut by routing"),
    "304 steel rod": (17.3, "stock rod; magnetic-permeability low for 304 but not zero: keep clear of the arm's field sensor"),
    "6061 aluminium": (23.0, "CNC or stock bar; the expensive option the user wanted to avoid"),
    "carbon-fibre rod": (1.0, "axial CTE about -1..+1 ppm/K for pultruded rod [assume]; conductive, adhesive-bonded"),
    "Invar 36": (1.3, "reference only: no stock source in the repo, not a candidate for buying"),
}
SHORT = {"air currents": "air", "temperature (printed frame to the sensor)": "frame-path temp", "temperature (arm expansion)": "arm temp",
         "floor acceleration through centre-of-mass offset": "floor accel", "floor tilt through centre-of-mass offset": "floor tilt",
         "thermal (Brownian, eddy damper)": "Brownian", "magnetic (stray moment x field noise)": "magnetic", "readout (shot + electronics + LED)": "readout"}
ARM_MATERIALS = {"FR4 (chosen)": 14.0, "6061 aluminium": 23.0, "PLA": 68.0}


def terms_for(frame_cte_ppm=None, arm_cte_ppm=None, flag_area_scale=1.0, vacuum=False, frame_path=None):
    """force_terms() with a changed frame material, arm material, flag area, and air or vacuum. Restores params afterwards."""
    keep = (P.PLA_EXPANSION, P.ARM_EXPANSION, P.AIR_AREA, P.FRAME_PATH)
    try:
        if frame_cte_ppm is not None:
            P.PLA_EXPANSION = frame_cte_ppm * 1e-6
        if arm_cte_ppm is not None:
            P.ARM_EXPANSION = arm_cte_ppm * 1e-6
        if frame_path is not None:
            P.FRAME_PATH = frame_path
        P.AIR_AREA = keep[2] * flag_area_scale
        t = M.force_terms()
        if vacuum:
            t["air currents"] = 0.0
        return t
    finally:
        P.PLA_EXPANSION, P.ARM_EXPANSION, P.AIR_AREA, P.FRAME_PATH = keep


def ranking(terms):
    """Terms sorted largest first as (name, nN/rtHz, share of the quadrature total)."""
    tot = M.total_density(terms)
    return [(n, v * 1e9, (v / tot) ** 2) for n, v in sorted(terms.items(), key=lambda a: -a[1])], tot


def transfer_coefficients():
    """Force per unit input of each environmental channel (the numbers the injected-signal tests measure). nN per K for the two thermal paths; the rest as given by the model."""
    k = M.k_eff(M.strip_stiffness(), P.ARM_HALF_LENGTH)
    return {
        "frame path (nN/K), PLA now": k * P.PLA_EXPANSION * P.FRAME_PATH * 1e9,
        "arm (nN/K)": k * P.ARM_EXPANSION * P.ARM_HALF_LENGTH * 1e9,
        "tilt (nN/urad)": P.MOVING_MASS * P.G_ACC * P.COM_OFFSET / P.ARM_HALF_LENGTH * 1e-6 * 1e9,
        "floor acceleration (nN per mm/s^2)": P.MOVING_MASS * P.COM_OFFSET / P.ARM_HALF_LENGTH * 1e-3 * 1e9,
        "magnetic (nN/uT)": P.STRAY_MOMENT / P.ARM_HALF_LENGTH * 1e-6 * 1e9,
    }


def upgrade_stages():
    """(label, terms) for the order of upgrades: baseline in air, cheaper air-term steps, a material swap, then vacuum with and without it."""
    st = [("0 baseline, air, PLA frame, 20 cm2 flag", terms_for())]
    st.append(("1a air: air-exposed area x0.5 (the model is linear in AIR_AREA = flag + device mount; unverified)", terms_for(flag_area_scale=0.5)))
    st.append(("1b air: air-speed fluctuation 0.5x via enclosure/gasket (an assumption, not a design)", None))
    st.append(("2 frame path to FR4 (CTE 14), air", terms_for(frame_cte_ppm=14.0)))
    st.append(("3 vacuum, PLA frame", terms_for(vacuum=True)))
    st.append(("4 vacuum + frame path to FR4", terms_for(frame_cte_ppm=14.0, vacuum=True)))
    st.append(("5 vacuum + carbon-rod frame path", terms_for(frame_cte_ppm=1.0, vacuum=True)))
    return st


def main_terms():
    print("Force-noise terms at %.3f Hz, one 1000 s measurement resolution = density x sqrt(1/(2 T)) (model.py, params.py assumptions)\n" % P.F_MOD)
    for label, t in upgrade_stages():
        if t is None:  # 1b: halve the air-speed fluctuation
            keep = P.AIR_SPEED_FLUCT
            try:
                P.AIR_SPEED_FLUCT = keep * 0.5
                t = terms_for()
            finally:
                P.AIR_SPEED_FLUCT = keep
        rk, tot = ranking(t)
        print("%s\n  total %.3f nN/rtHz -> %.3f nN in 1000 s; limiting term: %s (%.0f%% of the quadrature sum)" % (label, tot * 1e9, M.resolution(tot) * 1e9, SHORT.get(rk[0][0], rk[0][0]), 100 * rk[0][2]))
        print("  " + "; ".join("%s %.3f" % (SHORT.get(n, n), v) for n, v, _ in rk[:4]))
    print("\nFrame-path material swap (air and vacuum), arm material in FR4, frame path %.0f mm:" % (P.FRAME_PATH * 1e3))
    print("  %-18s %6s  %12s %10s  %12s %10s  %s" % ("material", "ppm/K", "air nN/rtHz", "1000 s nN", "vac nN/rtHz", "1000 s nN", "limiting in vacuum"))
    for name, (cte, note) in FRAME_MATERIALS.items():
        ta, tv = terms_for(frame_cte_ppm=cte), terms_for(frame_cte_ppm=cte, vacuum=True)
        da, dv = M.total_density(ta), M.total_density(tv)
        print("  %-18s %6.1f  %12.3f %10.3f  %12.3f %10.3f  %s" % (name, cte, da * 1e9, M.resolution(da) * 1e9, dv * 1e9, M.resolution(dv) * 1e9, SHORT.get(ranking(tv)[0][0][0], "")))
    print("\nArm material alone (frame stays PLA): only the arm-expansion term moves")
    for name, cte in ARM_MATERIALS.items():
        t = terms_for(arm_cte_ppm=cte)
        print("  %-18s arm-expansion term %.3f nN/rtHz, total in air %.3f" % (name, t["temperature (arm expansion)"] * 1e9, M.total_density(t) * 1e9))
    print("\nFlag area scaling of the air term (linear in AIR_AREA in model.force_terms: 1.2 x 1.0 x area x v_rms x v_fluct):")
    for s in (0.25, 0.5, 1.0, 2.0):
        print("  flag area x%.2f -> air %.3f nN/rtHz" % (s, terms_for(flag_area_scale=s)["air currents"] * 1e9))
    print("\nTransfer coefficients (what the injected-signal tests measure; predicted noise = coefficient x measured environment noise):")
    for n, v in transfer_coefficients().items():
        print("  %-38s %.4g" % (n, v))


if __name__ == "__main__" and "--terms" in sys.argv:
    main_terms()
