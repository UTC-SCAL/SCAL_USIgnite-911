##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.
import feather
import pandas

data = feather.read_dataframe("../Ignore/Weather/2019 Weather Updated.feather")
print(data.columns)

print(data.time.values[len(data)-2])
