from LLMRunner.Initialiser import *

from Settings import *
from Llama318BInstruct.LlamaClass import *
from DataFetcher.Main import *

def RunProgram():
    #=========================
    # START LLAMA
    #=========================
    llama = LlamaModel("./Llama318BInstruct")

    #=========================
    # GETS DATASET AND CALCULATIONS
    #=========================

    StartDate = date.fromisoformat("2025-01-01") 
    EndDate   = date.fromisoformat("2025-01-31")
    StockCode = "^GSPC"        # ^GSPC = STOCK CODE FOR S&P 500
    BaseDataSet, BaseDataSet_NoOutliers, PriceChange, PriceChange_NoOutliers, LLMSummary, LLMSummary_NoOutliers, Indicators = GetDataset(StartDate, EndDate, StockCode, llama)

    #=========================
    # VALIDATING MODEL & GENERATING IDS FROM SETTINGS FILE
    #=========================

    validModelStartID = ValidateModelID(ModelIDStartRange, "ModelIDStartRange")
    validModelEndID = ValidateModelID(ModelIDEndRange, "ModelIDEndRange")

    if validModelStartID == False or validModelEndID == False:
        sys.exit(1)
    else:
        print("Model IDs are valid")
    
    ModelList = GenerateModelList(ModelIDStartRange, ModelIDEndRange)

    datasets = {
        (0, 0): BaseDataSet,
        (0, 1): BaseDataSet_NoOutliers,
        (1, 0): PriceChange,
        (1, 1): PriceChange_NoOutliers,
        (2, 0): LLMSummary,
        (2, 1): LLMSummary_NoOutliers,
    }

    duration_map = {
        0: "One Month",
        1: "One Week"
    }

    for model in ModelList:
        key = (model[0], model[1])

        if key not in datasets:
            raise ValueError(f"Invalid config: {model}")

        # Gets respective dataset
        dataset = datasets[key]

        # Checks if model uses indicator or not
        indicators = Indicators if model[2] == 1 else ""

        # Get respective duration
        duration = duration_map.get(model[3], "One Month")

        PredictionFunction(dataset, indicators, duration)

RunProgram()

