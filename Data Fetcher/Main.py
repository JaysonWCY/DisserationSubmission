from API import *

import os
import json


StartDate = date.fromisoformat("2025-01-01")
EndDate   = date.fromisoformat("2025-01-31")


'^GSPC = Stock code for S&P 500 '
StockData = GetStockData("^GSPC", StartDate, EndDate) 
for stocks in StockData:
    print(stocks.OpenVal)

# Convert MarketData object to dict
def marketdata_to_dict(md: MarketData):
    return {
        "id": md.id,
        "datadate": str(md.datadate),
        "OpenVal": md.OpenVal,
        "CloseVal": md.CloseVal,
        "HighVal": md.HighVal,
        "LowVal": md.LowVal,
        "quantity": md.quantity
    }

# Convert list of MarketData objects
json_data = [marketdata_to_dict(md) for md in StockData]



folder_path = "DataSets"          # e.g. "data" or "datasets/market"
file_path = os.path.join(folder_path, "BaseDataSet.txt")

# Create folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Save to file
with open(file_path, "w") as f:
    json.dump(json_data, f, indent=4)