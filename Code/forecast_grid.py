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
from selenium import webdriver
import schedule

# This is the file containing the lat/long coords for the grid blocks and their centers
places = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Blank Forecast Forum.csv", sep=",")

##Fetching the weather forecast for the given file.
def forecasting(places, month, day, year):
    start = datetime.datetime.now()
    places.Event = places.Event.astype(str)
    # places.Unix = places.Unix.astype(int)
    places.Conditions = places.Conditions.astype(str)
    places.Precipitation_Type = places.Precipitation_Type.astype(str)
    places.Precipitation_Intensity = places.Precipitation_Intensity.astype(float)
    places.Precip_Intensity_Max = places.Precip_Intensity_Max.astype(float)
    places.Temp_Max = places.Temp_Max.astype(float)
    places.Temp_Min = places.Temp_Min.astype(float)
    # places.Precip_Intensity_Time = places.Precip_Intensity_Time.astype(str)
    places.Latitude = places.Latitude.astype(float)
    places.Longitude = places.Longitude.astype(float)
    places.EventBefore = places.EventBefore.astype(str)
    places.ConditionBefore = places.ConditionBefore.astype(str)
    thisdate = str(month) + '/' + str(day) + '/' + str(year)
    dt = datetime.datetime.strptime(thisdate, '%m/%d/%Y')
    print(thisdate, dt.weekday())
    # places.Date = thisdate
    places.Weekday = dt.weekday()
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
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
                    try:
                        places.Cloud_Coverage.values[r] = value2.cloudCover
                    except:
                        places.Cloud_Coverage.values[r] = -1000
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


print("Beginning code at:", datetime.datetime.now())

# forecasting(places, 5, 13, 2019)
# exit()
##Run the forecast at 6PM, midnight, 6AM, and noon.
# schedule.every().day.at("18:00").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("00:00").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("09:37").do(job, "Fetching weather forecast", places)
# schedule.every().day.at("12:02").do(job, "Fetching weather forecast", places)

forecasting(places, 6, 8, 2019)

# while True:
#     schedule.run_pending()
#     schedule.every(30).minutes.do(waiting, datetime.datetime.now())
#     time.sleep(30)