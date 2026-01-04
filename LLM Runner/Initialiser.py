import sys
from itertools import product

"""
CHECK VALID MODEL ID
"""


def ValidateModelID(ModelID, StartOrEnd):
    ModelStart_digits = [int(d) for d in str(ModelID)]

    if type(ModelID) != str:
        print(StartOrEnd + " should be an string")
        print("Please read SettingsManual.py")
        return False

    if len(ModelStart_digits) != 7:
        print(StartOrEnd + " has the wrong length")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[0] > 2:
        print(StartOrEnd + " Data representation parameter value invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[1] > 1:
        print(StartOrEnd + " Preprocess data parameter value invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[2] > 1:
        print(StartOrEnd + " Fundamental data parameter invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[3] > 1:
        print(StartOrEnd + " Technical Indicator parameter invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[4] > 1:
        print(StartOrEnd + " Macroeconomic data parameter value invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[5] > 1:
        print(StartOrEnd + " Prediction Architecture parameter invalid")
        print("Please read SettingsManual.py")
        return False

    if ModelStart_digits[6] > 1:
        print(StartOrEnd + " Prediction Duration parameter invalid")
        print("Please read SettingsManual.py")
        return False

    return True


"""
CREATE MODEL LIST
"""

def GenerateModelList(ModelIDStart, ModelIDEnd):
    # Allowed values for each position
    position_values = [
        [0, 1, 2],  # 1. Data Representation
        [0, 1],     # 2. Preprocess Data
        [0, 1],     # 3. Fundamental Data
        [0, 1],     # 4. Technical Indicators
        [0, 1],     # 5. Macroeconomic Data
        [0, 1],     # 6. Prediction Architecture
        [0, 1]      # 7. Prediction Duration
    ]

    start_digits = [int(d) for d in str(ModelIDStart)]
    end_digits = [int(d) for d in str(ModelIDEnd)]

    # Iterate through combinations
    all_models = []
    for model in product(*position_values):
        if start_digits <= list(model) <= end_digits:
            all_models.append(list(model))

    return all_models