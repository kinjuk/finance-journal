#!/usr/bin/env python3
"""Template: walk-forward test of a moving-average trend system (Kaufman, testing.md).
Replace `price` with real closes. Reports out-of-sample metrics and the chosen-parameter history.
If chosen parameters jump around (e.g. 38, 128, 57), the in-sample window is too short or the system is not robust."""
import numpy as np
from metrics import report, walk_forward, pct_step_values
from indicators import ma_direction_signal

rng = np.random.default_rng(21)
ret = rng.normal(0.0003, 0.01, 3000)
for k in range(5): ret[k * 600:k * 600 + 120] += 0.004      # synthetic trending regimes (demo only)
price = 100 * np.cumprod(1 + ret)

periods = pct_step_values(5, 200, 1.5)                        # percentage-step ladder, fixed BEFORE testing

def strat(p, n):
    pos = ma_direction_signal(p, n)
    r = np.zeros(len(p)); r[1:] = pos[:-1] * (p[1:] / p[:-1] - 1.0)   # position decided on prior close
    return r                                                   # add per-trade costs here for real use

fit = lambda train: max(periods, key=lambda n: report(strat(train, n))["information_ratio"])
oos, chosen = walk_forward(price, fit, strat, in_len=750, out_len=250)

print("periods tested:", periods)
print("chosen per window:", chosen)
for k, v in report(oos).items():
    print(f"{k:32s} {v:.4f}" if isinstance(v, float) else f"{k:32s} {v}")
print("buy-and-hold IR:", round(report(ret[750:])["information_ratio"], 2))
