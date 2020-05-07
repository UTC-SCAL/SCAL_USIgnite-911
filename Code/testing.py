##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.
import pandas

data = pandas.read_csv("../Jeremy Thesis/Feature Selection Results.csv")
negatives = pandas.read_csv("../Jeremy Thesis/Date Shift/Data/DS Data 50-50 Split.csv")
# print(negatives.columns)
columns = list(data.iloc[:0])
columns = list(map(str, columns))
print(columns)
negatives = negatives.reindex(columns=columns[1:])
print(negatives.columns)
