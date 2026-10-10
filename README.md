# Stock Market AI Bots

A starter Python project for building a multi-agent stock market analysis system. This repository focuses on a core stock-analysis bot that fetches market data, computes common technical indicators, and produces a structured summary.

## Project goals

- Pull stock price history from Yahoo Finance
- Compute technical indicators such as SMA and RSI
- Summarize trend, momentum, and risk indicators
- Prepare the bot for future multi-agent communication and AI reasoning layers

## Repository structure

- `app/` - bot code and supporting modules
- `requirements.txt` - Python dependencies
- `.env.example` - example environment variables
- `README.md` - project documentation

## Quick start

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy environment variables

```bash
cp .env.example .env
```

4. Run the bot

```bash
python -m app.bot AAPL --period 6mo --interval 1d
```

## Example output

```json
{
  "ticker": "AAPL",
  "latest_price": 214.37,
  "daily_change_percent": 1.28,
  "trend": "Bullish",
  "rsi": 62.14,
  "sma_20": 208.84,
  "sma_50": 198.42,
  "market_sentiment": "Positive momentum with moderate strength",
  "risk_note": "No major warning flags, but monitor price action near resistance."
}
```

## Future expansion

This is the foundation for a broader multi-agent system where separate bots can work together, such as:

- market-data bot
- news-and-sentiment bot
- risk-evaluation bot
- portfolio-recommendation bot
- coordinator bot

## Notes

This project uses public market data from Yahoo Finance for educational and analysis purposes. It does not provide investment advice.
