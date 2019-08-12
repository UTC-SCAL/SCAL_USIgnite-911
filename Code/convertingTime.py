import pandas
from datetime import datetime

# calldata = pandas.read_csv("", sep=",")


def convertPrecipTime():
    # Cast the column as a string
    calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(str)

    ##Loop Converts each item within Precip Intensity Time to Unix time. 
    for i, value in enumerate(calldata.values):
        ts = int(calldata.Precip_Intensity_Time.values[i])
        string_time = str(datetime.utcfromtimestamp(ts).strftime('%H:%M:%S'))
        calldata.Precip_Intensity_Time.values[i] = string_time

    calldata.to_csv("../", index=False)

def unixFromStandard(calldata):

    ##This section takes in the standard time column and creates Unix time. 
    for k, info in enumerate(calldata.values):
        print(k)
        # All variables are blank-of-accident, thus year is yoa.
        hoa = int(calldata.Hour.values[k])
        toa = calldata.Time.values[k]
        mioa = int(toa.split(':')[1])
        soa = int(toa.split(':')[2])
        doa = calldata.Date.values[k]
        yoa = int(doa.split('/')[2])+2000
        moa = int(doa.split('/')[0])
        dayoa = int(doa.split('/')[1])
        # print(yoa, moa, dayoa, hoa, mioa, soa)
        date = datetime(yoa, moa, dayoa, hoa, mioa, soa)
        # print(date)
        unixtime = date.strftime('%s')
        # print(unixtime)
        calldata.Unix.values[k] = unixtime
    return calldata

# data = pandas.read_csv("../Excel & CSV Sheets/2017+2018 Data/2017+2018 Accidents.csv",sep=",")
# data['time'] = data.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
# # This actually makes the column
# data['time'] = data.apply(lambda x : x.time.strftime('%s'), axis=1)
# data.to_csv("../Excel & CSV Sheets/2017+2018 Data/2017+2018 Accidents.csv")