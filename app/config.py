"""Application configuration and environment settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    stock_ticker: str = os.getenv("STOCK_TICKER", "AAPL")
    market_data_provider: str = os.getenv("MARKET_DATA_PROVIDER", "yfinance")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
