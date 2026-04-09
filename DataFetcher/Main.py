from DataFetcher.API import *
from DataFetcher.Converters import *
from LLMRunner.Main import *
from DataFetcher.Classes import *

import os
import json

def GetDataset(StartDate,EndDate, StockCode, llama):

    #=========================
    # GET DATA
    #=========================
    MarketDataObject = GetStockData(StockCode, StartDate, EndDate) 

    #=========================
    # CONVERT DATA TO LIST & SAVE
    #=========================
    # Convert list of MarketData objects to dict
    DataSetDict = [marketdata_to_dict(md) for md in MarketDataObject]
    # Convert list of MarketData objects to PriceChangeObjects
    PriceChangeObject = [PriceChange(md) for md in MarketDataObject]
    # Convert list of PriceChangeObjects objects to dict
    PriceChangeDict = [pricechange_to_dict(md) for md in PriceChangeObject]

    # Create folder if it doesn't exist
    folder_path = "DataSets"   
    os.makedirs(folder_path, exist_ok=True)

    # Save Price Data
    file_path = os.path.join(folder_path, "BaseDataSet.txt")
    with open(file_path, "w") as f:
        json.dump(DataSetDict, f, indent=4)

    # Save Percentage Data
    file_path = os.path.join(folder_path, "PriceChange.txt")
    with open(file_path, "w") as f:
        json.dump(PriceChangeDict, f, indent=4)

    #=========================
    # DO INDICATOR CALCULATIONS & SAVE
    #=========================

    # Calculate indicators
    Indicators = calculate_indicators(MarketDataObject)
    
    # Save indicators
    file_path = os.path.join(folder_path, "Indicators.txt")
    with open(file_path, "w") as f:
        json.dump(Indicators, f, indent=4)


    #=========================
    # REMOVE OUTLIERS
    #=========================

    # Remove outliers from MarketData Object
    NoOutliers_DatasetObject = remove_price_outliers(MarketDataObject)
    # Change MarketData object to PriceChange Object and Remove Outliers
    NoOutliers_PriceChangeObject = remove_pricechange_outliers(MarketDataObject)



    BaseDataSet_NoOutliers = [marketdata_to_dict(md) for md in NoOutliers_DatasetObject]
    PriceChange_NoOutliers = [pricechange_to_dict(md) for md in NoOutliers_PriceChangeObject]

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
    messages = GenerateTrendSummary(MarketDataObject)
    prompt = llama.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    LLMSummary = llama.generate_text(prompt)
    file_path = os.path.join(folder_path, "LLMSummary.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(LLMSummary)

    #Cleaned Dataset
    messages = GenerateTrendSummary(NoOutliers_DatasetObject)
    prompt = llama.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    LLMSummary_NoOutliers = llama.generate_text(prompt)
    file_path = os.path.join(folder_path, "LLMSummary_NoOutliers.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(LLMSummary_NoOutliers)

    return MarketDataObject, NoOutliers_DatasetObject, PriceChangeObject, NoOutliers_PriceChangeObject, LLMSummary, LLMSummary_NoOutliers, Indicators