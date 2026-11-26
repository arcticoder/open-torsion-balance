"""
slowdemod.py — slow demodulation of a logged force record at the modulation frequency (design: docs/campaign_loop.md section 4).

    from slowdemod import demodulate
    r = demodulate(t, force_N, ref01, f_mod, witnesses={"T_wall": ..., "B_x": ...}, driven=("B_x",))

The reference `ref01` is the DUT_EN (or heater) square wave read back from the logger (0/1 per sample), so a dropped sample cannot rotate the phase.
One least-squares fit over whole modulation cycles: force = A * ref + Q * ref_quarter_cycle_later + constant + linear + quadratic + sum_k w_k * witness_k,
the witnesses high-passed (a running mean of 3 / f_mod seconds removed: cut-off f_mod / 3, so the signal at f_mod is untouched).
Rule D: a witness named in `driven`, or whose own response to the reference exceeds `z_drop` times its noise, is dropped from the fit and reported.
Uncertainty = the largest of (fit covariance, per-cycle scatter, block bootstrap over cycles); a run whose three estimates differ by over 1.5x is flagged.
A is the force step between reference off and on (the quantity of interest); Q is the quadrature part (a thermal lag shows up here).
"""

import numpy as np


def _highpass(x, fs, f_mod):
    n = max(3, int(round(3.0 * fs / f_mod)))
    k = np.ones(n) / n
    pad = np.pad(x, (n // 2, n - 1 - n // 2), mode="edge")
    return x - np.convolve(pad, k, mode="valid")


def _whole_cycles(t, ref, f_mod, fs, skip_first=True):
    """Index range covering whole cycles starting at the first rising edge of the reference."""
    edges = np.flatnonzero((ref[1:] > 0.5) & (ref[:-1] <= 0.5)) + 1
    if len(edges) < 3:
        raise ValueError("fewer than 2 whole modulation cycles in the record")
    first = edges[1] if skip_first and len(edges) > 3 else edges[0]
    ncyc = int((t[-1] - t[first]) * f_mod)
    last = min(len(t), first + int(round(ncyc * fs / f_mod)))
    return first, last, edges[(edges >= first) & (edges < last)]


def _fit(y, X):
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ coef
    dof = max(1, len(y) - X.shape[1])
    cov = np.linalg.inv(X.T @ X) * (res @ res / dof)
    return coef, np.sqrt(np.diag(cov)), res


def demodulate(t, force, ref, f_mod, witnesses=None, driven=(), z_drop=3.0, n_boot=200, seed=0, skip_first=True):
    """Returns a dict: A, sigma_A (the largest estimate) and its three parts, Q, dropped witnesses with their z, the noise before and after the witness fit."""
    t = np.asarray(t, float)
    force = np.asarray(force, float)
    ref = (np.asarray(ref, float) > 0.5).astype(float)
    fs = (len(t) - 1) / (t[-1] - t[0])
    i0, i1, edges = _whole_cycles(t, ref, f_mod, fs, skip_first)
    tt = t[i0:i1] - t[i0]
    y = force[i0:i1]
    r = ref[i0:i1]
    q = np.roll(ref, int(round(fs / f_mod / 4)))[i0:i1]
    base = np.column_stack([r, q, np.ones_like(tt), tt / tt[-1], (tt / tt[-1]) ** 2])
    kept, dropped = {}, {}
    for name, w in (witnesses or {}).items():
        wh = _highpass(np.asarray(w, float), fs, f_mod)[i0:i1]
        if name in driven:
            dropped[name] = float("inf")
            continue
        c, se, _ = _fit(wh, base[:, :5])
        z = float(np.hypot(c[0] / se[0], c[1] / se[1]))
        if z > z_drop:
            dropped[name] = z
        else:
            kept[name] = wh
    X0 = base
    X = np.column_stack([base] + list(kept.values())) if kept else base
    c0, se0, res0 = _fit(y, X0)
    c, se, res = _fit(y, X)
    # per-cycle estimate: mean(on) - mean(off) of the residual-from-drift record, scatter over cycles
    drift = X[:, 2:5] @ c[2:5]
    wit = X[:, 5:] @ c[5:] if kept else 0.0
    yc = y - drift - wit
    per = []
    cyc = np.append(edges - i0, len(y))
    for a, b in zip(cyc[:-1], cyc[1:]):
        seg, rs = yc[a:b], r[a:b]
        if rs.min() == rs.max():
            continue
        per.append(seg[rs > 0.5].mean() - seg[rs < 0.5].mean())
    per = np.array(per)
    s_fit = float(se[0])
    s_cyc = float(per.std(ddof=1) / np.sqrt(len(per))) if len(per) > 2 else float("nan")
    rng = np.random.default_rng(seed)
    boots = [per[rng.integers(0, len(per), len(per))].mean() for _ in range(n_boot)] if len(per) > 2 else [np.nan]
    s_boot = float(np.std(boots, ddof=1))
    parts = [s for s in (s_fit, s_cyc, s_boot) if np.isfinite(s)]
    return {"A": float(c[0]), "Q": float(c[1]), "sigma": max(parts), "sigma_fit": s_fit, "sigma_cycles": s_cyc, "sigma_boot": s_boot,
            "flag_disagree": max(parts) / min(parts) > 1.5, "dropped_witnesses": dropped, "kept_witnesses": list(kept),
            "resid_rms_before": float(res0.std()), "resid_rms_after": float(res.std()), "n_cycles": len(per), "A_without_witness_fit": float(c0[0])}
