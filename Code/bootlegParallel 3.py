import pandas
import os, sys
from datetime import datetime
from darksky import forecast

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def find_cred(service):
    file = "../Excel & CSV Sheets/login.csv"
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


blocks = pandas.read_csv(
    "../Excel & CSV Sheets/2019 Data/2019 Weather Dates.csv")
centers = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/CenterPoints Ori Layout.csv")
weather_holder = pandas.read_csv(
    "../Excel & CSV Sheets/2019 Data/2019 Weather Dates 3.csv")
miss_loc = 0
key = find_cred("darksky")
for stuff, i in enumerate(blocks.columns.values):
    # print(i)
    i = int(i)
    if 906 > i >= 617:
        print(i)
        values = blocks[str(i)].values
        values = values[pandas.notna(values)]
        row_num = centers.loc[centers['ORIG_FID'] == i].index[0]
        lat = centers.Center_Lat.values[row_num]
        long = centers.Center_Long.values[row_num]
        # print(values)
        for j in values:
            if j == " ":
                break
            else:
                year = int(j.split("-")[0])
                month = int(j.split("-")[1])
                day = int(j.split("-")[2])
                print(year, month, day)
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

        weather_holder.to_csv \
            ("../Excel & CSV Sheets/2019 Data/2019 Weather Dates3 Part 2.csv",
             index=False)
weather_holder.to_csv \
    ("../Excel & CSV Sheets/2019 Data/2019 Weather Dates3 Part 2.csv", index=False)