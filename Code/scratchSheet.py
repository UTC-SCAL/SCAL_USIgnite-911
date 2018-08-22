import pandas
from datetime import datetime


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")

# A relative temperature variable, the deviation of the mean daily temp from the monthly temp
# This cancels out the seasonal effects
calldata.Date = calldata.Date.astype(str)

daily_temps = []
monthly_avg_temps = []
daily_avg_temp = 0
count = 0
day_num = 1
month_num = 1

for j, value in enumerate(calldata.values[0:25947]):  # covering 2017 only
    doa = calldata.Date.values[j]
    # print("Date is: ", doa)
    yoa = int(doa.split('-')[0])
    # print("Year is: ", yoa)
    moa = int(doa.split('-')[1])
    # print("Month is: ", moa)
    dayoa = int(doa.split('-')[2])
    # print("Day is: ", dayoa)

    if moa == month_num:
        if dayoa == day_num:
            daily_avg_temp += calldata.Temperature.values[j]
            count = count + 1
        else:
            daily_avg_temp = round(daily_avg_temp / count, 2)
            daily_temps.append(daily_avg_temp)
            daily_avg_temp = 0
            count = 0
            day_num = day_num + 1
    else:
        # print("End of month ", month_num, " reached")
        monthly_avg = sum(daily_temps)
        monthly_avg = round(monthly_avg / (day_num - 1), 2)
        monthly_avg_temps.append(monthly_avg)

        month_num = month_num + 1
        # print("moa = ", moa)
        # print("yoa = ", yoa)
        day_num = 1
        daily_avg_temp = 0
        monthly_avg = 0
        daily_temps = []
print("Monthly Averages: ", monthly_avg_temps)
