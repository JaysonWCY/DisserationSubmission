import os
import json
from DataFetcher.Classes import *


def GenerateTrendSummary(data):

    lines = ["Date,Open,Close,High,Low,Volume"]
    highs, lows, closes = [], [], []

    for row in data:
        open_v = float(row.OpenVal)
        close_v = float(row.CloseVal)
        high_v = float(row.HighVal)
        low_v = float(row.LowVal)
        volume = row.quantity

        lines.append(f"{row.datadate},{open_v},{close_v},{high_v},{low_v},{volume}")

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
            ),
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
""",
        },
    ]

    return messages


def GenerateMarketDataPrompt(market_data_list, indicators, duration):

    # =========================
    # PREPARE MARKET DATA
    # =========================

    recent_data = market_data_list[-30:]

    lines = ["Date,Open,Close,High,Low,Volume"]

    for row in recent_data:
        lines.append(
            f"{row.datadate},{row.OpenVal},{row.CloseVal},{row.HighVal},{row.LowVal},{row.quantity}"
        )

    market_text = "\n".join(lines)

    # =========================
    # SAFE HELPER
    # =========================

    def get_last_valid(arr):
        if not arr:
            return 0
        valid = [x for x in arr if x is not None and x == x]
        return valid[-1] if valid else 0

    # =========================
    # EXTRACT INDICATORS
    # =========================

    if indicators and isinstance(indicators, list):

        rsi = round(get_last_valid([d.get("RSI") for d in indicators]), 2)
        sma = round(get_last_valid([d.get("SMA") for d in indicators]), 2)
        ema = round(get_last_valid([d.get("EMA") for d in indicators]), 2)
        macd = round(get_last_valid([d.get("MACD") for d in indicators]), 4)
        macd_signal = round(
            get_last_valid([d.get("MACD_signal") for d in indicators]), 4
        )
        bb_upper = round(
            get_last_valid([d.get("Bollinger_upper") for d in indicators]), 2
        )
        bb_lower = round(
            get_last_valid([d.get("Bollinger_lower") for d in indicators]), 2
        )

        indicator_text = f"""
Technical Indicators:
RSI: {rsi}
SMA: {sma}
EMA: {ema}
MACD: {macd}
MACD Signal: {macd_signal}
Bollinger Upper: {bb_upper}
Bollinger Lower: {bb_lower}
"""
    else:
        indicator_text = "No technical indicators provided."

    # =========================
    # JSON FORMAT (STRICT)
    # =========================

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial forecasting model.\n"
                "You MUST follow these rules strictly:\n"
                "- Do NOT explain reasoning\n"
                "- Do NOT add any text outside JSON\n"
                "- Output MUST be valid JSON only\n"
                "- Do NOT include markdown or comments\n"
                "- All values must be numbers or strings where specified\n"
                "- The JSON must be properly formatted and parsable"
            ),
        },
        {
            "role": "user",
            "content": f"""
Financial Market Forecasting Task

Recent Market Data (last 30 days):
{market_text}

{indicator_text}

Task:
Predict the next {duration} daily closing prices.

STRICT OUTPUT FORMAT:

Return ONLY valid JSON in the following structure:

{{
  "Predicted Daily Closing Prices": [
    {{"day": 1, "price": <number>}},
    {{"day": 2, "price": <number>}},
    ...
    {{"day": {duration}, "price": <number>}}
  ],
  "Predicted Price Range": {{
    "min": <number>,
    "max": <number>
  }},
  "Trend": "<Bullish | Bearish | Neutral>",
  "Volatility": "<Low | Moderate | High>",
  "Confidence": <number between 0 and 1>
}}

IMPORTANT RULES:
- Output EXACTLY {duration} predictions
- No extra fields
- No explanations
- JSON must be valid and parsable
""",
        },
    ]

    return messages


def GeneratePriceChangePrompt(price_change_list, indicators, duration):

    # =========================
    # BUILD PRICE CHANGE DATA
    # =========================

    combined_data = []

    for pc_obj in price_change_list:
        pc = pc_obj.percentage_change()

        if pc is not None and pc == pc:
            combined_data.append((pc_obj.market_data, pc))

    # Take last 30 valid entries
    combined_data = combined_data[-30:]

    lines = ["Date,PriceChange(%)"]

    for md, pc in combined_data:
        lines.append(f"{md.datadate},{round(pc, 4)}")

    market_text = "\n".join(lines)

    # =========================
    # GET STARTING PRICE
    # =========================

    last_close_price = None

    if price_change_list:
        last_md = price_change_list[-1].market_data
        if last_md and last_md.CloseVal is not None:
            last_close_price = round(last_md.CloseVal, 4)

    starting_price_text = (
        f"Starting Price: {last_close_price}"
        if last_close_price is not None
        else "Starting Price: Not available"
    )

    # =========================
    # SAFE HELPER
    # =========================

    def get_last_valid(arr):
        if not arr:
            return 0
        valid = [x for x in arr if x is not None and x == x]
        return valid[-1] if valid else 0

    # =========================
    # EXTRACT INDICATORS
    # =========================

    if indicators and isinstance(indicators, list):

        rsi = round(get_last_valid([d.get("RSI") for d in indicators]), 2)
        sma = round(get_last_valid([d.get("SMA") for d in indicators]), 2)
        ema = round(get_last_valid([d.get("EMA") for d in indicators]), 2)
        macd = round(get_last_valid([d.get("MACD") for d in indicators]), 4)
        macd_signal = round(
            get_last_valid([d.get("MACD_signal") for d in indicators]), 4
        )
        bb_upper = round(
            get_last_valid([d.get("Bollinger_upper") for d in indicators]), 2
        )
        bb_lower = round(
            get_last_valid([d.get("Bollinger_lower") for d in indicators]), 2
        )

        indicator_text = f"""
Technical Indicators:
RSI: {rsi}
SMA: {sma}
EMA: {ema}
MACD: {macd}
MACD Signal: {macd_signal}
Bollinger Upper: {bb_upper}
Bollinger Lower: {bb_lower}
"""
    else:
        indicator_text = "No technical indicators provided."

    # =========================
    # JSON FORMAT (STRICT)
    # =========================

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial forecasting model.\n"
                "You MUST follow these rules strictly:\n"
                "- Do NOT explain reasoning\n"
                "- Do NOT add any text outside JSON\n"
                "- Output MUST be valid JSON only\n"
                "- Do NOT include markdown or comments\n"
                "- All values must be numbers\n"
                "- Do NOT use null, NaN, Infinity, or empty values\n"
                "- The JSON must be properly formatted and parsable\n"
            ),
        },
        {
            "role": "user",
            "content": f"""
Financial Market Forecasting Task (Price Reconstruction)

{starting_price_text}

Recent Price Change Data (last 30 entries):
{market_text}

{indicator_text}

Task:
Using the starting price and predicted daily % changes, predict the next {duration} daily closing prices.

IMPORTANT:
- You are NOT directly outputting returns
- You must convert returns into cumulative prices internally
- Each price depends on the previous day

STRICT OUTPUT FORMAT:

Return ONLY valid JSON in the following structure:

{{
  "Predicted Daily Closing Prices": [
    {{"day": 1, "price": <number>}},
    {{"day": 2, "price": <number>}},
    ...
    {{"day": {duration}, "price": <number>}}
  ],
  "Predicted Price Range": {{
    "min": <number>,
    "max": <number>
  }},
  "Trend": "<Bullish | Bearish | Neutral>",
  "Volatility": "<Low | Moderate | High>",
  "Confidence": <number between 0 and 1>
}}

IMPORTANT RULES:
- Output EXACTLY {duration} predictions
- No extra fields
- No explanations
- Prices MUST be numeric floats
- Ensure JSON is valid and parsable
""",
        },
    ]

    return messages


def GenerateSummaryToPricePrompt(summary_text, indicators, duration):

    # =========================
    # SAFE HELPER
    # =========================

    def get_last_valid(arr):
        if not arr:
            return 0
        valid = [x for x in arr if x is not None and x == x]
        return valid[-1] if valid else 0

    # =========================
    # EXTRACT INDICATORS
    # =========================

    if indicators and isinstance(indicators, list):

        rsi = round(get_last_valid([d.get("RSI") for d in indicators]), 2)
        sma = round(get_last_valid([d.get("SMA") for d in indicators]), 2)
        ema = round(get_last_valid([d.get("EMA") for d in indicators]), 2)
        macd = round(get_last_valid([d.get("MACD") for d in indicators]), 4)
        macd_signal = round(get_last_valid([d.get("MACD_signal") for d in indicators]), 4)
        bb_upper = round(get_last_valid([d.get("Bollinger_upper") for d in indicators]), 2)
        bb_lower = round(get_last_valid([d.get("Bollinger_lower") for d in indicators]), 2)

        indicator_text = f"""
Technical Indicators:
RSI: {rsi}
SMA: {sma}
EMA: {ema}
MACD: {macd}
MACD Signal: {macd_signal}
Bollinger Upper: {bb_upper}
Bollinger Lower: {bb_lower}
"""
    else:
        indicator_text = "No technical indicators provided."

    # =========================
    # PROMPT
    # =========================

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial forecasting model.\n"
                "You MUST follow these rules strictly:\n"
                "- Do NOT explain reasoning\n"
                "- Do NOT add any text outside JSON\n"
                "- Output MUST be valid JSON only\n"
                "- Do NOT include markdown or comments\n"
                "- All values must be numbers or strings where specified\n"
                "- The JSON must be properly formatted and parsable\n"
            ),
        },
        {
            "role": "user",
            "content": f"""
Financial Market Forecasting Task (Summary + Indicators → Price Prediction)

Market Summary:
{summary_text}

{indicator_text}

Task:
Using the summary and technical indicators, predict the next {duration} daily closing prices.

Guidance:
- Use the summary for trend direction and volatility context
- Use RSI, MACD, and moving averages for confirmation
- Ensure prices move logically and sequentially
- Avoid unrealistic jumps unless volatility is high

STRICT OUTPUT FORMAT:

Return ONLY valid JSON in the following structure:

{{
  "Predicted Daily Closing Prices": [
    {{"day": 1, "price": <number>}},
    {{"day": 2, "price": <number>}},
    ...
    {{"day": {duration}, "price": <number>}}
  ],
  "Predicted Price Range": {{
    "min": <number>,
    "max": <number>
  }},
  "Trend": "<Bullish | Bearish | Neutral>",
  "Volatility": "<Low | Moderate | High>",
  "Confidence": <number between 0 and 1>
}}

IMPORTANT RULES:
- Output EXACTLY {duration} predictions
- No extra fields
- No explanations
- Prices must be numeric floats
- JSON must be valid and parsable
"""
        },
    ]

    return messages