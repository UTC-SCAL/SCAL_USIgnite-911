import pandas
from datetime import datetime
from darksky import forecast
import pandas
from datetime import datetime
from darksky import forecast
import os, sys
import random
from datetime import datetime, timedelta, date, time


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")

# A relative temperature variable, the deviation of the mean daily temp from the monthly temp
# This cancels out the seasonal effects
# calldata.Date = calldata.Date.astype(str)
#
# daily_temps = []
# monthly_avg_temps = []
# daily_avg_temp = 0
# count = 0
# day_num = 1
# month_num = 1

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


# Finding the daily average temmperatures #
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
