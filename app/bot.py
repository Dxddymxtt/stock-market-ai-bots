"""Generate structured market summary objects from technical analysis results."""

from __future__ import annotations

import os

import pandas as pd


def build_market_summary(df: pd.DataFrame, ticker: str) -> dict:
    """Summarize market trend and momentum from recent price data."""
    if df.empty:
        raise ValueError("Cannot summarize an empty DataFrame.")

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    latest_close = float(latest["Close"])
    previous_close = float(previous["Close"])
    daily_change = ((latest_close - previous_close) / previous_close) * 100 if previous_close else 0.0

    sma_20 = float(latest.get("SMA_20", latest_close))
    sma_50 = float(latest.get("SMA_50", latest_close))
    rsi = float(latest.get("RSI_14", 50.0))
    macd = float(latest.get("MACD", 0.0))

    if latest_close > sma_20 and sma_20 > sma_50:
        trend = "Bullish"
    elif latest_close < sma_20 and sma_20 < sma_50:
        trend = "Bearish"
    else:
        trend = "Neutral"

    if rsi >= 70:
        momentum = "Overbought"
    elif rsi <= 30:
        momentum = "Oversold"
    elif rsi >= 55:
        momentum = "Positive momentum"
    elif rsi <= 45:
        momentum = "Weak momentum"
    else:
        momentum = "Balanced"

    if macd > 0:
        macd_comment = "Positive MACD momentum"
    else:
        macd_comment = "Negative MACD momentum"

    summary = {
        "ticker": ticker.upper(),
        "latest_price": round(latest_close, 2),
        "daily_change_percent": round(daily_change, 2),
        "trend": trend,
        "momentum": momentum,
        "rsi": round(rsi, 2),
        "sma_20": round(sma_20, 2),
        "sma_50": round(sma_50, 2),
        "macd": round(macd, 4),
        "market_sentiment": f"{trend} structure with {momentum.lower()} and {macd_comment.lower()}",
        "risk_note": "Monitor support and resistance as trend strength changes." if trend in {"Bullish", "Bearish"} else "Market is relatively balanced; watch for volatility.",
    }

    return summary


def generate_ai_summary(summary: dict, api_key: str | None = None, model: str = "gpt-4o-mini") -> str | None:
    """Generate a natural-language explanation using the OpenAI API if configured."""
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=api_key)
    prompt = (
        "Provide a concise trading insight from this stock summary. "
        "Keep it practical and professional. Mention trend, momentum, and risk.\n\n"
        f"Summary: {summary}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()
