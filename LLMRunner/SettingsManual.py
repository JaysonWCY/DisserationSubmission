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


3. Technical Indicators       : 0–1
   - 0 = Not included
   - 1 = Included (e.g. SMA, RSI, MACD, EMA, Bollinger Bands)

   
4. Prediction Duration        : 0–1
   - 0 = Short-term prediction
   - 1 = Long-term prediction

Dont talk about prediction architecture

Example:
2 1 0 1

Interpreted as:
- Data Representation        = Trend Summary
- Preprocessing              = Enabled
- Technical Indicators       = Excluded
- Prediction Duration        = Long-term

'''
