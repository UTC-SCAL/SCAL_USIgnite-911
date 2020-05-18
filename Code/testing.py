# This file is kept empty for testing small chunks of code easily.
# Please clear this file when you are done working on the code, and put it into whatever file it needs to go in.
import pandas

data = pandas.read_csv("../Jeremy Thesis/RawAccidentData.csv")
data.Hour = data.Hour.astype(str)
data.Date = data.Date.astype(str)
for i, values in enumerate(data.values):
    print(i)
    data.Hour.values[i] = data['Response Date'].values[i].split(" ")[1].split(":")[0]
    data.Date.values[i] = data['Response Date'].values[i].split(" ")[0]
data.to_csv("../Jeremy Thesis/RawAccidentData Formatted.csv")
