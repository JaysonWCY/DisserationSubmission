from LLMRunner.Initialiser import *

from Settings import *
from Llama8B.LlamaClass import *
from DataFetcher.Main import *

def RunProgram():
    #=========================
    # START LLAMA
    #=========================
    llama = LlamaModel("./Llama8B")

    #=========================
    # GETS DATASET AND CALCULATIONS
    #=========================

    StartDate = date.fromisoformat("2025-01-01")
    EndDate   = date.fromisoformat("2025-01-31")
    StockCode = "^GSPC"        # ^GSPC = STOCK CODE FOR S&P 500
    GetDataset(StartDate, EndDate, StockCode, llama)

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
    print(ModelList)




RunProgram()
