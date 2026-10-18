"""python -m heat.pipeline  ->  writes data/heat.csv"""
from pathlib import Path

from . import data
from .indicators import build_indicators
from .score import heat_score

OUT = Path(__file__).resolve().parents[2] / "data" / "heat.csv"


def run() -> None:
    basket = data.fetch_prices(data.BASKET)
    spy = data.fetch_prices([data.BENCHMARK])[data.BENCHMARK]
    vix = data.fetch_prices([data.VIX])[data.VIX]
    cpi = data.fetch_fred("CPIAUCSL")
    y10 = data.fetch_fred("DGS10")

    ind = build_indicators(basket, spy, vix, cpi, y10)
    scores = heat_score(ind.dropna())
    OUT.parent.mkdir(exist_ok=True)
    scores.to_csv(OUT)
    print(f"Wrote {len(scores)} rows to {OUT}. Latest heat: {scores['heat'].iloc[-1]:.1f}")


if __name__ == "__main__":
    run()
