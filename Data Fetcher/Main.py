from API import *


StartDate = date.fromisoformat("2025-01-01")
EndDate   = date.fromisoformat("2025-01-31")

'^GSPC = Stock code for S&P 500 '
StockData = GetStockData("^GSPC", StartDate, EndDate) 
for stocks in StockData:
    print(stocks.OpenVal)