"""Turn raw series into indicators. Higher raw value = hotter, unless noted in score.SIGNS."""
import pandas as pd

CPI_PUBLICATION_LAG_DAYS = 45  # CPI for a month is published ~2 weeks after month end; be conservative


def basket_index(basket_px: pd.DataFrame) -> pd.Series:
    """Equal-weight daily-rebalanced index; tickers join when they start trading."""
    ret = basket_px.pct_change().mean(axis=1, skipna=True)
    return (1 + ret.fillna(0)).cumprod()


def build_indicators(basket_px, spy, vix, cpi, y10) -> pd.DataFrame:
    idx = basket_index(basket_px)
    spy = spy.reindex(idx.index).ffill()
    rel = idx / spy

    out = pd.DataFrame(index=idx.index)
    out["stretch_200d"] = idx / idx.rolling(200).mean() - 1
    out["momentum_12m"] = idx.pct_change(252)
    out["relative_strength"] = rel / rel.rolling(252 * 3).mean() - 1
    out["vix"] = vix.reindex(idx.index).ffill()

    # Macro: shift by publication lag so we only use what was public at the time.
    cpi_yoy = cpi.pct_change(12) * 100
    cpi_yoy.index = cpi_yoy.index + pd.Timedelta(days=CPI_PUBLICATION_LAG_DAYS)
    out["cpi_yoy"] = cpi_yoy.reindex(idx.index, method="ffill")
    out["yield_10y"] = y10.reindex(idx.index).ffill()
    return out
