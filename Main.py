from LLMRunner.Initialiser import *
from LLMRunner.Settings import *
from Llama8B.LlamaClass import *

def RunProgram():
    validModelStartID = ValidateModelID(ModelIDStartRange, "ModelIDStartRange")
    validModelEndID = ValidateModelID(ModelIDEndRange, "ModelIDEndRange")

    if validModelStartID == False or validModelEndID == False:
        sys.exit(1)
    else:
        print("Model IDs are valid")
    
    ModelList = GenerateModelList(ModelIDStartRange, ModelIDEndRange)
    print(ModelList)
    
    llama = LlamaModel("./Llama8B")

    # Run your prompt
    prompt = "Explain stock volatility in simple terms."
    output = llama.generate_text(prompt)
    print(output)


RunProgram()
