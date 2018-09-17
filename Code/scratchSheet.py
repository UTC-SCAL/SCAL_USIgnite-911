import pandas
from datetime import datetime
from darksky import forecast

def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")

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
    # else:
    #     # print("End of month ", month_num, " reached")
    #     monthly_avg = sum(daily_temps)
    #     monthly_avg = round(monthly_avg / (day_num - 1), 2)
    #     monthly_avg_temps.append(monthly_avg)
    #
    #     month_num = month_num + 1
    #     # print("moa = ", moa)
    #     # print("yoa = ", yoa)
    #     day_num = 1
    #     daily_avg_temp = 0
    #     monthly_avg = 0
    #     daily_temps = []
# print("Monthly Averages: ", monthly_avg_temps)

key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'

print("Adding in DarkSky Weather")
# Iterate through calldata and assign weather data for each incident
for k, info in enumerate(calldata.values):
    print(k)
    # All variables are blank-of-accident, thus year is yoa.
    hoa = int(calldata.Hour.values[k])
    toa = calldata.Time.values[k]
    mioa = int(toa.split(':')[1])
    soa = int(toa.split(':')[2])
    doa = calldata.Date.values[k]
    yoa = int(doa.split('-')[0])
    moa = int(doa.split('-')[1])
    dayoa = int(doa.split('-')[2])
    lat = calldata.Latitude.values[k]
    long = calldata.Longitude.values[k]

    # The following line needs to have this format:
    t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
    call = key, lat, long

    # Retrieve the previous hour's weather event and conditions for each incident
    # A series of if statements to see what day of the year it is
    # If it is the first of the month, then we call the weather data for the last day of the previous month
    if hoa == 0 and dayoa == 1:  # If 1/1, get weather data from 12/31, reduce year by 1
        if moa == 1:
            new_hoa = 23
            new_dayoa = 31
            new_moa = 12
            new_yoa = yoa - 1
            # Get weather data
            # The following line needs to have this format:
            t = datetime(new_yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 2:  # If 2/1, get weather data from 1/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 1
            # Get weather data
            # The following line needs to have this format:
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 3:  # If 3/1, get weather data from 2/28, same year
            new_hoa = 23
            new_dayoa = 28
            new_moa = 2
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 4:  # If 4/1, get weather data from 3/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 3
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 5:  # If 5/1, get weather data from 4/30, same year
            new_hoa = 23
            new_dayoa = 30
            new_moa = 4
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 6:  # If 6/1, get weather data from 5/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 5
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 7:  # If 7/1, get weather data from 6/30, same year
            new_hoa = 23
            new_dayoa = 30
            new_moa = 6
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 8:  # If 8/1, get weather data from 7/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 7
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 9:  # If 9/1, get weather data from 8/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 8
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 10:  # If 10/1, get weather data from 9/30, same year
            new_hoa = 23
            new_dayoa = 30
            new_moa = 9
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 11:  # If 11/1, get weather data from 10/31, same year
            new_hoa = 23
            new_dayoa = 31
            new_moa = 10
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif moa == 12:  # If 12/1, get weather data from 11/30, same year
            new_hoa = 23
            new_dayoa = 30
            new_moa = 11
            # Get weather data
            t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        else:
            print("Error in calculating previous day")
    elif hoa == 0 and dayoa != 1:
        new_dayoa = dayoa - 1
        new_hoa = 23
        # Get weather data
        t = datetime(yoa, moa, new_dayoa, new_hoa, mioa, soa).isoformat()
        call = key, lat, long
        try:
            forecastcall = forecast(*call, time=t)
            for i, value in enumerate(forecastcall.hourly):
                calldata.EventBefore.values[k] = value.icon
                calldata.ConditionBefore.values[k] = value.summary
        except:
            print("Error in finding previous hour")
    elif hoa > 0:
        new_hoa = hoa - 1
        # Get weather data
        t = datetime(yoa, moa, dayoa, new_hoa, mioa, soa).isoformat()
        call = key, lat, long
        try:
            forecastcall = forecast(*call, time=t)
            for i, value in enumerate(forecastcall.hourly):
                calldata.EventBefore.values[k] = value.icon
                calldata.ConditionBefore.values[k] = value.summary
        except:
            print("Error in finding previous hour")
    else:
        print("One of the hours was 0 and didn't register")