"""Data ingestion. Network calls live here only, so the rest is testable offline."""
import pandas as pd

# Equal-weight "AI basket". Known limitation: today's winners (survivorship bias).
BASKET = ["NVDA", "MSFT", "GOOGL", "META", "AMZN", "AVGO", "AMD", "TSM", "ORCL", "PLTR"]
BENCHMARK = "SPY"
VIX = "^VIX"


def fetch_prices(tickers, start="2000-01-01") -> pd.DataFrame:
    import yfinance as yf  # imported lazily so tests don't need it

    px = yf.download(tickers, start=start, auto_adjust=True, progress=False)["Close"]
    if isinstance(px, pd.Series):
        px = px.to_frame(tickers[0] if isinstance(tickers, list) else tickers)
    return px.sort_index()


def fetch_fred(series_id: str) -> pd.Series:
    """FRED's public CSV endpoint, no API key needed."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    df = pd.read_csv(url, index_col=0, parse_dates=True)
    s = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna()
    s.name = series_id
    return s
