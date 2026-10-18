import numpy as np
import pandas as pd

from heat.score import expanding_percentile, heat_score


def _series(n=800, seed=0):
    rng = np.random.default_rng(seed)
    return pd.Series(rng.normal(size=n).cumsum(), index=pd.bdate_range("2015-01-01", periods=n))


def test_rising_series_scores_high():
    s = pd.Series(np.arange(600, dtype=float), index=pd.bdate_range("2015-01-01", periods=600))
    assert expanding_percentile(s, 100).iloc[-1] > 0.99


def test_no_lookahead():
    """Changing the future must never change the past."""
    s = _series()
    a = expanding_percentile(s, 100)
    s2 = s.copy()
    s2.iloc[-50:] += 1000
    b = expanding_percentile(s2, 100)
    pd.testing.assert_series_equal(a.iloc[:-50], b.iloc[:-50])


def test_heat_bounds_and_sign():
    ind = pd.DataFrame({"x": _series(seed=1), "y": _series(seed=2)})
    h = heat_score(ind, signs={"x": 1, "y": -1}, min_periods=100)
    assert h["heat"].between(0, 100).all()
    assert np.isclose(h["x"] + h["y"], 2 * h["heat"]).all()
