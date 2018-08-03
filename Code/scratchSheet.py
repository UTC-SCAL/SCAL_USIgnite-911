import pandas
import os, sys
from datetime import datetime

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


# MAIN Calldata 2018 + 2017 #
calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Accident Report List.xlsx",
    dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
            'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
            'Temperature': float, 'Dewpoint': float, 'Event': str, 'Humidity': float, 'Month': int,
            'Visibility': float, 'Conditions': str})

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
