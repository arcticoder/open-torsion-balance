"""
eddy_vane_sim.py — SKETCH: eddy-current damping of a slit copper vane, from the repo's magpylib disc model and a resistor-network sheet-current solver (4.1, 2026-11-23).

    ~/.venvs/lab-hw/bin/python hardware/balance/eddy_vane_sim.py

Model [assume]: low magnetic Reynolds number (the field of the induced currents is ignored), a thin sheet (thickness t, conductivity sigma, uniform through the
thickness), the vane moving in y (the swing direction) at speed v through the discs' Bz(x, y). The motional EMF field is E = v x B = v Bz x_hat. The sheet carries
J = sigma (E - grad phi) with div J = 0 and no current through the vane's edge or a slit; phi is solved on a square grid of cells (nodal analysis, every pair of
touching cells joined by a conductance sigma t; a cell not in the mask has none). Dissipated power P = integral J^2 t / sigma dA = c v^2, so c = P / v^2.
The existing `model.eddy_damping_field` is the no-return-path limit (c = sigma t integral Bz^2 dA), an upper bound: this solver gives how much of it survives the
vane's edges, and ranks slit patterns RELATIVE to the plain pad (the absolute number is good to a factor of about two at best; the ratios are the useful output).
Not yet done: eddy-current back-action, the finite thickness, the discs moving with the arm's rotation (the vane's speed varies across it by +-x/VANE_X), validation
against a measured decay (A5 step 4 with a cut pad), and JLC copper (35 um layers: a plain layer is 0.035/0.3 = 0.12 of the 0.3 mm pad; N layers need N sheets in contact or in parallel).
"""

import os
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import params as P  # noqa: E402

SIGMA_CU = 5.8e7  # S/m


def bz_grid(half=14e-3, h=0.25e-3):
    """Bz (T) at cell centres of a square grid with cell size h covering [-half, half]^2 in the vane plane. Returns (xs, ys, Bz[ny, nx])."""
    gap = P.MAGNET_GAP + (P.MAGNET_LIP if P.MAGNET_MAGNETIZATION == "axial" else 0.0)
    coll = M._damper_discs(gap, P.MAGNET_MAGNETIZATION)
    n = int(round(2 * half / h))
    xs = -half + h * (np.arange(n) + 0.5)
    X, Y = np.meshgrid(xs, xs)
    pts = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1)
    return xs, xs, coll.getB(pts)[:, 2].reshape(n, n)


def mask_pad(xs, ys, size=P.VANE_SIZE, slits=()):
    """Boolean mask [ny, nx] of copper cells: a size[0] x size[1] pad (x along the arm, y along the swing) centred on the origin, minus slit rectangles
    (xmin, xmax, ymin, ymax) in metres."""
    X, Y = np.meshgrid(xs, ys)
    m = (np.abs(X) <= size[0] / 2) & (np.abs(Y) <= size[1] / 2)
    for x0, x1, y0, y1 in slits:
        m &= ~((X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1))
    return m


def damping(mask, bz, h, t, v=1.0, sigma=SIGMA_CU):
    """Damping coefficient c (N s/m) of the masked sheet moving in y at speed v, and the no-return-path value for the same mask."""
    ny, nx = mask.shape
    idx = -np.ones(mask.shape, dtype=int)
    idx[mask] = np.arange(mask.sum())
    n = int(mask.sum())
    g = sigma * t  # sheet conductance: a square cell's conductance is sigma*t regardless of h
    rows, cols, vals = [], [], []
    b = np.zeros(n)
    # EMF along x between horizontally adjacent cells: E_x = v Bz (average of the two cells); no EMF along y (E has only an x component)
    for dy, dx in ((0, 1), (1, 0)):
        a = mask[: ny - dy, : nx - dx] & mask[dy:, dx:]
        i0 = idx[: ny - dy, : nx - dx][a]
        i1 = idx[dy:, dx:][a]
        if dx:
            emf = v * 0.5 * (bz[: ny - dy, : nx - dx][a] + bz[dy:, dx:][a]) * h  # volts around the link i0 -> i1
        else:
            emf = np.zeros(a.sum())
        # link current i0 -> i1 = g (emf - (phi1 - phi0)); node equations: sum of currents leaving = 0
        for p, q, s in ((i0, i1, 1.0), (i1, i0, -1.0)):
            rows += [p, p]
            cols += [p, q]
            vals += [np.full(p.size, g), np.full(p.size, -g)]
            b += np.bincount(p, weights=-g * s * emf, minlength=n)
    L = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsc()
    L = L + coo_matrix(([1e-12 * g], ([0], [0])), shape=(n, n)).tocsc()  # pin the potential's free constant
    phi = spsolve(L, b)
    power = 0.0
    for dy, dx in ((0, 1), (1, 0)):
        a = mask[: ny - dy, : nx - dx] & mask[dy:, dx:]
        i0 = idx[: ny - dy, : nx - dx][a]
        i1 = idx[dy:, dx:][a]
        emf = v * 0.5 * (bz[: ny - dy, : nx - dx][a] + bz[dy:, dx:][a]) * h if dx else np.zeros(a.sum())
        cur = g * (emf - (phi[i1] - phi[i0]))
        power += float((cur**2 / g).sum())
    free = sigma * t * float((bz[mask] ** 2).sum()) * h * h  # the field-integral estimate model.eddy_damping_field uses (v = 1)
    return power / v**2, free


def patterns():
    s = 0.5e-3  # slit width, m
    a = P.VANE_SIZE[0] / 2
    b = P.VANE_SIZE[1] / 2
    out = {"plain pad": ()}
    out["1 slit along y, from one edge, to 2 mm of the far edge"] = ((-s / 2, s / 2, -b, b - 2e-3),)
    out["1 slit along x (across the swing), from one edge to 2 mm of the far edge"] = ((-a, a - 2e-3, -s / 2, s / 2),)
    out["comb: 4 slits along y from alternate edges"] = tuple(((x - s / 2, x + s / 2, -b, b - 2e-3) if i % 2 == 0 else (x - s / 2, x + s / 2, -b + 2e-3, b)) for i, x in enumerate((-6e-3, -2e-3, 2e-3, 6e-3)))
    out["comb: 4 slits along x from alternate edges"] = tuple(((-a, a - 2e-3, y - s / 2, y + s / 2) if i % 2 == 0 else (-a + 2e-3, a, y - s / 2, y + s / 2)) for i, y in enumerate((-6e-3, -2e-3, 2e-3, 6e-3)))
    out["grid of 1 mm holes at 3 mm pitch (perforated)"] = tuple((x - 0.5e-3, x + 0.5e-3, y - 0.5e-3, y + 0.5e-3) for x in np.arange(-7.5e-3, 8e-3, 3e-3) for y in np.arange(-7.5e-3, 8e-3, 3e-3))
    return out


def main():
    h = 0.25e-3
    xs, ys, bz = bz_grid(h=h)
    t = P.VANE_THICKNESS
    print("Damper field: peak |Bz| %.0f mT on the vane plane; vane %.0f x %.0f mm, t %.2f mm, sigma %.1e S/m, grid %.2f mm" % (np.abs(bz).max() * 1e3, P.VANE_SIZE[0] * 1e3, P.VANE_SIZE[1] * 1e3, t * 1e3, SIGMA_CU, h * 1e3))
    c_ref = None
    print("%-78s %10s %10s %8s" % ("pattern", "c (N s/m)", "vs plain", "of free"))
    for name, slits in patterns().items():
        m = mask_pad(xs, ys, slits=slits)
        c, free = damping(m, bz, h, t)
        c_ref = c if c_ref is None else c_ref
        print("%-78s %10.3e %9.2fx %7.0f%%" % (name, c, c / c_ref, 100 * c / free))
    print("model.eddy_damping_field (no return path, 28 mm window): c = %.3e N s/m" % M.eddy_damping_field()[0])
    print("Thickness: damping is linear in t at this level, so one 35 um layer is %.2fx the 0.3 mm pad; a JLC board with several copper layers adds their copper (they are insulated from each other, so each layer carries its own eddy loops)." % (0.035e-3 / P.PAD_T))


if __name__ == "__main__":
    main()
