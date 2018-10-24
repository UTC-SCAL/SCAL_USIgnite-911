import pandas
from datetime import datetime

calldata = pandas.read_csv("", sep=",")

# Cast the column as a string
calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(str)

for i, value in enumerate(calldata.values):
    ts = int(calldata.Precip_Intensity_Time.values[i])
    string_time = str(datetime.utcfromtimestamp(ts).strftime('%H:%M:%S'))
    calldata.Precip_Intensity_Time.values[i] = string_time

calldata.to_csv(
        "")