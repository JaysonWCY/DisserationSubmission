import sys
from itertools import product

"""
CHECK VALID MODEL ID
"""

def ValidateModelID(ModelID, StartOrEnd="ModelID"):
    # Convert to string if integer
    if isinstance(ModelID, int):
        ModelID = str(ModelID)
    elif not isinstance(ModelID, str):
        print(f"{StartOrEnd} should be a string or integer")
        print("Please read SettingsManual.py")
        return False

    # Convert to digits
    digits = [int(d) for d in ModelID]

    # Check length
    if len(digits) != 4:
        print(f"{StartOrEnd} has the wrong length (should be 5 digits)")
        print("Please read SettingsManual.py")
        return False

    # Allowed values per position
    max_values = [2, 1, 1, 1]
    param_names = [
        "Data Representation",
        "Preprocess Data",
        "Technical Indicator",
        "Prediction Duration"
    ]

    for i, (digit, max_val) in enumerate(zip(digits, max_values)):
        if digit > max_val:
            print(f"{StartOrEnd} {param_names[i]} parameter value invalid")
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
        [0, 1],     # 3. Technical Indicators
        [0, 1]      # 4. Prediction Duration
    ]

    start_digits = [int(d) for d in str(ModelIDStart)]
    end_digits = [int(d) for d in str(ModelIDEnd)]

    # Iterate through combinations
    all_models = []
    for model in product(*position_values):
        if start_digits <= list(model) <= end_digits:
            all_models.append(list(model))

    return all_models