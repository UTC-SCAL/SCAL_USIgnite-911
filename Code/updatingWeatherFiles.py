import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
# import feather


def find_cred(service):
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
    print("Fetching Weather")
    dates = pandas.date_range(beginDate, endDate)
    # Read in the center points file to get the used grid blocks (ORIG_FID) and their lat/longs
    centers = pandas.read_csv("../Excel & CSV Sheets/Grid Files/Grid Oriented Layout/CenterPoints Ori Layout.csv")
    miss_loc = len(weatherFile)
    key = find_cred("darksky")
    for _, i in enumerate(centers.ORIG_FID.values):
        # This first loop is used to resume the code where it crashes, as sometimes darksky decides to deny us
        # if i < 0:
        #     print("Passing til ", i)
        #     pass
        # else:
        i = int(i)
        print(i)
        lat = centers.Center_Lat.values[i]
        long = centers.Center_Long.values[i]
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
                    weatherFile.loc[miss_loc, things] = entry[things]
                weatherFile.loc[miss_loc, "Center_Lat"] = lat
                weatherFile.loc[miss_loc, "Center_Long"] = long
                weatherFile.loc[miss_loc, "ORIG_FID"] = i
                miss_loc += 1
        return weatherFile

# Converting the unix time (labeled as time because Pete doesn't like consistency) to Date and timereadable
def standardFromUnix(weatherFile):
    print("Converting Time")
    weatherFile.timereadable = weatherFile.timereadable.astype(str)
    weatherFile.Date = weatherFile.Date.astype(str)
    weatherFile.time = weatherFile.time.astype(int)

    for i, value in enumerate(weatherFile.values):
        print(i)
        unix = weatherFile.time.values[i]
        readTime = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        weatherFile.timereadable.values[i] = readTime.split(" ")[1]
        weatherFile.Date.values[i] = readTime.split(" ")[0]
    return weatherFile

# Aggregates Event and Conditions
def finding_binaries(weatherFile):
    print("Aggregating Weather")
    weatherFile['Event'] = weatherFile['icon']
    weatherFile['Conditions'] = weatherFile['summary']
    weatherFile.Event = weatherFile.Event.apply(lambda x: x.lower())
    weatherFile.Conditions = weatherFile.Conditions.apply(lambda x: x.lower())
    # weatherFile.EventBefore = weatherFile.EventBefore.apply(lambda x: x.lower())
    # weatherFile.ConditionBefore = weatherFile.ConditionBefore.apply(lambda x: x.lower())
    weatherFile['Rain'] = weatherFile.apply(lambda x : 1 if ("rain" in x.Event or "rain" in x.Conditions) else 0, axis=1)
    weatherFile['Cloudy'] = weatherFile.apply(lambda x : 1 if ("cloud" in x.Event or "cloud" in x.Conditions) else 0, axis=1)
    weatherFile['Foggy'] = weatherFile.apply(lambda x : 1 if ("fog" in x.Event or "fog" in x.Conditions) else 0, axis=1)
    weatherFile['Snow'] = weatherFile.apply(lambda x : 1 if ("snow" in x.Event or "snow" in x.Conditions) else 0, axis=1)
    weatherFile['Clear'] = weatherFile.apply(lambda x : 1 if ("clear" in x.Event or "clear" in x.Conditions) else 0, axis=1)
    return weatherFile


def appendMainWeather(main_weather, new_weather):
    # Now, append the new weather file to the main weather file for the corresponding year #
    # This is the list order for the columns we want the weather files to have
    header_list = ('Center_Lat', 'Center_Long', 'ORIG_FID', 'apparentTemperature', 'cloudCover', 'dewPoint', 'humidity',
                   'Event', 'ozone', 'precipAccumulation', 'precipIntensity', 'precipProbability', 'precipType',
                   'pressure',
                   'Conditions', 'temperature', 'time', 'Date', 'timereadable', 'uvIndex', 'visibility', 'windBearing',
                   'windGust', 'windSpeed', 'EventBefore', 'ConditionBefore', 'hourbefore', 'Rain', 'Cloudy', 'Foggy',
                   'Snow', 'Clear')
    main_weather = main_weather.reindex(columns=header_list)
    new_weather = new_weather.reindex(columns=header_list)
    main_weather.timereadable = main_weather.timereadable.astype(str)
    new_weather.timereadable = new_weather.timereadable.astype(str)
    # Print the length and columns of the main weather file and the new weather file, just to make sure the appended
    # dataframe is the proper length and has the correct columns
    print("Length of Main Weather file: ", len(main_weather))
    print(main_weather.columns)
    print("Length of New Weather file: ", len(new_weather))
    print(new_weather.columns)

    bigBOIweather = main_weather.append(new_weather)
    print("Appended Weather file length: ", len(bigBOIweather))
    print(bigBOIweather.columns)

    return bigBOIweather


# Use these lines for adding weather #
# This file is only for reading in the columns we need for the weather file
# weather_2019 = feather.read_dataframe("../Ignore/Weather/2019 Weather.feather")
# weatherFile = pandas.DataFrame(columns=weather_2019.columns)
# Set the start and end date for the weather file to be updated
# begin = '2019-06-26'
# end = '2019-09-05'
# fetchWeather(weatherFile, begin, end)


# Use these lines for formatting the newly added weather #
# weatherFile = pandas.read_csv("../Ignore/Weather/2019 Weather Updated4.csv")
# Convert unix time to date and time readable
# standardFromUnix(weatherFile)
# Get the aggregated values of event and conditions
# finding_binaries(weatherFile)
# weatherFile.to_csv("../Ignore/Weather/2019 Weather Updated4 Full.csv")

# Use these lines to combine weather files #
# Based on how many different files were made when getting new weather, add or remove weather# files to be appended
# weather1 = pandas.read_csv("../")
# weather2 = pandas.read_csv("../")
# weather3 = pandas.read_csv("../")
# weather4 = pandas.read_csv("../")

# Append that shiz
# new_weather = pandas.concat([weather1, weather2, weather3, weather4], axis=0, join='outer', ignore_index=False)
# Drop duplicates if there are any
# new_weather.drop_duplicates(keep="first", inplace=True)
# Save the new weather file if you want to
# feather.write_dataframe(new_weather, "../")
# Read in the main weather file you'll be appending to
# new_weather = feather.read_dataframe("../")
# main_weather = feather.read_dataframe("../")
# Append the new weather to the main weather
# bigBOIweather = appendMainWeather(main_weather, new_weather)
# After the main appending, save the file
# feather.write_dataframe(bigBOIweather, "../")
