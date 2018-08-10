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

calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/MLK Data for Khashi.xlsx")
calldata = calldata.iloc[::-1]
save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/MLK Data for Khashi.xlsx", "CrashData",
                calldata)

# # MAIN Calldata 2018 + 2017 #
# calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx",
#                              dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float,'Date': datetime,
#                                      'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
#                                      'Temperature': float, "Temp_Max": float, "Temp_Min": float, 'Dewpoint': float,
#                                      'Event': str, 'Humidity': float, 'Month': int, 'Visibility': float,
#                                      'Conditions': str, "Cloud_Coverage": float, "Precipitation_Type": str,
#                                      "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
#                                      "Precip_Intensity_Time": datetime.time})
#
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
# save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Time Test.xlsx",
#                 "Time", calldata)