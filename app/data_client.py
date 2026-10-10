"""Market data client for retrieving stock history."""

from __future__ import annotations

import yfinance as yf
from pandas import DataFrame


class MarketDataClient:
    """Small wrapper around the yfinance API for stock market data."""

    def __init__(self, ticker: str):
        self.ticker = ticker.upper()

    def fetch_history(self, period: str = "6mo", interval: str = "1d") -> DataFrame:
        """Fetch a ticker's historical price data."""
        stock = yf.Ticker(self.ticker)
        data = stock.history(period=period, interval=interval)

        if data.empty:
            raise ValueError(f"No market data returned for ticker: {self.ticker}")

        return data.reset_index()
