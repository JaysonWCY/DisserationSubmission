import os
import json


def GenerateTrendSummary(data):

    lines = ["Date,Open,Close,High,Low,Volume"]
    highs, lows, closes = [], [], []

    for row in data:
        open_v = float(row['OpenVal'])
        close_v = float(row['CloseVal'])
        high_v = float(row['HighVal'])
        low_v = float(row['LowVal'])
        volume = row['quantity']

        lines.append(f"{row['datadate']},{open_v},{close_v},{high_v},{low_v},{volume}")

        highs.append(high_v)
        lows.append(low_v)
        closes.append(close_v)

    market_text = "\n".join(lines)

    key_high = max(highs) if highs else 0
    key_low = min(lows) if lows else 0
    avg_close = sum(closes) / len(closes) if closes else 0

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial market analyst.\n"
                "Follow these rules:\n"
                "- Do NOT write code\n"
                "- Do NOT use markdown\n"
                "- ONLY output the required fields\n"
                "- Be concise and structured"
            )
        },
        {
            "role": "user",
            "content": f"""
Analyze the following dataset and provide a structured analysis.

Dataset (OHLC data):
{market_text}

Key Prices:
- Highest Price: {key_high}
- Lowest Price: {key_low}
- Average Closing Price: {avg_close:.2f}

Instructions:
- Identify the overall trend (bullish, bearish, sideways)
- Assess volatility (low, moderate, high)
- Highlight notable movements
- Provide a short summary

Output format (STRICT):

Key Prices: <text>
Trend: <text>
Volatility: <text>
Notable Movements: <text>
Summary: <text>
"""
        }
    ]

    return messages


def GenerateForecastPrompt(market_data_list, indicators):

    # Use last 30 days
    recent_data = market_data_list[-30:]

    # Convert to table
    lines = ["Date,Open,Close,High,Low,Volume"]
    for row in recent_data:
        lines.append(
            f"{row.datadate},{row.OpenVal},{row.CloseVal},{row.HighVal},{row.LowVal},{row.quantity}"
        )

    market_text = "\n".join(lines)

    # Helper to get last valid value
    def get_last_valid(arr):
        return [x for x in arr if x == x][-1]

    # Extract indicators
    rsi = round(get_last_valid(indicators["RSI_14"]), 2)
    sma = round(get_last_valid(indicators["SMA_20"]), 2)
    ema = round(get_last_valid(indicators["EMA_20"]), 2)
    macd = round(get_last_valid(indicators["MACD"]), 4)
    macd_signal = round(get_last_valid(indicators["MACD_signal"]), 4)
    bb_upper = round(get_last_valid(indicators["BB_upper"]), 2)
    bb_lower = round(get_last_valid(indicators["BB_lower"]), 2)

    # Signals
    if rsi > 70:
        rsi_signal = "overbought"
    elif rsi < 30:
        rsi_signal = "oversold"
    else:
        rsi_signal = "neutral"

    macd_signal_text = "bullish" if macd > macd_signal else "bearish"

    # Build structured messages (NEW FORMAT)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial market forecasting expert.\n"
                "Follow these rules:\n"
                "- Do NOT write code\n"
                "- Do NOT use markdown\n"
                "- ONLY output the required fields\n"
                "- Be concise and structured"
            )
        },
        {
            "role": "user",
            "content": f"""
Financial Market Forecasting Task

Recent Market Data (last 30 days):
{market_text}

Technical Indicators (latest values):
- RSI (14): {rsi} ({rsi_signal})
- SMA (20): {sma}
- EMA (20): {ema}
- MACD: {macd} vs Signal {macd_signal} ({macd_signal_text})
- Bollinger Bands: Upper {bb_upper}, Lower {bb_lower}

Task:
Based on the data and indicators, predict the market behaviour over the next 30 days.

Provide the forecast in the following structure:

Trend (next 30 days):
Expected Price Range:
Volatility:
Key Drivers:
Final Outlook:
"""
        }
    ]

    return messages