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
    BaseDataSet = [marketdata_to_dict(md) for md in StockData]
    # Convert list of PriceChange objects
    PriceChange = [pricechange_to_dict(md) for md in StockData]

    # Create folder if it doesn't exist
    folder_path = "DataSets"   
    os.makedirs(folder_path, exist_ok=True)

    # Save Price Data
    file_path = os.path.join(folder_path, "BaseDataSet.txt")
    with open(file_path, "w") as f:
        json.dump(BaseDataSet, f, indent=4)

    # Save Percentage Data
    file_path = os.path.join(folder_path, "PriceChange.txt")
    with open(file_path, "w") as f:
        json.dump(PriceChange, f, indent=4)

    #=========================
    # DO INDICATOR CALCULATIONS & SAVE
    #=========================

    # Calculate indicators
    Indicators = calculate_indicators(StockData)
    
    # Save indicators
    file_path = os.path.join(folder_path, "Indicators.txt")
    with open(file_path, "w") as f:
        json.dump(Indicators, f, indent=4)


    #=========================
    # REMOVE OUTLIERS
    #=========================

    clean_price_data = remove_price_outliers(StockData)
    clean_pricechange_data = remove_pricechange_outliers(StockData)

    BaseDataSet_NoOutliers = [marketdata_to_dict(md) for md in clean_price_data]
    PriceChange_NoOutliers = [pricechange_to_dict(md) for md in clean_pricechange_data]

    # Save Clean raw prices
    file_path = os.path.join(folder_path, "BaseDataSet_NoOutliers.txt")
    with open(file_path, "w") as f:
        json.dump(BaseDataSet_NoOutliers, f, indent=4)

    # Save Clean price changes
    file_path = os.path.join(folder_path, "PriceChange_NoOutliers.txt")
    with open(file_path, "w") as f:
        json.dump(PriceChange_NoOutliers, f, indent=4)

        
    #=========================
    # GENERATE TREND SUMMARIES
    #=========================

    #Base Dataset
    messages = GenerateTrendSummary(BaseDataSet)
    prompt = llama.tokenizer.apply_chat_template(messages, tokenize=False)
    LLMSummary = llama.generate_text(prompt)
    file_path = os.path.join(folder_path, "LLMSummary.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(LLMSummary)

    #Cleaned Dataset
    messages = GenerateTrendSummary(BaseDataSet_NoOutliers)
    prompt = llama.tokenizer.apply_chat_template(messages, tokenize=False)
    LLMSummary_NoOutliers = llama.generate_text(prompt)
    file_path = os.path.join(folder_path, "LLMSummary_NoOutliers.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(LLMSummary_NoOutliers)

    return BaseDataSet, BaseDataSet_NoOutliers, PriceChange, PriceChange_NoOutliers, LLMSummary, LLMSummary_NoOutliers, Indicators