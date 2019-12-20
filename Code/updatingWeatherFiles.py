"""
    This file is meant to fetch weather for our Grid Block and Grid Hex city layouts for the 911 project
    I use this as a sort of bootleg parallelization of the code, as I simply copy the code from this file and paste
        it in 3 other temporary files
"""

import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
import feather
import time
import pytz


def find_cred(service):
    """
        A method to call in the username and password for certain authentication requiring services
        If you don't have the login.csv file for it, then ask Jeremy or Peter to send it to you
    """
    file = "../Ignore/login.csv"
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
        The longer this code runs, the slower it gets. For 25 grid locations it takes about 3-4 hours
        start_block: this is the grid location where the fetching should start. The for loop below starts on the next
            grid location. So, for start_block = 25, the code would start fetching on grid location 26.
        stop_block: the last block the loop should fetch weather for.
        Both start and stop block are used in saving the file (seen in saveName). So, when fetching weather, all you
            have to do is alter the start_block value
    """
    print("Fetching Weather")
    dates = pandas.date_range(beginDate, endDate)
    # Read in the center points file to get the used grid locations and their lat/longs
    centers = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/Hex_GridInfo.csv")
    miss_loc = 0  # used for positioning values in the dataframe

    start_block = 600
    stop_block = start_block + 25
    saveName = "../Ignore/Weather/Hex Layout/2019 Weather " + str(start_block+1) + "-" + str(stop_block) + " CP.feather"

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
                feather.write_dataframe(weatherFile, saveName)
    # A final save for all the weather
    feather.write_dataframe(weatherFile, saveName)

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
    weatherFile['Rain'] = weatherFile.apply(lambda x: 1 if ("rain" in x.Event or "rain" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    weatherFile['Cloudy'] = weatherFile.apply(lambda x: 1 if ("cloud" in x.Event or "cloud" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    weatherFile['Foggy'] = weatherFile.apply(lambda x: 1 if ("fog" in x.Event or "fog" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    weatherFile['Snow'] = weatherFile.apply(lambda x: 1 if ("snow" in x.Event or "snow" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)
    weatherFile['Clear'] = weatherFile.apply(lambda x: 1 if ("clear" in x.Event or "clear" in x.Conditions)
    else ("-1" if "empty" in x.Event or "empty" in x.Conditions else 0), axis=1)

    weatherFile.Rain = weatherFile.Rain.astype(int)
    weatherFile.Cloudy = weatherFile.Cloudy.astype(int)
    weatherFile.Foggy = weatherFile.Foggy.astype(int)
    weatherFile.Snow = weatherFile.Snow.astype(int)
    weatherFile.Clear = weatherFile.Clear.astype(int)
    return weatherFile


def hourly_check(lat, long, y, m, d, key):
    """
    A quick method to check a single return value for our hourly weather call
    This is a small snip of the code using in updatingWeatherFiles.py's fetchWeather method
    :param lat: latitude
    :param long: longitude
    :param y: year
    :param m: month
    :param d: day
    :param key: the darksky api key needed to call darksky (requires find_cred method)
    :return:
    """
    print("Fetching weather for ", y, m, d)
    t = datetime(y, m, d, 0, 0, 0).isoformat()
    call = key, lat, long
    forecastcall = forecast(*call, time=t)
    hourly_list = [item._data for item in forecastcall.hourly]
    for l, info in enumerate(hourly_list):
        entry = hourly_list[l]
        print(entry)


def return_unix(date, hour):
    """
        A quick function to convert a date hour combo to unix
    """
    # Ensure date is formatted as such: yyyy/mm/d
    timestamp = str(date) + " " + str(hour)
    return time.mktime(datetime.strptime(timestamp, "%Y/%m/%d %H").timetuple())


def return_date(unix):
    """
        A quick function to return a readable timestamp in our timezone (Chattanooga time)
        I left in different specific variables (hour, year, etc.) in case a user wants those specific values
        If you do, then just uncomment the variable and set it as the return value
    """
    tz = pytz.timezone('America/New_York')
    dt = datetime.fromtimestamp(unix, tz)
    # hour = dt.hour
    # date = dt.date()
    # year = date.year
    # month = date.month
    # day = date.day
    timereadable = dt.strftime("%Y-%m-%d %H:%M:%S")
    return timereadable


def get_missing_weather(missingWeather):
    """
    A method for finding certain darksky variables that may have not been returned when fetching weather
    This is mainly for large batchest of missing weather dates that all have the same grid locations
    In other words, if we have a list of 13 date/hour combinations that are all missing weather for grid locations
        1-300, then we can group those dates together to fetch the weather for those respective grid locations
    :param missingWeather: the dataframe to hold your missing weather. it should have any weather items you want to
        get
    dates: list of dates and the hour that's missing weather information from the fetched weather file
    centers: the center points for the grid locations. By default, code assumes all grid locations in the file are
        missing weather for the corresponding values in dates. To only get the desired grid blocks, simply alter the
        second for loop (centers.Grid_Num.values) to cover the range of grid locations you want
    gridLocations: a smaller list of the grid locations. Use this if you only have a hand full of grid locations you
        need
    The variables returned by the darksky call are the ones available for the type of call we are doing. If you don't
        need certain variables for your call, just comment out those variables below
    """
    # If you want to use gridLocations, then remember to alter some lat/long code in for loop # 2
    centers = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/Hex_GridInfo.csv")
    gridLocations = []

    # You will likely have to convert some columns to the appropriate type, just fyi
    # Add any columns you may need, and comment out any you don't
    missingWeather.Event = missingWeather.Event.astype(str)
    missingWeather.Conditions = missingWeather.Conditions.astype(str)
    # missingWeather.precipType = missingWeather.precipType.astype(str)
    missingWeather.timereadable = missingWeather.timereadable.astype(str)

    # Ensure format of a date is as follows: "yyyy/mm/d h", where h is hour in military time
    # So, a date of "2018/03/11 14" means that we are missing the weather for 2018/03/11 at 2 pm
    # Each entry is its own entity, so if we have multiple hours lacking weather for the same day (e.g., 2018/02/11 is
    # missing hours 3 and 8), then we'll have the following two entries: 2018/02/11 3 and 2018/02/11 8
    dates = []
    miss_loc = 0
    key = find_cred("darksky")
    for m, dateValue in enumerate(dates):
        print(m, "/", len(dates))
        hour = int(dates[m].split(" ")[1])
        date = dates[m].split(" ")[0]
        unix = return_unix(date, hour)

        tz = pytz.timezone('America/New_York')
        dt = datetime.fromtimestamp(unix, tz)
        dt_date = dt.date()
        year = int(dt_date.year)
        month = int(dt_date.month)
        day = int(dt_date.day)

        t = datetime(year, month, day, hour, 0, 0).isoformat()

        # For loop # 2 #
        # This for loop is for when using gridLocations to go over a smaller selection of grid locations
        # we get the corresponding row for the current grid location in the centers file and use the lat/long
        # for i, gridNum in enumerate(gridLocations):
        #     centers_row = centers.loc[centers["Grid_Num"] == gridLocations[i]]
        #     call = key, centers_row.Center_Lat.values[0], centers_row.Center_Long.values[0]
        #     gridValue = gridLocations[i]

        # This for loop is for iterating through the entire centers file for all grid locations
        for i, gridNum in enumerate(centers.Grid_Num.values):
            call = key, centers.Center_Lat.values[i], centers.Center_Long.values[i]
            gridValue = centers.Grid_Num.values[i]

            forecastcall = forecast(*call, time=t)
            for j, value in enumerate(forecastcall.hourly):
                # We use a series of try/except statements because sometimes darksky doesn't have the info we want to
                # query, so these statements avoid the code crashing and allow us to know what values weren't returned
                # The variables listed here are the ones available for the type of call we are sending to darksky
                # if you don't needs some of these variables, just comment them out
                if j == hour:
                    missingWeather.at[miss_loc, "Unix"] = unix
                    try:
                        missingWeather.at[miss_loc, "Event"] = value.icon
                    except:
                        missingWeather.at[miss_loc, "Event"] = 'empty'
                    try:
                        missingWeather.at[miss_loc, "Conditions"] = value.summary
                    except:
                        missingWeather.at[miss_loc, "Conditions"] = 'empty'
                    # Since these two values aren't from darksky, we don't have to worry about try/except
                    missingWeather.at[miss_loc, "timereadable"] = dateValue
                    missingWeather.at[miss_loc, "Grid_Num"] = gridValue
                    # try:
                    #     missingWeather.at[miss_loc, "cloudCover"] = value.cloudCover
                    # except:
                    #     missingWeather.at[miss_loc, "cloudCover"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "dewPoint"] = value.dewPoint
                    # except:
                    #     missingWeather.at[miss_loc, "dewPoint"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "humidity"] = value.humidity
                    # except:
                    #     missingWeather.at[miss_loc, "humidity"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "precipIntensity"] = value.precipIntensity
                    # except:
                    #     missingWeather.at[miss_loc, "precipIntensity"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "precipProbability"] = value.precipProbability
                    # except:
                    #     missingWeather.at[miss_loc, "precipProbability"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "precipType"] = value.precipType
                    # except:
                    #     missingWeather.at[miss_loc, "precipType"] = "empty"
                    # try:
                    #     missingWeather.at[miss_loc, "pressure"] = value.pressure
                    # except:
                    #     missingWeather.at[miss_loc, "pressure"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "temperature"] = value.temperature
                    # except:
                    #     missingWeather.at[miss_loc, "temperature"] = -100
                    # try:
                    #     missingWeather.at[miss_loc, "uvIndex"] = value.uvIndex
                    # except:
                    #     missingWeather.at[miss_loc, "uvIndex"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "visibility"] = value.visibility
                    # except:
                    #     missingWeather.at[miss_loc, "visibility"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "windBearing"] = value.windBearing
                    # except:
                    #     missingWeather.at[miss_loc, "windBearing"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "windGust"] = value.windGust
                    # except:
                    #     missingWeather.at[miss_loc, "windGust"] = -1
                    # try:
                    #     missingWeather.at[miss_loc, "windSpeed"] = value.windSpeed
                    # except:
                    #     missingWeather.at[miss_loc, "windSpeed"] = -1
                    miss_loc += 1
        # Saving after each date in dates has finished, in case some error happens
        missingWeather.to_csv("../", index=False)


def post_process_weather(columns):
    """
    This method is mainly for saving some space in the file and preventing me from continually commenting out certain
        chunks of code
    It's main function is to do some post processing tasks for weather files we've recently fetched from darksky
    You can add in any additional post processing effects you need and comment out any you don't
    """

    # Use these lines to combine weather files #
    # Based on how many different files were made when getting new weather, add or remove weather# files to be appended
    weather1 = feather.read_dataframe("../")
    weather2 = feather.read_dataframe("../")

    # Create the Unix column for later use
    weather1.Unix = weather1.time.astype(int)
    weather2.Unix = weather2.time.astype(int)

    # Lines for reindexing files if you need to
    # weather1 = weather1.reindex(columns=columns)
    # weather2 = weather2.reindex(columns=columns)

    # Append that shiz
    new_weather = pandas.concat([weather1, weather2], axis=0, join='outer', ignore_index=False)

    # Drop duplicates if there are any
    new_weather.drop_duplicates(keep="first", inplace=True)

    # convert the Event/Conditions to their respective binary values
    new_weather = finding_binaries(new_weather)

    # Converting Unix time to our local time
    new_weather.Date = pandas.to_datetime(new_weather['Unix'], unit='s', utc=False)
    new_weather.Date = new_weather.Date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    new_weather.Hour = new_weather['Date'].dt.hour
    new_weather.Date = new_weather['Date'].dt.date

    # Reindex our fetched weather to have the columns we want
    new_weather = new_weather.reindex(columns=columns)

    # If you want to append your newly fetched weather to an existing weather file, then run these lines
    # Read in the main weather file you'll be appending to
    # main_weather = feather.read_dataframe("../")
    # bigBOIweather = pandas.concat([main_weather, new_weather], axis=0, join='outer', ignore_index=False)
    # After the main appending, save the file
    # feather.write_dataframe(bigBOIweather, "../")

    # If you are just fetching new weather and don't want to append it to any current weather file, then just save it
    feather.write_dataframe(new_weather, "../")


# Use these lines for adding weather #
# The columns we want for our weather file
columns = ['Center_Lat', 'Center_Long', 'Grid_Num', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
               'precipProbability', 'precipType', 'pressure', 'temperature', 'Unix', 'Date', 'Hour', 'uvIndex',
               'visibility', 'windBearing', 'windGust', 'windSpeed', 'Event', 'Conditions', 'Rain', 'Cloudy',
               'Foggy', 'Snow', 'Clear']
# The new file to hold our weather
# When fetching weather, darksky adds in its own columns, but this ensures we have the other columns we need later on
weatherFile = pandas.DataFrame(columns=columns)
# Set the start and end date for the weather file to be updated
begin = ''
end = ''
