import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
import feather


def find_cred(service):
    file = "../Ignore/login.csv"
    if os.path.exists(file):
        with open(file, "r") as file:
            lines = file.readlines()
            if service in lines[0]:
                cred = lines[0].split(",")[1]
                # print(cred)
            if service in lines[1]:
                cred = str(lines[1].split(",")[1]) + "," + str(lines[1].split(",")[2])
                # print(cred)
                    # logins[username] = password
    return cred


header_list = ('X', 'Center_Lat', 'Center_Long', 'ORIG_FID', 'apparentTemperature', 'cloudCover', 'dewPoint', 'humidity',
               'icon', 'ozone', 'precipAccumulation', 'precipIntensity', 'precipProbability', 'precipType', 'pressure',
               'summary', 'temperature', 'time', 'Date', 'timereadable', 'uvIndex', 'visibility', 'windBearing',
               'windGust', 'windSpeed', 'Event', 'Conditions', 'EventBefore', 'ConditionBefore', 'hourbefore',
               'Grid_Block')
weather_holder = feather.read_dataframe("../Ignore/Weather/2019 Weather.feather")
begin = '2019-01-01'
end = '2019-09-05'
dates = pandas.date_range(begin, end)

centers = pandas.read_csv("../Excel & CSV Sheets/Grid Files/Grid Oriented Layout/CenterPoints Ori Layout.csv")
miss_loc = len(weather_holder)
key = find_cred("darksky")
for _, i in enumerate(centers.ORIG_FID.values):
    i = int(i)
    print(i)
    # row_num = centers.loc[centers['ORIG_FID'] == i].index[0]
    lat = centers.Center_Lat.values[i]
    long = centers.Center_Long.values[i]
    # print(values)
    for j in dates:
        j = str(j)
        # print(j)
        # exit()
        # year = int(j.split("-")[0])
        # month = int(j.split("-")[1])
        # day = int(j.split("-")[2])
        # print(year, month, day)
        t = datetime(j).isoformat()
        print(t)
        exit()
        call = key, lat, long
        forecastcall = forecast(*call, time=j)
        hourly_list = [item._data for item in forecastcall.hourly]
        print(hourly_list)
        exit()
        for l, info in enumerate(hourly_list):
            entry = hourly_list[l]
            for d, things in enumerate(hourly_list[l]):
                weather_holder.loc[miss_loc, things] = entry[things]
            weather_holder.loc[miss_loc, "Center_Lat"] = lat
            weather_holder.loc[miss_loc, "Center_Long"] = long
            weather_holder.loc[miss_loc, "ORIG_FID"] = i
            miss_loc += 1
    weather_holder.to_csv \
        ("../Excel & CSV Sheets/2019 Data/2019 Weather Dates 1.csv",
         index=False)

weather_holder.to_csv \
    ("../Excel & CSV Sheets/2019 Data/2019 Weather Dates 1.csv", index=False)