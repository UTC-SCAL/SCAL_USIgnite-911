import pandas
from datetime import datetime
from darksky import forecast
import pandas
from datetime import datetime
from darksky import forecast
import os, sys
import random
import pytz
from datetime import datetime, timedelta, date, time


def add_data(calldata):
    # Caste the columns into the data types we need them to be
    calldata.Event = calldata.Event.astype(str)
    calldata.Conditions = calldata.Conditions.astype(str)
    calldata.Precipitation_Type = calldata.Precipitation_Type.astype(str)
    calldata.Precipitation_Intensity = calldata.Precipitation_Intensity.astype(float)
    calldata.Precip_Intensity_Max = calldata.Precip_Intensity_Max.astype(float)
    calldata.Temp_Max = calldata.Temp_Max.astype(float)
    calldata.Temp_Min = calldata.Temp_Min.astype(float)
    calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(datetime)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.Date = calldata.Date.astype(str)
    calldata.Time = calldata.Time.astype(str)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.EventBefore = calldata.EventBefore.astype(str)
    calldata.ConditionBefore = calldata.ConditionBefore.astype(str)

    print("Fixing Latitude and Longitude")
    # Format the latitude and longitude values into the appropriate formats, if they need to be formatted
    for k, info in enumerate(calldata.values):
        if calldata.Latitude.values[k] > 40:
            calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
            calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)

    # The key for using DarkSky API
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

        # Retrieve the main weather data
        try:
            forecastcall = forecast(*call, time=t)
            # Hourly data
            for i, value in enumerate(forecastcall.hourly):
                # Retrieving weather for previous weather
                if i == hoa:
                    calldata.Temperature.values[k] = value.temperature
                    calldata.Dewpoint.values[k] = value.dewPoint
                    calldata.Event.values[k] = value.icon
                    calldata.Humidity.values[k] = value.humidity
                    calldata.Month.values[k] = moa
                    calldata.Visibility.values[k] = value.visibility
                    calldata.Conditions.values[k] = value.summary
        except:
            print("Hourly Lookup Failed")
        # try:
            # Daily data, which requires individual try/except statements, otherwise the code crashes for some reason
        for j, value2 in enumerate(forecastcall.daily):
            try:
                calldata.Precipitation_Type.values[k] = value2.precipType
            except:
                calldata.Precipitation_Type.values[k] = "NA"
            try:
                calldata.Precipitation_Intensity.values[k] = value2.precipIntensity
            except:
                calldata.Precipitation_Intensity.values[k] = -1000
            try:
                calldata.Precip_Intensity_Max.values[k] = value2.precipIntensityMax
            except:
                calldata.Precip_Intensity_Max.values[k] = -1000
            try:
                calldata.Precip_Intensity_Time.values[k] = value2.precipIntensityMaxTime
            except:
                calldata.Precip_Intensity_Time.values[k] = -1000
            try:
                calldata.Temp_Max.values[k] = value2.temperatureMax
            except:
                calldata.Temp_Max.values[k] = -1000
            try:
                calldata.Temp_Min.values[k] = value2.temperatureMin
            except:
                calldata.Temp_Min.values[k] = -1000
            try:
                calldata.Cloud_Coverage.values[k] = value2.cloudCover
            except:
                calldata.Cloud_Coverage.values[k] = -1000
        # except:
        #     print("Daily Lookup Failed")


    save_excel_file(folderpath + "Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg.xlsx",
                    "DarkSky Weather", calldata)


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

# Code for aggregating data and converting them into numerical forms for modelling #
# calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/I24AccidentHours.xlsx")

# header_list = ("Accident", 'Latitude', 'Longitude', 'Date', 'Time', 'Address', "Route", "Log_Mile", 'City', 'Event',
#                'Conditions', "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min",
#                "Daily_Avg_Temp", "Monthly_Avg_Temp", "Relative_Temp", 'Dewpoint', 'Humidity', 'Month', 'Visibility',
#                "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity", "Precip_Intensity_Max",
#                "Precip_Intensity_Time", "Clear", "Cloudy", "Rain", "Fog", "Snow", "RainBefore")
#
# calldata = calldata.reindex(columns=header_list)
# calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg.xlsx")
# for i, value in enumerate(calldata.values):
#     print(i)
#     if "clear" in calldata.Event.values[i] or "clear" in calldata.Conditions.values[i] \
#             or "Clear" in calldata.Event.values[i] or "Clear" in calldata.Conditions.values[i]:
#         calldata.Clear.values[i] = 1
#     else:
#         calldata.Clear.values[i] = 0
#
#     if "rain" in calldata.Event.values[i] or "rain" in calldata.Conditions.values[i] \
#             or "Rain" in calldata.Event.values[i] or "Rain" in calldata.Conditions.values[i] \
#             or "Drizzle" in calldata.Event.values[i] or "Drizzle" in calldata.Conditions.values[i] \
#             or "drizzle" in calldata.Event.values[i] or "drizzle" in calldata.Conditions.values[i]:
#         calldata.Rain.values[i] = 1
#     else:
#         calldata.Rain.values[i] = 0
#
#     if "snow" in calldata.Event.values[i] or "snow" in calldata.Conditions.values[i] \
#             or "Snow" in calldata.Event.values[i] or "Snow" in calldata.Conditions.values[i]:
#         calldata.Snow.values[i] = 1
#     else:
#         calldata.Snow.values[i] = 0
#
#     if "cloudy" in calldata.Event.values[i] or "cloudy" in calldata.Conditions.values[i] \
#             or "Cloudy" in calldata.Event.values[i] or "Cloudy" in calldata.Conditions.values[i] \
#             or "overcast" in calldata.Event.values[i] or "overcast" in calldata.Conditions.values[i] \
#             or "Overcast" in calldata.Event.values[i] or "Overcast" in calldata.Conditions.values[i]:
#         calldata.Cloudy.values[i] = 1
#     else:
#         calldata.Cloudy.values[i] = 0
#
#     if "fog" in calldata.Event.values[i] or "foggy" in calldata.Conditions.values[i] \
#             or "Fog" in calldata.Event.values[i] or "Foggy" in calldata.Conditions.values[i]:
#         calldata.Fog.values[i] = 1
#     else:
#         calldata.Fog.values[i] = 0
#     if "rain" in calldata.EventBefore.values[i] or "rain" in calldata.ConditionBefore.values[i] \
#             or "Rain" in calldata.EventBefore.values[i] or "Rain" in calldata.ConditionBefore.values[i]:
#         calldata.RainBefore.values[i] = 1
#     else:
#         calldata.RainBefore.values[i] = 0
# calldata.drop(["Precipitation_Type", "Event", "Conditions", "EventBefore", "ConditionBefore"], axis=1, inplace=True)

# dayHolder_2017 = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2017.xlsx")
# dayHolder_2018 = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx")
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
# save_excel_file(folderpath +
#                 "Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg.xlsx",
#                 "Aggregated Weather", calldata)



