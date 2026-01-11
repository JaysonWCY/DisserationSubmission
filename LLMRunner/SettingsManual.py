'''
MODEL ID RANGE

Must be 7 digits 

Position / Meaning / Allowed Values
1. Data Representation        : 0–2
   - 0 = Raw prices
   - 1 = % Changes
   - 2 = Trend Summary

2. Preprocess Data            : 0–1
   - 0 = No preprocessing
   - 1 = Preprocessing applied (e.g. normalization, scaling, cleaning)

3. Fundamental Data           : 0–1
   - 0 = Not included
   - 1 = Included (e.g. P/E ratio, revenue growth)

4. Technical Indicators       : 0–1
   - 0 = Not included
   - 1 = Included (e.g. SMA, RSI, MACD, EMA, Bollinger Bands)

5. Macroeconomic Data: 0–1
   - 0 = Not included
   - 1 = Included (e.g. GDP, unemployement, inflation, interest rates)

6. Prediction Architecture    : 0–1
   - 0 = Direct Prediction
   - 1 = Sequence-to-sequence prediction

7. Prediction Duration        : 0–1
   - 0 = Short-term prediction
   - 1 = Long-term prediction

Example:
2 1 1 0 1 0 1

Interpreted as:
- Data Representation        = Trend Summary
- Preprocessing              = Enabled
- Fundamental Data           = Included
- Technical Indicators       = Excluded
- Macroeconomic Data         = Included
- Prediction Architecture    = Direct Prediction
- Prediction Duration        = Long-term

'''
