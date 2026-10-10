"""Technical indicator calculations for stock analysis."""

from __future__ import annotations

import pandas as pd


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Attach a few common technical indicators to a price DataFrame."""
    output = df.copy()

    if "Close" not in output.columns:
        raise ValueError("Input DataFrame must contain a 'Close' column.")

    output["SMA_20"] = output["Close"].rolling(window=20, min_periods=1).mean()
    output["SMA_50"] = output["Close"].rolling(window=50, min_periods=1).mean()
    output["RSI_14"] = calculate_rsi(output["Close"], period=14)
    short_ema = output["Close"].ewm(span=12, adjust=False).mean()
    long_ema = output["Close"].ewm(span=26, adjust=False).mean()
    output["MACD"] = short_ema - long_ema

    return output
