import pandas
import os, sys

path = os.path.dirname(sys.argv[0])

calldata = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")

rainday = calldata.Date.values[0]

