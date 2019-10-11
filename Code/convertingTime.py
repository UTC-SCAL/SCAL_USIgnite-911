import pandas
from datetime import datetime
# import feather

# Method to convert the variable Precipitation Time to a unix timestamp
def convertPrecipTime(calldata):
    # Cast the column as a string
    calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(str)

    ##Loop Converts each item within Precip Intensity Time to Unix time. 
    for i, value in enumerate(calldata.values):
        ts = int(calldata.Precip_Intensity_Time.values[i])
        string_time = str(datetime.utcfromtimestamp(ts).strftime('%H:%M:%S'))
        calldata.Precip_Intensity_Time.values[i] = string_time

    calldata.to_csv("../", index=False)

# Method to convert a standard timestamp to a unix timestamp
# Format of standard time used: month/day/year
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
        print(yoa, moa, dayoa, hoa, mioa, soa)
        date = datetime(yoa, moa, dayoa, hoa, mioa, soa)
        print(date)
        unixtime = date.strftime('%s')
        calldata.Unix.values[k] = unixtime
    return calldata

# Method to convert standard timestamp to a unix timestamp
# Format of standard time used: year-month-day
def unixFromStandardAlt(calldata):

    ##This section takes in the standard time column and creates Unix time.
    for k, info in enumerate(calldata.values):
        print(k)
        # All variables are blank-of-accident, thus year is yoa.
        hoa = int(calldata.Hour.values[k])
        toa = calldata.Time.values[k]
        mioa = int(toa.split(':')[1])
        soa = int(toa.split(':')[2])
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

# Method to convert Unix timestamp to standard time stamp
def standardFromUnix(data):
    # Cast the column as a string
    # Depending on the column names, use one of the following conversions, because Pete doesn't like consistency
    # data.Unix = data.Unix.astype(str)
    data.time = data.time.astype(str)

    ##Loop Converts each item within Precip Intensity Time to Unix time.
    for i, value in enumerate(data.values):
        unix = int(data.time.values[i])
        readTime = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        data.timereadable.values[i] = readTime.split(" ")[1]
        data.Date.values[i] = readTime.split(" ")[0]

    return data

# This is a version of getting unix timestamp for windows matching, which Jeremy uses when he works from home
def getUnixTimeWindows(calldata):
    calldata.Hour = calldata.Hour.astype(str)
    calldata.Date = calldata.Date.astype(str)
    # Combine the hour and date column into a certain format for conversion
    calldata['Unix'] = calldata.apply(lambda x: pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
    # Convert the combined column values to unix values
    calldata['Unix'] = calldata.apply(lambda x: x.Unix.timestamp(), axis=1)

    return calldata

# Method for splitting the Time column into separate date and hour columns
# Example format of Time variable: 2018-3-5 12:13:45
# It won't always be in that exact format, but that's the general format used in this method
def splitTime(data):
    data['Hour'] = 0
    for i, value in enumerate(data.values):
        print(i)
        data.Hour.values[i] = (data.time[i]).split(" ")[1].split(":")[0]
        data.Date.values[i] = (data.time[i]).split(" ")[0]
    return data


