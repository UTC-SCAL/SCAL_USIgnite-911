import pandas
from datetime import datetime
import feather

# calldata = pandas.read_csv("", sep=",")


def convertPrecipTime(calldata):
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
        yoa = int(doa.split('/')[2])
        moa = int(doa.split('/')[0])
        dayoa = int(doa.split('/')[1])
        # print(yoa, moa, dayoa, hoa, mioa, soa)
        date = datetime(yoa, moa, dayoa, hoa, mioa, soa)
        # print(date)
        unixtime = date.strftime('%s')
        # print(unixtime)
        calldata.Unix.values[k] = unixtime
    return calldata

def unixFromStandardAlt(calldata):

    ##This section takes in the standard time column and creates Unix time.
    for k, info in enumerate(calldata.values):
        print(k)
        # All variables are blank-of-accident, thus year is yoa.
        hoa = int(calldata.Hour.values[k])
        mioa = 0
        soa = 0
        doa = calldata.Date.values[k]
        yoa = int(doa.split('-')[0])
        moa = int(doa.split('-')[1])
        dayoa = int(doa.split('-')[2])
        # print(yoa, moa, dayoa, hoa, mioa, soa)
        date = datetime(yoa, moa, dayoa, hoa, mioa, soa)
        # print(date)
        unixtime = date.strftime('%s')
        calldata.Unix.values[k] = unixtime
    return calldata

def standardFromUnix(data):
    # Cast the column as a string
    data.time = data.time.astype(str)

    ##Loop Converts each item within Precip Intensity Time to Unix time.
    for i, value in enumerate(data.values):
        unix = int(data.time.values[i])
        readTime = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        data.timereadable.values[i] = readTime.split(" ")[1]
        data.Date.values[i] = readTime.split(" ")[0]

    return data

# data = pandas.read_csv("../Ignore/Weather/2019 Weather Updated.csv",sep=",")
# standardFromUnix(data)
# data['time'] = data.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
# # This actually makes the column
# data['time'] = data.apply(lambda x : x.time.strftime('%s'), axis=1)
# data.to_csv("../Excel & CSV Sheets/2017+2018 Data/2017+2018 Accidents.csv")

# Splitting time column into date and hour #
# weather = feather.read_dataframe("../Ignore/Weather/2017+2018 Weather Full.feather")
# weather['Hour'] = 0
# for i, value in enumerate(weather.values):
#     print(i)
#     weather.Hour.values[i] = (weather.time[i]).split(" ")[1].split(":")[0]
#     weather.Date.values[i] = (weather.time[i]).split(" ")[0]
# feather.write_dataframe(weather, "../Ignore/Weather/2017+2018 Weather Stage 1.feather")

# Creating the unix column #
weather = feather.read_dataframe("../Ignore/Weather/2017+2018 Weather Stage 1.feather")
weather['Unix'] = 0
new_weather = unixFromStandardAlt(weather)
feather.write_dataframe(new_weather, "../Ignore/Weather/2017+2018 Weather Stage 2.feather")