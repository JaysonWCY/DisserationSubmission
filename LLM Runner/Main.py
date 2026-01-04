from Initialiser import *
from Settings import *


def RunProgram():
    validModelStartID = ValidateModelID(ModelIDStartRange, "ModelIDStartRange")
    validModelEndID = ValidateModelID(ModelIDEndRange, "ModelIDEndRange")

    if validModelStartID == False or validModelEndID == False:
        sys.exit(1)
    else:
        print("Model IDs are valid")
    
    ModelList = GenerateModelList(ModelIDStartRange, ModelIDEndRange)
    print(ModelList)



RunProgram()
