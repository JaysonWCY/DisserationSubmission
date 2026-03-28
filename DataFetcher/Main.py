from DataFetcher.API import *
from DataFetcher.Converters import *
from LLMRunner.Main import *

import os
import json

def GetDataset(StartDate,EndDate, StockCode, llama):

    #=========================
    # GET DATA
    #=========================
    StockData = GetStockData(StockCode, StartDate, EndDate) 

    #=========================
    # CONVERT DATA TO LIST & SAVE
    #=========================
    # Convert list of MarketData objects
    json_data = [marketdata_to_dict(md) for md in StockData]
    # Convert list of PriceChange objects
    price_change_data = [pricechange_to_dict(md) for md in StockData]

    # Create folder if it doesn't exist
    folder_path = "DataSets"   
    os.makedirs(folder_path, exist_ok=True)

    # Save Price Data
    file_path = os.path.join(folder_path, "BaseDataSet.txt")
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)

    # Save Percentage Data
    file_path = os.path.join(folder_path, "PriceChange.txt")
    with open(file_path, "w") as f:
        json.dump(price_change_data, f, indent=4)

    #=========================
    # DO INDICATOR CALCULATIONS & SAVE
    #=========================

    # Calculate indicators
    indicator_data = calculate_indicators(StockData)
    
    # Save indicators
    file_path = os.path.join(folder_path, "Indicators.txt")
    with open(file_path, "w") as f:
        json.dump(indicator_data, f, indent=4)


    #=========================
    # REMOVE OUTLIERS
    #=========================

    clean_price_data = remove_price_outliers(StockData)
    clean_pricechange_data = remove_pricechange_outliers(StockData)

    clean_price_json = [marketdata_to_dict(md) for md in clean_price_data]
    clean_pricechange_json = [pricechange_to_dict(md) for md in clean_pricechange_data]

    # Save Clean raw prices
    file_path = os.path.join(folder_path, "BaseDataSet_NoOutliers.txt")
    with open(file_path, "w") as f:
        json.dump(clean_price_json, f, indent=4)

    # Save Clean price changes
    file_path = os.path.join(folder_path, "PriceChange_NoOutliers.txt")
    with open(file_path, "w") as f:
        json.dump(clean_pricechange_json, f, indent=4)

        
    # #=========================
    # # GENERATE TREND SUMMARIES
    # #=========================
    # prompt = GenerateTrendSummary()
    # output = llama.generate_text(prompt)
    # print(output)
