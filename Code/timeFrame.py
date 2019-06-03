import pandas
import os, sys

path = os.path.dirname(sys.argv[0])

calldata = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")

for i, value in enumerate(calldata.values):
    if 0 <= calldata.Hour.values[i] <= 4 or 18 <= calldata.Hour.values[i] <= 23:
        calldata.DayFrame.values[i] = 1
    elif 5 <= calldata.Hour.values[i] <= 9:
        calldata.DayFrame.values[i] = 2
    elif 10 <= calldata.Hour.values[i] <= 12:
        calldata.DayFrame.values[i] = 3
    elif 13 <= calldata.Hour.values[i] <= 17:
        calldata.DayFrame.values[i] = 4
calldata.to_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")