import matplotlib.pyplot as plt
import numpy
import datetime
import time
from darksky import forecast
import pytz
import pandas
import math
import os, sys
from os.path import exists
# from selenium import webdriver
import feather
# import schedule
from datetime import timedelta

yoa = 2019
moa = 8
dayoa = 5
theday = datetime.datetime(yoa, moa, dayoa, 1, 0, 0)
test = theday.isoweekday() in range(1,6)
print(theday, test)
yesterday = (datetime.date.today()- timedelta(1)).strftime("%Y-%m-%d")
today = datetime.date.today().strftime("%Y-%m-%d")
isit = pandas.bdate_range(yesterday, yesterday)
name = (datetime.date.today()-timedelta(1)).isoweekday() in range(1, 6)
print("Yesterday",isit, name)

isit = pandas.bdate_range(today, today)
name = (datetime.date.today()).isoweekday() in range(1, 6)
print("Today",isit, name)

exit()

# This is the file containing the lat/long coords for the grid blocks and their centers
places = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Forecast Forum Ori Filled.csv", sep=",")
grid_blocks = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Info.csv")
# print(grid_blocks.Grid_Block[0:5])

##Filling in GridBlocks for the forecast file. 
# newplaces = pandas.merge(places, grid_blocks[['Grid_Block','Grid_Col', 'Grid_Row']], on=['Grid_Col', 'Grid_Row'])
# newplaces.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Forecast Forum Ori Filled.csv", index=False)

all_weather = feather.read_dataframe("../Excel & CSV Sheets/ALL_Weather_with_Binary.feather")
print(all_weather.columns)
test = all_weather.columns[1:-2]
shape = test.shape
print(test.shape)
print(len(all_weather.Rain))
print(sum(all_weather.Rain))
exit()
def finding_binaries(data):
    starttime = datetime.datetime.now()
    print("Beginning Lowercase conversion at:", starttime)
    data.Event = data.Event.apply(lambda x: x.lower())
    data.Conditions = data.Conditions.apply(lambda x: x.lower())
    data.EventBefore = data.EventBefore.apply(lambda x: x.lower())
    data.ConditionBefore = data.ConditionBefore.apply(lambda x: x.lower())
    lowertime = datetime.datetime.now()
    print("Lowercase conversion done, Beginning Binary Lambdas at:", lowertime - starttime)
    data['Rain'] = data.apply(lambda x : 1 if ("rain" in x.Event or "rain" in x.Conditions) else 0, axis=1)
    raintime = datetime.datetime.now()
    print("Rain completed in:", raintime - lowertime)
    data['Cloudy'] = data.apply(lambda x : 1 if ("cloud" in x.Event or "cloud" in x.Conditions) else 0, axis=1)
    cloudtime = datetime.datetime.now()
    print("Cloudy completed in:", cloudtime - raintime)
    data['Foggy'] = data.apply(lambda x : 1 if ("fog" in x.Event or "fog" in x.Conditions) else 0, axis=1)
    fogtime = datetime.datetime.now()
    print("Foggy completed in:", fogtime - cloudtime)
    data['Snow'] = data.apply(lambda x : 1 if ("snow" in x.Event or "snow" in x.Conditions) else 0, axis=1)
    snowtime = datetime.datetime.now()
    print("Snow completed in:", snowtime - fogtime)
    data['Clear'] = data.apply(lambda x : 1 if ("clear" in x.Event or "clear" in x.Conditions) else 0, axis=1)
    cleartime = datetime.datetime.now()
    print("Clear completed in:", cleartime - snowtime)
    return data

# print(all_weather.columns)
# print(all_weather.Rain[0:5])
# print(all_weather.Rain.unique)
exit()
places['Hour'] = places['Hour'].astype(int)
# exit()

# places['time'] = places['Hour'].map(lambda x : datetime.datetime(yoa, moa, dayoa, x, 0, 0).strftime('%s'))
# places['hourbefore'] = places['time'].map(lambda x : int(x) - 60*60)
# print(places.time[0:5],places.hourbefore[0:5])

def find_cred(service):
    file = "../Excel & CSV Sheets/login.csv"
    if os.path.exists(file):
        with open(file, "r") as file:
            lines = file.readlines()
            if service in lines[0]:
                cred = lines[0].split(",")[1]
                # print(cred)
            if service in lines[1]:
                cred = str(lines[1].split(",")[1]) + "," + str(lines[1].split(",")[2])
                # print(cred)
                    # logins[username] = password
    return cred

##Fetching the weather forecast for the given file.
def forecasting(places, month, day, year):
    start = datetime.datetime.time()
    places.Event = places.Event.astype(str)
    # places.Unix = places.Unix.astype(int)
    places.Conditions = places.Conditions.astype(str)
    places.Precipitation_Type = places.Precipitation_Type.astype(str)
    places.Precipitation_Intensity = places.Precipitation_Intensity.astype(float)
    places.Precip_Intensity_Max = places.Precip_Intensity_Max.astype(float)
    # places.Temp_Max = places.Temp_Max.astype(float)
    # places.Temp_Min = places.Temp_Min.astype(float)
    # places.Precip_Intensity_Time = places.Precip_Intensity_Time.astype(str)
    places.Latitude = places.Latitude.astype(float)
    places.Longitude = places.Longitude.astype(float)
    places.EventBefore = places.EventBefore.astype(str)
    places.ConditionBefore = places.ConditionBefore.astype(str)
    thisdate = str(month) + '/' + str(day) + '/' + str(year)
    dt = datetime.datetime.strptime(thisdate, '%m/%d/%Y')
    # print(thisdate, dt.weekday())
    # places.Date = thisdate
    # places.Weekday = dt.weekday()
    key = find_cred("darksky")
    # key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    hoa = 0
    mioa = 0
    soa = 0
    yoa = year
    moa = month
    dayoa = day
    filename = "../Excel & CSV Sheets/Grid Layout Test Files/Forecast-for" + str(month) + "-" + str(day) + "-" + str(year) + "_" + str(
        start.date()) + "_" + str(start.hour) + ".csv"
    print(filename)
    for d, stuff in enumerate(places.values[0:(len(places.loc[places['Hour'] == 0]))]):
        print(d)
        lat = places.Latitude.values[d]
        long = places.Longitude.values[d]
        t = datetime.datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
        call = key, lat, long

        try:
            forecastcall = forecast(*call, time=t, header={'Accept-Encoding': 'gzip'})

            # Hourly data
            for i in range(0, 7):
                r = (i * len(places.loc[places['Hour'] == 0]))
                if d != 0:
                    r = (i * len(places.loc[places['Hour'] == 0])) + d
                hour = places.Hour.values[r]
                for k, value in enumerate(forecastcall.hourly):
                    # Retrieving weather for previous weather
                    if k == hour:
                        # places.Temperature.values[r] = value.temperature
                        # places.Dewpoint.values[r] = value.dewPoint
                        places.Event.values[r] = value.icon
                        # places.Humidity.values[r] = value.humidity
                        # places.Month.values[r] = moa
                        places.Visibility.values[r] = value.visibility
                        places.Conditions.values[r] = value.summary
                        places.ConditionBefore.values[r] = forecastcall.hourly[k - 1].summary
                        places.EventBefore.values[r] = forecastcall.hourly[k - 1].icon
                # print(places.values[r])
                for j, value2 in enumerate(forecastcall.daily):
                    try:
                        places.Precipitation_Type.values[r] = value2.precipType
                    except:
                        places.Precipitation_Type.values[r] = "NA"
                    try:
                        places.Precipitation_Intensity.values[r] = value2.precipIntensity
                    except:
                        places.Precipitation_Intensity.values[r] = -1000
                    try:
                        places.Precip_Intensity_Max.values[r] = value2.precipIntensityMax
                    except:
                        places.Precip_Intensity_Max.values[r] = -1000
                    # try:
                    #     places.Precip_Intensity_Time.values[r] = value2.precipIntensityMaxTime
                    # except:
                    #     places.Precip_Intensity_Time.values[r] = -1000
                    # try:
                    #     places.Temp_Max.values[r] = value2.temperatureMax
                    # except:
                    #     places.Temp_Max.values[r] = -1000
                    # try:
                    #     places.Temp_Min.values[r] = value2.temperatureMin
                    # except:
                    #     places.Temp_Min.values[r] = -1000
                    # try:
                    #     places.Cloud_Coverage.values[r] = value2.cloudCover
                    # except:
                    #     places.Cloud_Coverage.values[r] = -1000
                    if "clear" in places.Event.values[r] or "clear" in places.Conditions.values[
                        r] \
                            or "Clear" in places.Event.values[r] or "Clear" in \
                            places.Conditions.values[r]:
                        places.Clear.values[r] = 1
                    else:
                        places.Clear.values[r] = 0

                    if "rain" in places.Event.values[r] or "rain" in places.Conditions.values[r] \
                            or "Rain" in places.Event.values[r] or "Rain" in \
                            places.Conditions.values[r] \
                            or "Drizzle" in places.Event.values[r] or "Drizzle" in \
                            places.Conditions.values[r] \
                            or "drizzle" in places.Event.values[r] or "drizzle" in \
                            places.Conditions.values[r]:
                        places.Rain.values[r] = 1
                    else:
                        places.Rain.values[r] = 0

                    if "snow" in places.Event.values[r] or "snow" in places.Conditions.values[i] \
                            or "Snow" in places.Event.values[r] or "Snow" in places.Conditions.values[r]:
                        places.Snow.values[r] = 1
                    else:
                        places.Snow.values[r] = 0

                    if "cloudy" in places.Event.values[r] or "cloudy" in \
                            places.Conditions.values[r] \
                            or "Cloudy" in places.Event.values[r] or "Cloudy" in \
                            places.Conditions.values[r] \
                            or "overcast" in places.Event.values[r] or "overcast" in \
                            places.Conditions.values[r] \
                            or "Overcast" in places.Event.values[r] or "Overcast" in \
                            places.Conditions.values[
                                r]:
                        places.Cloudy.values[r] = 1
                    else:
                        places.Cloudy.values[r] = 0

                    if "fog" in places.Event.values[r] or "foggy" in places.Conditions.values[r] \
                            or "Fog" in places.Event.values[r] or "Foggy" in \
                            places.Conditions.values[r]:
                        places.Fog.values[r] = 1
                    else:
                        places.Fog.values[r] = 0
                    if "rain" in places.EventBefore.values[r] or "rain" in \
                            places.ConditionBefore.values[r] \
                            or "Rain" in places.EventBefore.values[r] or "Rain" in \
                            places.ConditionBefore.values[r]:
                        places.RainBefore.values[r] = 1
                    else:
                        places.RainBefore.values[r] = 0
        except:
            pass
        if d % 400 == 0:
            places.to_csv(filename, sep=",", index=False)
    places.to_csv(filename, sep=",", index=False)

    end = datetime.datetime.now()
    print("Forecasting Complete. Duration:", end - start)

def findingweather(data, all_weather, yoa, moa, dayoa):
    data['time'] = data['Hour'].map(lambda x : datetime.datetime(yoa, moa, dayoa, x, 0, 0).strftime('%s'))
    data['hourbefore'] = data['time'].map(lambda x : int(x) - 60*60)
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['hourbefore'].astype(int)
    # Merge the event/conditions columns based on time and grid block
    newdata = pandas.merge(data, all_weather[['Rain','Cloudy', 'Foggy','Snow','Clear','time','Grid_Block']], on=['time','Grid_Block'])
    # Merge the event/conditions before columns based on hour before and grid block
    newdata = pandas.merge(newdata, all_weather[['RainBefore','hourbefore','Grid_Block']], on=['hourbefore','Grid_Block'])

def job(t, places):
    # Setting the date to fetch for. If it's 6pm, use the date of tomorrow. If any other time, use todays.
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    thistime = datetime.datetime.now()
    if thistime.hour == 18:
        month = tomorrow.month
        day = tomorrow.day
        year = tomorrow.year
    else:
        month = thistime.month
        day = thistime.day
        year = thistime.year
    # month = 6
    # day = 8
    # year = 2019
    print(t, "Using Date: ", month, "/", day, "/", year)
    forecasting(places, month, day, year)
    return


def waiting(time):
    print("Waiting:", time.strftime("%Y-%m-%d %H:%M"))
    return


findingweather(places, all_weather, 2019, 3, 5)
print(places.head())
print(places.Event.unique())
exit()
print("Beginning code at:", datetime.datetime.now())

# forecasting(places, 4, 10, 2019)

exit()
##Run the forecast at 6PM, midnight, 6AM, and noon.
# schedule.every().day.at("18:00").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("00:00").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("09:37").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("12:02").do(job, "Fetching weather forecast", places)

# forecasting(places, 6, 8, 2019)

# while True:
#     schedule.run_pending()
#     schedule.every(30).minutes.do(waiting, datetime.datetime.now())
#     time.sleep(30)