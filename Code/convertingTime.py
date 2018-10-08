import pandas
from datetime import datetime


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()

calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg.xlsx")

# Cast the column as a string
calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(str)

for i, value in enumerate(calldata.values):
    ts = int(calldata.Precip_Intensity_Time.values[i])
    string_time = str(datetime.utcfromtimestamp(ts).strftime('%H:%M:%S'))
    calldata.Precip_Intensity_Time.values[i] = string_time

save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg.xlsx", "Time is Dumb", calldata)