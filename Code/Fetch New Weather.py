"""
Authors: Jeremy Roland and Pete Way
Purpose: This file is meant to fetch weather for our Grid Block and Grid Hex city layouts for the 911 project
    I use this as a sort of bootleg parallelization of the code, as I simply copy the code from this file and paste
        it in 3 other temporary files
"""

import pandas
import os
from datetime import datetime
from darksky import forecast
import feather


def find_cred(service):
    """
        A method to call in the username and password for certain authentication requiring services
        If you don't have the login.csv file for it, then ask Jeremy or Peter to send it to you
    """
    file = "../Ignore/logins.csv"
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


# File for getting weather from DarkSky and adding it to our files
def fetchWeather(weatherFile, beginDate, endDate):
    """
        Ok, so, the way this code works is each fetching run of the code only gets 25 grid locations worth of weather
        for the date range provided.
        The longer this code runs, the slower it gets
        start_block: this is the grid location where the fetching should start. The for loop below starts on the next
            grid location. So, for start_block = 0, the code would start fetching on grid location 1.
        stop_block: the last block the loop should fetch weather for.
        Both start and stop block are used in saving the file (seen in saveName). So, when fetching weather, all you
            have to do is alter the start_block value
    """
    print("Fetching Weather")
    dates = pandas.date_range(beginDate, endDate)
    # Read in the center points file to get the used grid locations and their lat/longs
    centers = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    miss_loc = 0  # used for positioning values in the dataframe

    start_block = 0
    stop_block = start_block + 100
    saveName = "../Ignore/2021 Weather " + str(start_block+1) + "-" + str(stop_block) + ".csv"

    key = find_cred("darksky")
    for _, i in enumerate(centers.Grid_Num.values):
        if i < start_block + 1:
            print("Passing til ", start_block)
            pass
        elif i > stop_block:
            print("Reached stopping point for this set of blocks, which is ", stop_block)
            break
        else:
            i = int(i)
            print(i)
            lat = centers.Center_Lat.values[i-1]
            long = centers.Center_Long.values[i-1]
            for j in dates:
                j = str(j)
                j = str(j.split(" ")[0])
                year = int(j.split("-")[0])
                month = int(j.split("-")[1])
                day = int(j.split("-")[2])
                t = datetime(year, month, day, 0, 0, 0).isoformat()
                call = key, lat, long
                forecastcall = forecast(*call, time=t)
                hourly_list = [item._data for item in forecastcall.hourly]
                for l, info in enumerate(hourly_list):
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        weatherFile.at[miss_loc, things] = entry[things]
                    weatherFile.at[miss_loc, "Center_Lat"] = lat
                    weatherFile.at[miss_loc, "Center_Long"] = long
                    weatherFile.at[miss_loc, "Grid_Num"] = i
                    miss_loc += 1
            # Incremental saving, in case something goes wrong
            if i % 10 == 0:
                weatherFile.to_csv(saveName)
                # feather.write_dataframe(weatherFile, saveName)
    # A final save for all the weather
    weatherFile.to_csv(saveName, index=False)
    # feather.write_dataframe(weatherFile, saveName)


# Aggregates Event and Conditions
def finding_binaries(weatherFile):
    """
        Takes the Event and Conditions variables provided by DarkSky and aggregates them into binary values for
            certain weather events
        By default, DarkSky returns icon and summary, which are Event and Conditions respectively. If the file you
            are using already has Event and Conditions, then comment out those two lines
        In the lambda statements, you'll see a lot of "empty" conditions. Sometimes DarkSky doesn't return any Event or
            Conditions for the time we want, so this code works around any empty values it returns so it doesn't break.
            It also sets the empty binary values to -1 so it's easy to find where any empty is in the dataframe.
    """
    print("Aggregating Weather")
    weatherFile['Event'] = weatherFile['icon']
    weatherFile['Conditions'] = weatherFile['summary']
    weatherFile.Event = weatherFile.Event.apply(lambda x: x.lower() if pandas.notnull(x) else "empty")
    weatherFile.Conditions = weatherFile.Conditions.apply(lambda x: x.lower() if pandas.notnull(x) else "empty")
    # Here, in the lambda functions, we use if, else, and elif statements for finding Event and Condition entries that
    # are NoneType, as darksky doesn't always have the answer for us.
    print("Aggregating Rain")
    weatherFile['Rain'] = weatherFile.apply(lambda x: 1 if ("rain" in x.Event or "rain" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    print("Aggregating Cloudy")
    weatherFile['Cloudy'] = weatherFile.apply(lambda x: 1 if ("cloud" in x.Event or "cloud" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    print("Aggregating Foggy")
    weatherFile['Foggy'] = weatherFile.apply(lambda x: 1 if ("fog" in x.Event or "fog" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    print("Aggregating Snow")
    weatherFile['Snow'] = weatherFile.apply(lambda x: 1 if ("snow" in x.Event or "snow" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    print("Aggregating Clear")
    weatherFile['Clear'] = weatherFile.apply(lambda x: 1 if ("clear" in x.Event or "clear" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)

    weatherFile.Rain = weatherFile.Rain.astype(int)
    weatherFile.Cloudy = weatherFile.Cloudy.astype(int)
    weatherFile.Foggy = weatherFile.Foggy.astype(int)
    weatherFile.Snow = weatherFile.Snow.astype(int)
    weatherFile.Clear = weatherFile.Clear.astype(int)
    return weatherFile


def post_process_weather(columns):
    """
    It's main function is to do some post processing tasks for weather files we've recently fetched from darksky
    You can add in any additional post processing effects you need and comment out any you don't
    """

    # Use these lines to combine weather files #

    # weathers is a list of file paths that hold your newly fetched weather
    weathers = []
    # weather1 is a lone filepath that the files listed in the weathers list will be appended to
    # make sure that the filepath of weather1 isn't in the weathers list
    weather1 = pandas.read_csv("../")
    for weather in weathers:
        weather2 = pandas.read_csv("../%s" % weather)
        # Append that shiz
        weather1 = pandas.concat([weather1, weather2], axis=0, join='outer', ignore_index=False)
    # convert the Event/Conditions to their respective binary values
    new_weather = finding_binaries(weather1)
    new_weather['Unix'] = new_weather['time'].astype(int)
    new_weather = new_weather.reindex(columns=columns)
    # Converting Unix time to our local time
    new_weather.Date = pandas.to_datetime(new_weather['Unix'], unit='s', utc=False)
    new_weather.Date = new_weather.Date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    new_weather.Hour = new_weather['Date'].dt.hour
    new_weather.Date = new_weather['Date'].dt.date
    # Reindex our fetched weather to have the columns we want
    # new_weather = new_weather.reindex(columns=columns)

    # If you want to append your newly fetched weather to an existing weather file, then run these lines
    # Read in the main weather file you'll be appending to
    # Depending on how large the file is, it may be in a feather format, just use whatever file reading method
    # fits the format of your main weather file
    # main_weather = pandas.read_csv("../")
    # main_weather = feather.read_dataframe("../")

    # bigBOIweather = pandas.concat([main_weather, new_weather], axis=0, join='outer', ignore_index=False)

    # After the main appending, save the file
    # Depending on the size of the file, you'll use either a csv or feather
    # Feather files are typically used for larger files (> 1 GB)
    # bigBOIweather.to_csv("../")
    # Cast Date as a string if writing data to a feather file, otherwise it throws an error
    # bigBOIweather.Date = bigBOIweather.Date.astype(str)
    # feather.write_dataframe(bigBOIweather, "../")

    # If you are just fetching new weather and don't want to append it to any current weather file, then just save it
    # Again, depending on how large your file is, choose the appropriate file format
    # new_weather.to_csv("../", index=False)
    # feather.write_dataframe(new_weather, "../")


################################################ Fetching New Weather ##################################################
# The columns we want for our weather file
# columns = ['Center_Lat', 'Center_Long', 'Grid_Num']
# The new file to hold our weather
# When fetching weather, darksky adds in its own columns, but this ensures we have the other columns we need later on
# weatherFile = pandas.DataFrame(columns=columns)
# Set the start and end date for the weather file to be updated
# For the fetchWeather method, it follows this format: yyyy-m-dd
# begin = '2021-1-25'
# end = '2021-1-31'
# fetchWeather(weatherFile, begin, end)

############################################# Formatting Newly Fetched Weather #########################################
# processingColumns is typically the columns present in our main weather file
# These are the variables we will want to save for any weather information we fetch
# processingColumns = ['Center_Lat', 'Center_Long', 'Grid_Num', 'cloudCover',
#        'dewPoint', 'humidity', 'precipIntensity', 'precipProbability',
#        'precipType', 'pressure', 'temperature', 'Unix', 'Date', 'Hour',
#        'uvIndex', 'visibility', 'windBearing', 'windGust', 'windSpeed',
#        'Event', 'Conditions', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear']
# post_process_weather(processingColumns)
