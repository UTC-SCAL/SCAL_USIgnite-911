import pandas
from datetime import datetime
from darksky import forecast


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()

calldata = \
    pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Daily Testing.xlsx",
                      dtypes={"Index": int, 'Date': datetime, 'Time': datetime.time,'Event': str,'Conditions': str,
                              "EventBefore": str, "ConditionBefore": str, 'Hour': int, 'Temperature': float,
                              "Temp_Max": float, "Temp_Min": float, "Monthly_Avg_Temp": float, "Temp_Below_0": int,
                              "Temp_0to10": int, "Temp_10to20": int, "Temp_20to30": int, "Temp_30to40": int,
                              "Temp_40to50": int, "Temp_50to60": int, "Temp_60to70": int, "Temp_Above_70": int,
                              "Daily_Avg_Temp": str, 'Humidity': float, 'Visibility': float,  "Cloud_Coverage": float,
                              "Precipitation_Type": str, "Precipitation_Intensity": float,
                              "Precip_Intensity_Max": float, "Precip_Intensity_Time": float})


key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'

print("Adding in DarkSky Weather")
calldata.Time = calldata.Time.astype(str)
calldata.Date = calldata.Date.astype(str)
# Iterate through calldata and assign weather data for each incident
for k, info in enumerate(calldata.values):
    print(k)
    # https://www.google.com/maps/place/Hamilton+County,+TN/@35.2207697,-85.4892699,10z/data=!4m5!3m4!1s0x8860973d964305bb:0xe62e089be673cfe!8m2!3d35.1618966!4d-85.1479364

save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Daily Testing2.xlsx", "Dark",
                calldata)
# print(calldata.head())
