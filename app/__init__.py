"""Core stock analysis bot entrypoint."""

from __future__ import annotations

import argparse
import json

from app.config import settings
from app.data_client import MarketDataClient
from app.indicators import add_technical_indicators
from app.summary import build_market_summary, generate_ai_summary


class StockAnalysisBot:
    """Analyze a stock ticker using price history, sentiment, and trend signals."""

    def __init__(self, ticker: str = settings.stock_ticker, api_key: str | None = settings.openai_api_key, model: str = settings.openai_model):
        self.ticker = ticker.upper()
        self.api_key = api_key
        self.model = model

    def analyze(self, period: str = "6mo", interval: str = "1d", include_ai_summary: bool = False) -> dict:
        client = MarketDataClient(self.ticker)
        raw_data = client.fetch_history(period=period, interval=interval)
        enriched = add_technical_indicators(raw_data)
        summary = build_market_summary(enriched, self.ticker)

        if include_ai_summary and self.api_key:
            summary["ai_summary"] = generate_ai_summary(summary, self.api_key, self.model)

        return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the stock analysis bot for a given ticker.")
    parser.add_argument("ticker", nargs="?", default=settings.stock_ticker, help="Stock ticker symbol, such as AAPL or MSFT")
    parser.add_argument("--period", default="6mo", help="Time period for historical prices, e.g. 1mo, 6mo, 1y")
    parser.add_argument("--interval", default="1d", help="Data interval, e.g. 1d, 1h")
    parser.add_argument("--ai-summary", action="store_true", help="Generate a natural-language AI summary if OpenAI credentials are configured")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bot = StockAnalysisBot(ticker=args.ticker, api_key=settings.openai_api_key, model=settings.openai_model)
    result = bot.analyze(period=args.period, interval=args.interval, include_ai_summary=args.ai_summary)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
