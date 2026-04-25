from LLMRunner.Initialiser import *

from Settings import *
from Llama318BInstruct.LlamaClass import *
from DataFetcher.Main import *


def RunProgram():
    # =========================
    # START LLAMA
    # =========================
    llama = LlamaModel("./Llama318BInstruct")

    # =========================
    # GETS DATASET AND CALCULATIONS
    # =========================

    StartDate = date.fromisoformat("2025-01-01")
    EndDate = date.fromisoformat("2025-01-31")
    StockCode = "^GSPC"  # ^GSPC = STOCK CODE FOR S&P 500
    (
        BaseDataSet,
        BaseDataSet_NoOutliers,
        PriceChange,
        PriceChange_NoOutliers,
        LLMSummary,
        LLMSummary_NoOutliers,
        Indicators,
    ) = GetDataset(StartDate, EndDate, StockCode, llama)

    # =========================
    # VALIDATING MODEL & GENERATING IDS FROM SETTINGS FILE
    # =========================

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

    duration_map = {0: 5, 1: 10}

    all_results = []

    for model in ModelList:
        key = (model[0], model[1])

        if key not in datasets:
            raise ValueError(f"Invalid config: {model}")

        # Gets respective dataset
        dataset = datasets[key]

        # Checks if model uses indicator or not
        indicators = Indicators if model[2] == 1 else ""

        # Get respective duration
        duration = duration_map.get(model[3], 10)

        # 🔥 Split here
        if model[0] == 0:
            textprompt = GenerateMarketDataPrompt(dataset, indicators, duration)
        elif model[0] == 1:
            textprompt = GeneratePriceChangePrompt(dataset, indicators, duration)
        elif model[0] == 2:
            textprompt = GenerateSummaryToPricePrompt(dataset, indicators, duration)
        else:
            raise ValueError("Invalid data type")

        prompt = llama.tokenizer.apply_chat_template(textprompt, tokenize=False, add_generation_prompt=True)
        LLM_output = llama.generate_text(prompt)

          # =========================
        # STORE RESULT
        # =========================
        result_entry = {
            "model_config": model,
            "data_type": model[0],
            "outliers_removed": model[1],
            "used_indicators": model[2],
            "duration": duration,
            "raw_output": LLM_output
        }

        all_results.append(result_entry)

        # =========================
        # SAVE RAW LOG (DEBUG)
        # =========================
        with open("raw_outputs.txt", "a", encoding="utf-8") as f:
            f.write(f"MODEL: {model}\n")
            f.write(LLM_output + "\n")
            f.write("=" * 50 + "\n")

    # =========================
    # SAVE FINAL RESULTS (JSON)
    # =========================
    with open("experiment_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    PredictionEndDate = add_business_days(EndDate, 10)
    ActualStockData = GetStockData(StockCode, EndDate, PredictionEndDate)
    ActualDataSetDict = [marketdata_to_dict(md) for md in ActualStockData]
    with open("ActualStockData.json", "w", encoding="utf-8") as f:
        json.dump(ActualDataSetDict, f, indent=4)
    

def add_business_days(start_date, n):
    current = start_date
    days_added = 0

    while days_added < n:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Mon–Fri
            days_added += 1

    return current

RunProgram()
