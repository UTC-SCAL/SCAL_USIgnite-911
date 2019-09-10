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


# This file is only for reading in the columns we need for the weather file
weather_2019= feather.read_dataframe("../Ignore/Weather/2019 Weather.feather")

weather_holder = pandas.DataFrame(columns=weather_2019.columns)
# Set the start and end date for the weather file to be updated
begin = '2019-06-26'
end = '2019-09-05'

dates = pandas.date_range(begin, end)

# Read in the center points file to get the used grid blocks (ORIG_FID) and their lat/longs
centers = pandas.read_csv("../Excel & CSV Sheets/Grid Files/Grid Oriented Layout/CenterPoints Ori Layout.csv")
miss_loc = len(weather_holder)
key = find_cred("darksky")

# print(centers.ORIG_FID.values)
# print(weather_holder)
# exit()

for _, i in enumerate(centers.ORIG_FID.values):
    # This first loop is used to resume the code where it crashes, as sometimes darksky decides to deny us
    # if i < 0:
    #     print("Passing til ", i)
    #     pass
    # else:
    i = int(i)
    print(i)
    row_num = centers.loc[centers['ORIG_FID'] == i].index[0]
    lat = centers.Center_Lat.values[i]
    long = centers.Center_Long.values[i]
    weather_holder = pandas.DataFrame(columns=weather_2019.columns)
    for j in dates:
        j = str(j)
        j = str(j.split(" ")[0])
        year = int(j.split("-")[0])
        month = int(j.split("-")[1])
        day = int(j.split("-")[2])
        t = datetime(year, month, day, 0, 0, 0).isoformat()
        call = key, lat, long
        forecastcall = forecast(*call, time=t)
        hourly_list = [item._data for item in forecastcall.hourly]
        for l, info in enumerate(hourly_list):
            entry = hourly_list[l]
            for d, things in enumerate(hourly_list[l]):
                weather_holder.loc[miss_loc, things] = entry[things]
            weather_holder.loc[miss_loc, "Center_Lat"] = lat
            weather_holder.loc[miss_loc, "Center_Long"] = long
            weather_holder.loc[miss_loc, "ORIG_FID"] = i
            miss_loc += 1
    weather_holder.to_csv("../", index=False, mode='a')

