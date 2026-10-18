"""Heat score: expanding-window percentile of each indicator, signed, averaged to 0-100.

Expanding (not full-sample) percentiles mean the score on day t only uses data up to t.
"""
import numpy as np
import pandas as pd

# +1: high value = hotter. -1: low value = hotter (e.g. low VIX = complacency).
# Macro signs are judgement calls; revisit them once you have a model to test them.
SIGNS = {
    "stretch_200d": 1,
    "momentum_12m": 1,
    "relative_strength": 1,
    "vix": -1,
    "yield_10y": 1,
    "cpi_yoy": 1,
}
MIN_HISTORY = 252 * 2


def expanding_percentile(s: pd.Series, min_periods: int = MIN_HISTORY) -> pd.Series:
    def rank_last(x: np.ndarray) -> float:
        return float((x[:-1] < x[-1]).mean())

    return s.expanding(min_periods=min_periods).apply(rank_last, raw=True)


def heat_score(ind: pd.DataFrame, signs: dict = SIGNS, min_periods: int = MIN_HISTORY) -> pd.DataFrame:
    comps = pd.DataFrame(index=ind.index)
    for col, sign in signs.items():
        pct = expanding_percentile(ind[col], min_periods)
        comps[col] = pct if sign > 0 else 1 - pct
    comps = comps * 100
    comps["heat"] = comps.mean(axis=1, skipna=False)
    return comps.dropna(subset=["heat"])
