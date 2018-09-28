import pandas
from datetime import datetime
from darksky import forecast
import os, sys
import random
import math


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


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

    # Create non-overlapping intervals to hold the temperature values
    # These specific columns don't like to use the easy method of reference by typing calldata.column_name, instead it
    # insists that I have to use iloc[row, column] for proper referencing.  So, if new variables are added, double check
    # to see what the current column numbers are for the temperature intervals
    # calldata.Temperature = calldata.Temperature.astype(float)
    # print("Adding in Temperature Intervals")
    # for i, values in enumerate(calldata.values):
    #     print(i)
    #     if calldata.Temperature.values[i] < 0:
    #         calldata.iloc[i, 17] = 1
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 0 and calldata.Temperature.values[i] < 10:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 1
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 10 and calldata.Temperature.values[i] < 20:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 1
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 20 and calldata.Temperature.values[i] < 30:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 1
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 30 and calldata.Temperature.values[i] < 40:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 1
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 40 and calldata.Temperature.values[i] < 50:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 1
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 50 and calldata.Temperature.values[i] < 60:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 1
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 60 and calldata.Temperature.values[i] < 70:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 1
    #         calldata.iloc[i, 25] = 0
    #     elif calldata.Temperature.values[i] >= 70:
    #         calldata.iloc[i, 17] = 0
    #         calldata.iloc[i, 18] = 0
    #         calldata.iloc[i, 19] = 0
    #         calldata.iloc[i, 20] = 0
    #         calldata.iloc[i, 21] = 0
    #         calldata.iloc[i, 22] = 0
    #         calldata.iloc[i, 23] = 0
    #         calldata.iloc[i, 24] = 0
    #         calldata.iloc[i, 25] = 1
    save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Negative Samples (Date).xlsx",
                    "Negative Samples", calldata)

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# # Hour Negative Sampling #
# calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")
# # Make a negative samples dataframe to hold the negative samples from calldata
# negative_samples = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/NegativeSamples.xlsx")
# neg_loc = 0  # Used for positioning
# calldata.Time = calldata.Time.astype(str)
# calldata.Date = calldata.Date.astype(str)
# # For selecting a random hour, use random.choice on a list while excluding the particular hour from the range
# for i, info in enumerate(calldata.values):
#     print(i)
#     # Get the hour
#     n = calldata.Hour.values[i]  # Number to remove from list of hours
#     hours = range(0, 24)
#     r = [x for x in hours if x != n]  # A list of numbers without n
#     # Replace hour in calldata with a random hour
#     calldata.Hour.values[i] = random.choice(r)
#     # Check other entries if there's a match
#     for k, checks in enumerate(calldata.values):  # Iterates through calldata checking for a match with i
#         if calldata.Hour.values[k] == calldata.Hour.values[i] and calldata.Date.values[k] is calldata.Date.values[i]:
#             # If match, skip
#             pass
#         else:
#             # print("No match found, negative sample added to new dataframe")
#             new_hour = str(calldata.Hour.values[i])
#             toa = calldata.Time.values[i]
#             mioa = str(toa.split(':')[1])
#             soa = str(toa.split(':')[2])
#             new_time = new_hour + ":" + mioa + ":" + soa
#             calldata.Date = calldata.Date.astype(datetime)
#             negative_samples.loc[neg_loc, "Latitude"] = calldata.Latitude.values[i]
#             negative_samples.loc[neg_loc, "Longitude"] = calldata.Longitude.values[i]
#             negative_samples.loc[neg_loc, "Date"] = calldata.Date.values[i]
#             negative_samples.loc[neg_loc, "Time"] = new_time
#             negative_samples.loc[neg_loc, "Hour"] = calldata.Hour.values[i]
#             negative_samples.loc[neg_loc, "Address"] = calldata.Address.values[i]
#             negative_samples.loc[neg_loc, "City"] = calldata.City.values[i]
#             negative_samples.loc[neg_loc, "Route"] = calldata.Route.values[i]
#             neg_loc = neg_loc + 1
#             break
# save_excel_file("",
#                 "Negative Samples", negative_samples)

calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Negative Samples by Date Raw.xlsx")
add_data(calldata)

# calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")
# day_holder2017 = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2017.xlsx")
# day_holder2018 = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx")
#
# # Make a negative samples dataframe to hold the negative samples from calldata
# negative_samples = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/NegativeSamples.xlsx")
# neg_loc = 0  # Used for positioning
# calldata.Date = calldata.Date.astype(str)
# day_holder2017.Date = day_holder2017.Date.astype(str)
# day_holder2018.Date = day_holder2018.Date.astype(str)
#
# # For selecting a random day, use random.choice on a list while excluding the particular day from the range
# for i, info in enumerate(calldata.values):
#     print(i)
#     # Get the day
#     doa = calldata.Date.values[i]  # Date of a 911 call
#     day_num = pandas.to_datetime(doa).strftime('%-j')
#     # Note: When selecting the corresponding date from the excel file, it's the Day_Num value - 1 #
#     # So, for the ranges, have them be from 0 to max Day_Num value + 1
#     days_2017 = range(0, 365)
#     # This variable needs to be updated for the current day, since 2018 is still going on
#     days_2018 = range(0, 269)
#
#     r_2017 = [x for x in days_2017 if x != day_num]  # A list of numbers without dayoa, covering the days in 2017
#     r_2018 = [y for y in days_2018 if y != day_num]  # A list of numbers without dayoa, covering the days in 2018
#     # Check to see what the year is; based on this, you use one of the above variables
#     yoa = int(doa.split('-')[0])  # Get the year
#     if yoa == 2017:
#         # Replace day in calldata with a random day
#         calldata.Date.values[i] = day_holder2017.Date.values[random.choice(r_2017)]
#     elif yoa == 2018:
#         calldata.Date.values[i] = day_holder2018.Date.values[random.choice(r_2018)]
#     # Check other entries if there's a match
#     for k, checks in enumerate(calldata.values):  # Iterates through calldata checking for a match with i
#         if calldata.Date.values[k] == calldata.Date.values[i]:
#             # If match, skip
#             pass
#         else:
#             # print("No match found, negative sample added to new dataframe")
#             calldata.Date = calldata.Date.astype(datetime)
#             negative_samples.loc[neg_loc, "Latitude"] = calldata.Latitude.values[i]
#             negative_samples.loc[neg_loc, "Longitude"] = calldata.Longitude.values[i]
#             negative_samples.loc[neg_loc, "Date"] = calldata.Date.values[i]
#             negative_samples.loc[neg_loc, "Time"] = calldata.Time.values[i]
#             negative_samples.loc[neg_loc, "Hour"] = calldata.Hour.values[i]
#             negative_samples.loc[neg_loc, "Address"] = calldata.Address.values[i]
#             negative_samples.loc[neg_loc, "City"] = calldata.City.values[i]
#             neg_loc = neg_loc + 1
#             break
# save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Negative Samples by Date Raw.xlsx",
#                 "Negative Samples", negative_samples)