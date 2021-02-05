"""
Authors: Jeremy Roland and Pete Way
Purpose: A one stop shop of methods Pete and Jeremy used that all relate to working with time variables
"""

import pandas
from datetime import datetime


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
        # toa = calldata.Time.values[k]
        # mioa = int(toa.split(':')[1])
        # soa = int(toa.split(':')[2])
        doa = calldata.Date.values[k]
        yoa = int(doa.split('/')[2])
        moa = int(doa.split('/')[0])
        dayoa = int(doa.split('/')[1])
        print(yoa, moa, dayoa, hoa, 0, 0)
        date = datetime(yoa, moa, dayoa, hoa, 0, 0)
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
# Windows machines need this version, because Windows sucks when working with code
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
    for i, _ in enumerate(data.values):
        print(i)
        data.Hour.values[i] = (data.Date[i]).split(" ")[1].split(":")[0]
        data.Date.values[i] = (data.Date[i]).split(" ")[0]
    return data


# Method for creating the DayFrame variable from the provided hour
def finding_Dayframe(data):
    data['DayFrame'] = 0
    for i, value in enumerate(data.values):
        if 0 <= data.Hour.values[i] <= 4 or 19 <= data.Hour.values[i] <= 23:
            data.DayFrame.values[i] = 1
        elif 5 <= data.Hour.values[i] <= 9:
            data.DayFrame.values[i] = 2
        elif 10 <= data.Hour.values[i] <= 13:
            data.DayFrame.values[i] = 3
        elif 14 <= data.Hour.values[i] <= 18:
            data.DayFrame.values[i] = 4
    return data


# This is an older method we used when we were thinking of including holiday as a variable
# This expects you to have a file that has the dates of the year that are holidays
def finding_holidays(data, holidays):
    data.Date = data.Date.astype(str)
    holidays.Dates = holidays.Dates.astype(str)
    for i, value in enumerate(data.values):
        print(i)
        # Set the default values for an entry to being a weekday, and it's only changed if the day
        # is a travel day or a weekend
        for j, value2 in enumerate(holidays.values):
            data.TravelDay.values[i] = 0
            data.WeekEnd.values[i] = 0
            data.WeekDay.values[i] = 1
            if data.Date.values[i] == holidays.Dates.values[j]:
                data.TravelDay.values[i] = 1
                data.WeekEnd.values[i] = 0
                data.WeekDay.values[i] = 0
                break
            elif data.Weekday.values[i] == 5 or data.Weekday.values[i] == 6:
                data.TravelDay.values[i] = 0
                data.WeekEnd.values[i] = 1
                data.WeekDay.values[i] = 0
                break
            else:
                pass
    return data


def finding_weekdays(data):
    """
    Quick, simple program that gets the day of the week value and the weekday value for our data
    DayOfWeek is 0-6, 0 = Monday, 6 = Sunday
    WeekDay is a binary representation of DayOfWeek, where WeekDay = 1 means DayOfWeek is between 0 and 4
    """
    data.Date = data.Date.astype(str)
    for i, value in enumerate(data.values):
        print(i)
        year = int(data.Date.values[i].split("-")[0])
        month = int(data.Date.values[i].split("-")[1])
        day = int(data.Date.values[i].split("-")[2])
        thisDate = datetime.date(year, month, day)
        data.DayOfWeek.values[i] = thisDate.weekday()
        if thisDate.weekday() >= 5:
            data.WeekDay.values[i] = 0
        else:
            data.WeekDay.values[i] = 1
    return data


def formatRawData(data):
    """
    Method for formatting the raw data taken from emails
    """
    columns = ['Address', 'City', 'Latitude', 'Longitude', 'Date', 'Unix', 'Hour', 'DayFrame', 'Grid_Num', 'DayOfWeek',
               'WeekDay']
    data['Date'] = data['Response Date'].astype(str)
    data['Unix'] = 0
    data['WeekDay'] = 0
    data['DayOfWeek'] = 0
    data['DayFrame'] = 0
    # First, split the date time into date and hour
    data = splitTime(data)
    # Then, get dayframe and unix
    data = finding_Dayframe(data)
    data = unixFromStandard(data)
    data = data.reindex(columns=columns)
    data.Latitude = data.Latitude/1000000
    data.Longitude = data.Longitude/-1000000
    for i, values in enumerate(data.values):
        timestamp = str(data.Date.values[i]) + " " + str(data.Hour.values[i])
        # A try/except statement for taking in what format the date is in, because 911 are buttheads
        try:
            thisDate = datetime.strptime(timestamp, "%m/%d/%Y %H")
        except:
            thisDate = datetime.strptime(timestamp, "%m/%d/%y %H")
        data.DayOfWeek.values[i] = thisDate.weekday()
    data.WeekDay = data.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    data.DayFrame = data.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23
    else (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    data.to_csv("../", index=False)

