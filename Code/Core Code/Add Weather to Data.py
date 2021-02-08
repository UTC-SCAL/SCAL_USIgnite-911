"""
Authors: Jeremy Roland and Pete Way
Purpose: To match our weather data to our accident data
"""

import pandas
import os
import feather


# Method to log into the corresponding DarkSky or Etrims service through a file on this machine
# The file itself isn't on GitHub, so if you don't have it message Jeremy or Pete for the file
def find_cred(service):
    file = "../Pre Thesis/login.csv"
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


# Matches up entries to existing weather from a weather file
def add_weather(data, weather):
    print("Adding Weather")
    data.Unix = data.Unix.astype(int)
    weather.Unix = weather.Unix.astype(int)
    data.Grid_Num = data.Grid_Num.astype(int)
    weather.Grid_Num = weather.Grid_Num.astype(int)
    # Merge the weather variables for the hour of the accident based on time and grid num
    newdata = pandas.merge(data, weather[['Grid_Num', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
                                          'precipProbability', 'precipType', 'pressure', 'temperature', 'Unix',
                                          'uvIndex', 'visibility', 'windBearing', 'windGust', 'windSpeed', 'Event',
                                          'Conditions', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear']],
                           on=['Unix', 'Grid_Num'])
    # Drop any duplicates that the above statement may make
    newdata.drop_duplicates(keep="first", inplace=True)

    # Applying rain before to data
    weather['hourbefore'] = weather.Unix.astype(int)
    weather['RainBefore'] = weather.Rain.astype(int)
    newdata['hourbefore'] = newdata['Unix'] - 60 * 60
    newdata['hourbefore'] = newdata.hourbefore.astype(int)
    newdata = pandas.merge(newdata, weather[['Grid_Num', 'hourbefore', 'RainBefore']],
                           on=['hourbefore', 'Grid_Num'])
    return newdata


def main():
    # Read in our data
    # The weather file can be in either feather or csv. Feather files are used for very large files (>1 GB or so)
    # Depending on what the format of your weather file is, you'll read it in using either weather assignment line
    weather = feather.read_dataframe("../")
    # weather = pandas.read_csv("../")
    # NOTE: the add_weather method adds in any potentially missing variables, so if you already have weather variables
    # in your data file, you'll get duplicates of those columns, marked as weatherCol_x and weatherCol_y.
    # Simply remove the weather variables listed in the add_weather from your data file to avoid this
    data = pandas.read_csv("../")
    newData = add_weather(data, weather)

    newData.to_csv("../", index=False)


if __name__ == "__main__":
    main()
