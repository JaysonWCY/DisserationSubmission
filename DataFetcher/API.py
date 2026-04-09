from datetime import datetime, timedelta
import yfinance as yf

from DataFetcher.Classes import *

import yfinance as yf
from datetime import date


def GetStockData(StockListID, startDate: date, endDate: date):
    # Validate input dates
    if not isinstance(startDate, date):
        raise ValueError("startDate must be a date object")
    if not isinstance(endDate, date):
        raise ValueError("endDate must be a date object")
    if startDate >= endDate:
        raise ValueError("startDate must be earlier than endDate")

    # Download data from yfinance
    df = yf.download(StockListID, start=startDate, end=endDate)

    market_data_list = []
    for date_index, row in df.iterrows():
        data = MarketData(
            datadate=date_index.date(),
            OpenVal=float(row[("Open", "^GSPC")]),
            CloseVal=float(row[("Close", "^GSPC")]),
            HighVal=float(row[("High", "^GSPC")]),
            LowVal=float(row[("Low", "^GSPC")]),
            quantity=float(row[("Volume", "^GSPC")]),
        )
        market_data_list.append(data)

    return market_data_list
