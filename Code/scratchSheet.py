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


# def update_temp_avgs(day_holder2018):
#         lat_coords = [35.421081, 35.153381, 35.006039, 35.150392, 35.301703, 35.185536]
#         long_coords = [-85.121603, -85.121603, -85.175549, -85.047341, -84.998361, -85.158404]
#         hour_times = [0, 6, 12, 18]
#         coord_avgs = []
#         # The key for using DarkSky API
#         key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
#         day_holder2018.Date = day_holder2018.Date.astype(str)
#
#         print("Adding in DarkSky Weather")
#         # Iterate through calldata and assign weather data for each incident
#         for k, info in enumerate(day_holder2018.values):
#             print(k)
#             if day_holder2018.Daily_Average.values[k] > -100:
#                 print("Skipping")
#             else:
#                 lat_iterator = 0
#                 hour_iterator = 0
#                 temp_avg = 0
#                 for j in range(0, 6):
#                     lat = lat_coords[lat_iterator]
#                     long = long_coords[lat_iterator]
#                     temp_avg = 0
#                     hour_iterator = 0
#                     for o in range(0, 4):
#                         hoa = hour_times[hour_iterator]
#                         mioa = 0
#                         soa = 0
#                         doa = day_holder2018.Date.values[k]
#                         yoa = int(doa.split('-')[0])
#                         moa = int(doa.split('-')[1])
#                         dayoa = int(doa.split('-')[2])
#                         # The following line needs to have this format:
#                         t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
#                         call = key, lat, long
#                         try:
#                             forecastcall = forecast(*call, time=t)
#                             # Hourly data
#                             for i, value in enumerate(forecastcall.hourly):
#                                 if i == hoa:
#                                     temp_avg = temp_avg + value.temperature
#                         except:
#                             print("Hourly Lookup Failed")
#                         hour_iterator = hour_iterator + 1
#                     lat_iterator = lat_iterator + 1
#                     temp_avg = temp_avg / 4
#                     coord_avgs.append(temp_avg)
#                     day_average = sum(coord_avgs) / len(coord_avgs)
#                     day_holder2018.Daily_Average.values[k] = day_average
#         day_holder2018.to_excel(
#             "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/2017+2018 Data/Day Holder 20182.xlsx",
#             "Time and Temp")
#
# calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")
#
# # A relative temperature variable, the deviation of the mean daily temp from the monthly temp
# # This cancels out the seasonal effects
# calldata.Date = calldata.Date.astype(str)
#
# daily_temps = []
# monthly_avg_temps = []
# daily_avg_temp = 0
# count = 0
# day_num = 1
# month_num = 1
#
# for j, value in enumerate(calldata.values[0:25947]):  # covering 2017 only
#     doa = calldata.Date.values[j]
#     # print("Date is: ", doa)
#     yoa = int(doa.split('-')[0])
#     # print("Year is: ", yoa)
#     moa = int(doa.split('-')[1])
#     # print("Month is: ", moa)
#     dayoa = int(doa.split('-')[2])
#     # print("Day is: ", dayoa)
#
#     if moa == month_num:
#         if dayoa == day_num:
#             daily_avg_temp += calldata.Temperature.values[j]
#             count = count + 1
#         else:
#             daily_avg_temp = round(daily_avg_temp / count, 2)
#             daily_temps.append(daily_avg_temp)
#             daily_avg_temp = 0
#             count = 0
#             day_num = day_num + 1
#     else:
#         # print("End of month ", month_num, " reached")
#         monthly_avg = sum(daily_temps)
#         monthly_avg = round(monthly_avg / (day_num - 1), 2)
#         monthly_avg_temps.append(monthly_avg)
#
#         month_num = month_num + 1
#         # print("moa = ", moa)
#         # print("yoa = ", yoa)
#         day_num = 1
#         daily_avg_temp = 0
#         monthly_avg = 0
#         daily_temps = []
# print("Monthly Averages: ", monthly_avg_temps)
#
#
# # Finding the daily average temmperatures
# timedata_2017 = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/Day Holder 2017.xlsx")
# timedata_2018 = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx")
#
# lat_coords = [35.421081, 35.153381, 35.006039, 35.150392, 35.301703, 35.185536]
# long_coords = [-85.121603, -85.121603, -85.175549, -85.047341, -84.998361, -85.158404]
# hour_times = [0, 6, 12, 18]
# coord_avgs = []
# # The key for using DarkSky API
# key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
# timedata_2018.Date = timedata_2018.Date.astype(str)
#
# print("Adding in DarkSky Weather")
# # Iterate through calldata and assign weather data for each incident
# for k, info in enumerate(timedata_2018.values):
#     print(k)
#     lat_iterator = 0
#     hour_iterator = 0
#     temp_avg = 0
#     for j in range(0, 6):
#         lat = lat_coords[lat_iterator]
#         long = long_coords[lat_iterator]
#         temp_avg = 0
#         hour_iterator = 0
#         for o in range(0, 4):
#             hoa = hour_times[hour_iterator]
#             mioa = 0
#             soa = 0
#             doa = timedata_2018.Date.values[k]
#             yoa = int(doa.split('-')[0])
#             moa = int(doa.split('-')[1])
#             dayoa = int(doa.split('-')[2])
#             # The following line needs to have this format:
#             t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
#             call = key, lat, long
#             try:
#                 forecastcall = forecast(*call, time=t)
#                 # Hourly data
#                 for i, value in enumerate(forecastcall.hourly):
#                     if i == hoa:
#                         temp_avg = temp_avg + value.temperature
#             except:
#                 print("Hourly Lookup Failed")
#             hour_iterator = hour_iterator + 1
#         lat_iterator = lat_iterator + 1
#         temp_avg = temp_avg / 4
#         coord_avgs.append(temp_avg)
#         day_average = sum(coord_avgs) / len(coord_avgs)
#     timedata_2018.Daily_Average.values[k] = day_average
# save_excel_file("",
#                 "Time and Temp", timedata_2018)

# Code for aggregating data and converting them into numerical forms for modelling #


# dayHolder_2017 = pandas.read_excel("/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/2017+2018 Data/Day Holder 2017.xlsx")
# dayHolder_2018 = pandas.read_excel("/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx")
# dayHolder_2017.Date = dayHolder_2017.Date.astype(str)
# dayHolder_2018.Date = dayHolder_2018.Date.astype(str)
# calldata.Date = calldata.Date.astype(str)
# print("Starting Temp Matching")
# for k, value2 in enumerate(calldata.values):
#     print(k)
#     doa = calldata.Date.values[k]
#     moa = int(doa.split('-')[1])
#     yoa = int(doa.split('-')[0])
#     if yoa == 2017:
#         for o, value3 in enumerate(dayHolder_2017.values):
#             dh_doa = dayHolder_2017.Date.values[o]
#             dh_moa = int(dh_doa.split('-')[1])
#             if calldata.Date.values[k] == dayHolder_2017.Date.values[o]:
#                 calldata.Daily_Avg_Temp.values[k] = dayHolder_2017.Daily_Average.values[o]
#             if moa == dh_moa:
#                 calldata.Monthly_Avg_Temp.values[k] = dayHolder_2017.Monthly_Average.values[o]
#     elif yoa == 2018:
#         for a, value4 in enumerate(dayHolder_2018.values):
#             dh_doa = dayHolder_2018.Date.values[a]
#             dh_moa = int(dh_doa.split('-')[1])
#             if calldata.Date.values[k] == dayHolder_2018.Date.values[a]:
#                 calldata.Daily_Avg_Temp.values[k] = dayHolder_2018.Daily_Average.values[a]
#             if moa == dh_moa:
#                 calldata.Monthly_Avg_Temp.values[k] = dayHolder_2018.Monthly_Average.values[a]
#
# print("Relative Temps")
# for h, value6 in enumerate(calldata.values):
#     calldata.Relative_Temp.values[h] = abs(calldata.Daily_Avg_Temp.values[h] - calldata.Monthly_Avg_Temp.values[h])
#
#
# day_holder2019 = pandas.read_excel("/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/Day Holder 2019.xlsx")
#
# day_holder2019.Date = day_holder2019.Date.astype(str)
#
# print(len(day_holder2019.Date))

# dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data.csv")
# holidays = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/HolidayList.csv")
# dataset.Date = dataset.Date.astype(str)
# holidays.Dates = holidays.Dates.astype(str)
# for i, value in enumerate(dataset.values):
#     print(i)
#     for j, value2 in enumerate(holidays.values):
#         dataset.TravelDay.values[i] = 0
#         dataset.WeekEnd.values[i] = 0
#         dataset.WeekDay.values[i] = 1
#         if dataset.Date.values[i] == holidays.Dates.values[j]:
#             dataset.TravelDay.values[i] = 1
#             dataset.WeekEnd.values[i] = 0
#             dataset.WeekDay.values[i] = 0
#             break
#         elif dataset.Weekday.values[i] == 5 or dataset.Weekday.values[i] == 6:
#             dataset.TravelDay.values[i] = 0
#             dataset.WeekEnd.values[i] = 1
#             dataset.WeekDay.values[i] = 0
#             break
#         else:
#             pass
# dataset.to_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2.csv")

missingblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/Date-Finder-output S1.csv")
centers = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/CenterPoints Ori Layout.csv")
missing_weather = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/MissingHourWeather S1.csv")
miss_loc = 0
key = find_cred("darksky")
for stuff, i in enumerate(missingblocks.columns.values):
    i = int(i)
    if i > 66:
        print(i)
        values = missingblocks[str(i)].values
        values = values[pandas.notna(values)]
        row_num = centers.loc[centers['ORIG_FID'] == i].index[0]
        lat = centers.Center_Lat.values[row_num]
        long = centers.Center_Long.values[row_num]
        # print(values)
        for j in values:
            if j == " ":
                break
            else:
                year = int(j.split("/")[2])+2000
                month = int(j.split("/")[0])
                day = int(j.split("/")[1])
                t = datetime(year, month, day, 0, 0, 0).isoformat()
                call = key, lat, long
                forecastcall = forecast(*call, time=t)
                hourly_list = [item._data for item in forecastcall.hourly]
                for l, info in enumerate(hourly_list):
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        missing_weather.loc[miss_loc, things] = entry[things]
                    missing_weather.loc[miss_loc, "Center_Lat"] = lat
                    missing_weather.loc[miss_loc, "Center_Long"] = long
                    missing_weather.loc[miss_loc, "ORIG_FID"] = i
                    miss_loc += 1
        missing_weather.to_csv\
            ("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/MissingHourWeather S1_Part2.csv", index=False)

missing_weather.to_csv\
    ("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/MissingHourWeather S1_Part2.csv", index=False)