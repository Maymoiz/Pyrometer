   # Pyrometer
   > Measuring how hot the AI market is running. Not predicting where it goes.

A transparent gauge of how stretched the AI-sector market looks relative to its own history.
**It does not predict prices.**

## Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                                   # offline tests
cd src && python -m heat.pipeline        # fetch data, compute scores -> data/heat.csv
uvicorn heat.api:app --reload            # http://127.0.0.1:8000/heat and /docs
```

## How the score works
Each indicator is converted to its percentile against *only past* data (expanding window),
sign-adjusted (low VIX = hotter), and averaged to 0-100.

## Known limitations (keep this section honest)
- Basket is today's winners: survivorship bias.
- v1 uses price and macro indicators only. Valuation multiples (P/E, P/S) need point-in-time
  data to avoid look-ahead bias, so they come later.
- Only a few real bubbles exist in history, so this is a risk gauge, not an oracle.
- Macro indicator signs are judgement calls.

## Roadmap
- v1: this repo, plus a simple dashboard
- v2: drawdown-probability model (walk-forward validation, calibration, naive baseline)
- v3: Docker, CI, scheduled refresh, drift monitoring
