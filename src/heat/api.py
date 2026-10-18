"""uvicorn heat.api:app --reload  (run from ./src, after running the pipeline)"""
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

CSV = Path(__file__).resolve().parents[2] / "data" / "heat.csv"
app = FastAPI(title="Pyrometer")


def _load() -> pd.DataFrame:
    if not CSV.exists():
        raise HTTPException(503, "No data yet. Run: python -m heat.pipeline")
    return pd.read_csv(CSV, index_col=0, parse_dates=True)


@app.get("/health")
def health():
    return {"status": "ok", "data_available": CSV.exists()}


@app.get("/heat")
def latest():
    df = _load()
    row = df.iloc[-1]
    return {
        "as_of": df.index[-1].date().isoformat(),
        "heat": round(float(row["heat"]), 1),
        "components": {k: round(float(v), 1) for k, v in row.drop("heat").items()},
    }


@app.get("/history")
def history(days: int = 365):
    df = _load().tail(max(1, min(days, 10000)))
    return {"dates": [d.date().isoformat() for d in df.index], "heat": df["heat"].round(1).tolist()}
