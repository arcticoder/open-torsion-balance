"""test_slowdemod.py — synthetic runs for slowdemod.py (docs/campaign_loop.md section 4.6)."""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slowdemod as SD  # noqa: E402

failures = []


def check(label, ok, detail=""):
    print(("[PASS] " if ok else "[FAIL] ") + label + (": " + detail if detail else ""))
    if not ok:
        failures.append(label)


FS, FMOD, DUR = 2.0, 0.025, 1000.0
t = np.arange(0, DUR, 1 / FS)
ref = ((t * FMOD) % 1.0 < 0.5).astype(float)


def red(rng, n, amp):
    w = rng.normal(size=n)
    f = np.fft.rfftfreq(n, 1 / FS)
    f[0] = f[1]
    return amp * np.fft.irfft(np.fft.rfft(w) / np.sqrt(f / f[1]), n)


def run(seed, A=1.0, leak=0.0, driven_coupling=0.0, sign=1.0):
    rng = np.random.default_rng(seed)
    T = red(rng, len(t), 0.5)  # a temperature witness, independent of the drive
    B = red(rng, len(t), 0.3) + driven_coupling * ref  # a field witness that follows the drive
    y = sign * A * ref + 0.3 * rng.normal(size=len(t)) + red(rng, len(t), 0.4) + 0.002 * t + leak * T + 0.0 * B
    return y, {"T": T, "B": B}


n, hits, sig = 100, 0, []
for s in range(n):
    y, w = run(s)
    r = SD.demodulate(t, y, ref, FMOD, {"T": w["T"]})
    hits += abs(r["A"] - 1.0) < 2 * r["sigma"]
    sig.append(r["sigma"])
check("the recovered step is within 2 sigma of the truth in over 90 %% of %d realizations (1/f drift, white noise, a linear drift)" % n, hits / n > 0.90, "%d/%d, median sigma %.3f" % (hits, n, np.median(sig)))

rng5 = np.random.default_rng(55)
Tw = rng5.normal(size=len(t))  # a broadband witness
y = 1.0 * ref + 0.3 * rng5.normal(size=len(t)) + 2.0 * Tw
w = {"T": Tw}
r = SD.demodulate(t, y, ref, FMOD, {"T": Tw})
check("a leaked independent witness (temperature) is removed by the regression and the residual drops", r["resid_rms_after"] < 0.8 * r["resid_rms_before"] and "T" in r["kept_witnesses"], "rms %.3f -> %.3f" % (r["resid_rms_before"], r["resid_rms_after"]))

y, w = run(6, driven_coupling=3.0)
r = SD.demodulate(t, y, ref, FMOD, {"T": w["T"], "B": w["B"]})
r_named = SD.demodulate(t, y, ref, FMOD, {"T": w["T"], "B": w["B"]}, driven=("B",))
check("a witness that follows the drive (rule D) is dropped by the per-run test and by name, and the signal is NOT reduced", "B" in r["dropped_witnesses"] and "B" in r_named["dropped_witnesses"] and abs(r["A"] - 1.0) < 3 * r["sigma"], "z %.1f, A %.3f +- %.3f" % (r["dropped_witnesses"].get("B", 0), r["A"], r["sigma"]))
spread_off = np.std([SD.demodulate(t, run(k, driven_coupling=3.0)[0], ref, FMOD, {"B": run(k, driven_coupling=3.0)[1]["B"]}, z_drop=1e9)["A"] for k in range(20, 40)])
spread_on = np.std([SD.demodulate(t, run(k, driven_coupling=3.0)[0], ref, FMOD, {"B": run(k, driven_coupling=3.0)[1]["B"]})["A"] for k in range(20, 40)])
check("without rule D a driven witness makes the recovered step unreliable (scatter over 20 runs at least 5 times larger than with rule D)", spread_off > 5 * spread_on, "scatter %.3f without, %.3f with" % (spread_off, spread_on))

y, w = run(7, sign=-1.0)
r = SD.demodulate(t, y, ref, FMOD, {"T": w["T"]})
check("swapping the polarity (the force changes sign) flips the recovered step", r["A"] < -0.5, "A %.3f" % r["A"])

print()
if failures:
    print("%d check(s) failed: %s" % (len(failures), failures))
    sys.exit(1)
print("All checks passed.")
