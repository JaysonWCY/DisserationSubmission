import talib
import numpy as np

from DataFetcher.Classes import *
from statistics import mean, stdev

# Convert MarketData object to dict
def marketdata_to_dict(md: MarketData):
    return {
        "datadate": str(md.datadate),
        "OpenVal": md.OpenVal,
        "CloseVal": md.CloseVal,
        "HighVal": md.HighVal,
        "LowVal": md.LowVal,
        "quantity": md.quantity
    }

def pricechange_to_dict(md: PriceChange):
    return {
        "datadate": str(md.market_data.datadate),
        "percentage_change": md.percentage_change()
    }

def remove_price_outliers(stock_data, threshold=3):
    closes = [md.CloseVal for md in stock_data if md.CloseVal is not None]

    mu = mean(closes)
    sigma = stdev(closes)

    filtered = [
        md for md in stock_data
        if md.CloseVal is not None and abs((md.CloseVal - mu) / sigma) <= threshold
    ]

    return filtered

def remove_pricechange_outliers(stock_data, threshold=3):
    changes = []

    # First pass: collect valid percentage changes
    for md in stock_data:
        pc = PriceChange(md).percentage_change()
        if pc is not None:
            changes.append(pc)

    mu = mean(changes)
    sigma = stdev(changes)

    filtered = []

    for md in stock_data:
        pc = PriceChange(md).percentage_change()

        if pc is not None:
            z_score = abs((pc - mu) / sigma)

            if z_score <= threshold:
                filtered.append(PriceChange(md))

    return filtered

def calculate_indicators(stock_data):

    closes = np.array([md.CloseVal for md in stock_data])
    highs = np.array([md.HighVal for md in stock_data])
    lows = np.array([md.LowVal for md in stock_data])

    # Calculate indicators
    sma = talib.SMA(closes, timeperiod=5)
    ema = talib.EMA(closes, timeperiod=5)
    rsi = talib.RSI(closes, timeperiod=5)
    macd, macd_signal, macd_hist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    upper, middle, lower = talib.BBANDS(closes, timeperiod=5)
    atr = talib.ATR(highs, lows, closes, timeperiod=5)

    # Pivot Points (classic)
    pivot = (highs + lows + closes) / 3
    support1 = 2 * pivot - highs
    resistance1 = 2 * pivot - lows
    support2 = pivot - (highs - lows)
    resistance2 = pivot + (highs - lows)

    # Build JSON-serializable list
    indicator_list = []
    for i, md in enumerate(stock_data):
        indicator_list.append({
            'Date': str(md.datadate),
            'SMA': float(sma[i]) if not np.isnan(sma[i]) else None,
            'EMA': float(ema[i]) if not np.isnan(ema[i]) else None,
            'RSI': float(rsi[i]) if not np.isnan(rsi[i]) else None,
            'MACD': float(macd[i]) if not np.isnan(macd[i]) else None,
            'MACD_signal': float(macd_signal[i]) if not np.isnan(macd_signal[i]) else None,
            'Bollinger_upper': float(upper[i]) if not np.isnan(upper[i]) else None,
            'Bollinger_lower': float(lower[i]) if not np.isnan(lower[i]) else None,
            'ATR': float(atr[i]) if not np.isnan(atr[i]) else None,
            'Pivot': float(pivot[i]) if not np.isnan(pivot[i]) else None,
            'Support1': float(support1[i]) if not np.isnan(support1[i]) else None,
            'Resistance1': float(resistance1[i]) if not np.isnan(resistance1[i]) else None,
            'Support2': float(support2[i]) if not np.isnan(support2[i]) else None,
            'Resistance2': float(resistance2[i]) if not np.isnan(resistance2[i]) else None,
        })
    return indicator_list