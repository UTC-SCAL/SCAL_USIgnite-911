import pandas
import os, sys
from datetime import datetime
import pytz


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/TimeFixer.xlsx")
# calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(datetime)
#
# for k, value in enumerate(calldata.values):
#     print(k)
#     if calldata.Precip_Intensity_Time.values[k] == 0:
#         pass
#     else:
#         tz = pytz.timezone('America/New_York')
#         dt = datetime.fromtimestamp(calldata.Precip_Intensity_Time.values[k], tz)
#         calldata.Precip_Intensity_Time.values[k] = dt
#
# calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(str)
#
# for i, value2 in enumerate(calldata.values):
#     x = calldata.Precip_Intensity_Time.values[i]
#     calldata.Precip_Intensity_Time.values[i] = x[11:19]
#
# save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/TimeTester.xlsx",
#                 "Time", calldata)


calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")

header_list = ("Y", 'Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Address', 'City', 'Event', 'Conditions',
               'Hour', 'Temperature', "Temp_Max", "Temp_Min", "Temp_<0", "Temp_0-10", "Temp_10-20", "Temp_20-30",
               "Temp_30-40", "Temp_40+", 'Dewpoint', 'Humidity', 'Month', 'Visibility',"Cloud_Coverage",
               "Precipitation_Type", "Precipitation_Intensity", "Precip_Intensity_Max", "Precip_Intensity_Time",
               "EventBefore", "ConditionBefore")
# Temp_<0 = 14
# Temp_0-10 = 15
# Temp_10-20 = 16
# Temp_20-30 = 17
# Temp_30-40 = 18
# Temp_40+ = 19
calldata.index.name = "Index"
calldata = calldata.reindex(columns=header_list)

calldata.Temperature = calldata.Temperature.astype(float)
# print(calldata.head())
for i, values in enumerate(calldata.values):
    if calldata.Temperature.values[i] < 0:
        calldata.iloc[i, 14] = 1
        calldata.iloc[i, 15] = 0
        calldata.iloc[i, 16] = 0
        calldata.iloc[i, 17] = 0
        calldata.iloc[i, 18] = 0
        calldata.iloc[i, 19] = 0
    elif calldata.Temperature.values[i] >= 0 and calldata.Temperature.values[i] < 10:
        calldata.iloc[i, 15] = 1
        calldata.iloc[i, 14] = 0
        calldata.iloc[i, 16] = 0
        calldata.iloc[i, 17] = 0
        calldata.iloc[i, 18] = 0
        calldata.iloc[i, 19] = 0
    elif calldata.Temperature.values[i] >= 10 and calldata.Temperature.values[i] < 20:
        calldata.iloc[i, 16] = 1
        calldata.iloc[i, 15] = 0
        calldata.iloc[i, 14] = 0
        calldata.iloc[i, 17] = 0
        calldata.iloc[i, 18] = 0
        calldata.iloc[i, 19] = 0
    elif calldata.Temperature.values[i] >= 20 and calldata.Temperature.values[i] < 30:
        calldata.iloc[i, 17] = 1
        calldata.iloc[i, 15] = 0
        calldata.iloc[i, 16] = 0
        calldata.iloc[i, 14] = 0
        calldata.iloc[i, 18] = 0
        calldata.iloc[i, 19] = 0
    elif calldata.Temperature.values[i] >= 30 and calldata.Temperature.values[i] < 40:
        calldata.iloc[i, 18] = 1
        calldata.iloc[i, 15] = 0
        calldata.iloc[i, 16] = 0
        calldata.iloc[i, 17] = 0
        calldata.iloc[i, 14] = 0
        calldata.iloc[i, 19] = 0
    elif calldata.Temperature.values[i] >= 40:
        calldata.iloc[i, 19] = 1
        calldata.iloc[i, 15] = 0
        calldata.iloc[i, 16] = 0
        calldata.iloc[i, 17] = 0
        calldata.iloc[i, 18] = 0
        calldata.iloc[i, 14] = 0

save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Temp Test.xlsx", "Temp",
                calldata)
