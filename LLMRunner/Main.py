import os
import json

def GenerateTrendSummary():

    file_path = os.path.join("DataSets", "BaseDataSet.txt")

    with open(file_path, "r") as f:
        data = json.load(f)

    # Limit rows to avoid context overload
    data = data[-30:]

    lines = ["Date,Open,Close,High,Low,Volume"]
    for row in data:
        lines.append(
            f"{row['datadate']},{row['OpenVal']},{row['CloseVal']},{row['HighVal']},{row['LowVal']},{row['quantity']}"
        )

    market_text = "\n".join(lines)

    prompt = f"""
Financial Market Analysis

Dataset (Daily OHLC Data):
{market_text}

Instructions:
Analyze the dataset and fill in the following fields using the data provided:

Trend:           # bullish, bearish, or sideways
Volatility:      # low, moderate, high
Notable Movements:  # any spikes, gaps, or unusual changes
Summary:         # short paragraph summarizing the behaviour

Analysis:
"""

    return prompt

def GenerateForecastPrompt(market_data_list, indicators):

    # Use last 30 days for context
    recent_data = market_data_list[-30:]

    # Convert to table
    lines = ["Date,Open,Close,High,Low,Volume"]
    for row in recent_data:
        lines.append(
            f"{row.datadate},{row.OpenVal},{row.CloseVal},{row.HighVal},{row.LowVal},{row.quantity}"
        )
    market_text = "\n".join(lines)

    # Extract latest indicator values
    def get_last_valid(arr):
        return [x for x in arr if x == x][-1]  # remove NaN

    rsi = round(get_last_valid(indicators["RSI_14"]), 2)
    sma = round(get_last_valid(indicators["SMA_20"]), 2)
    ema = round(get_last_valid(indicators["EMA_20"]), 2)
    macd = round(get_last_valid(indicators["MACD"]), 4)
    macd_signal = round(get_last_valid(indicators["MACD_signal"]), 4)
    bb_upper = round(get_last_valid(indicators["BB_upper"]), 2)
    bb_lower = round(get_last_valid(indicators["BB_lower"]), 2)

    # Convert indicators to signals
    if rsi > 70:
        rsi_signal = "overbought"
    elif rsi < 30:
        rsi_signal = "oversold"
    else:
        rsi_signal = "neutral"

    macd_signal_text = "bullish" if macd > macd_signal else "bearish"

    prompt = f"""
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

Forecast:
"""

    return prompt