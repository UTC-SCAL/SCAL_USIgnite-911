"""
Authors: Jeremy Roland and Pete Way
Purpose: To match our weather data to our accident data
"""

import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
import feather
import string


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


# Finds binary variables for the given event/conditions.
def finding_binaries(data):
    data.Event = data.Event.apply(lambda x: x.lower())
    data.Conditions = data.Conditions.apply(lambda x: x.lower())
    # data.EventBefore = data.EventBefore.apply(lambda x: x.lower())
    # data.ConditionBefore = data.ConditionBefore.apply(lambda x: x.lower())

    data['Rain'] = data.apply(lambda x: 1 if ("rain" in x.Event or "rain" in x.Conditions) else 0, axis=1)
    data['Cloudy'] = data.apply(lambda x: 1 if ("cloud" in x.Event or "cloud" in x.Conditions) else 0, axis=1)
    data['Foggy'] = data.apply(lambda x: 1 if ("fog" in x.Event or "fog" in x.Conditions) else 0, axis=1)
    data['Snow'] = data.apply(lambda x: 1 if ("snow" in x.Event or "snow" in x.Conditions) else 0, axis=1)
    data['Clear'] = data.apply(lambda x: 1 if ("clear" in x.Event or "clear" in x.Conditions) else 0, axis=1)

    # data = data.drop_duplicates(subset=['Unix', 'Grid_Block'], keep='last')
    return data


# Creates the unix time column for the provided file
def make_unix_with_hour(data):
    # Taking the date and hour from the data file and converting it to the
    # year-month-day hour:minute:second format (note: it assumes minute and second are 0 if not supplied)
    data['time'] = data.apply(lambda x: pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
    # This actually makes the column
    data['time'] = data.apply(lambda x: x.time.strftime('%s'), axis=1)
    return data


# Creates datetime, which is the actual date time column, if we need it
def create_datetime_from_unix(data):
    data['dt'] = pandas.to_datetime(data['time'], unit='s', utc=True)
    return data


# Get the grid column and row of a grid block
# This was only used for the grid block layout of our grid layout, the hex layout doesn't use this
def get_gridcol_row(grid):
    for index, i in enumerate(grid.GRID_ID):
        alpha = i.split("-")[0].lower()
        if len(alpha) > 1:
            alpha = (int(string.ascii_lowercase.index(alpha[0])) + int(string.ascii_lowercase.index(alpha[1])) + 27)
        else: 
            alpha = (int(string.ascii_lowercase.index(alpha)) + 1)
        grid.at[index, 'Grid_Col'] = alpha
        grid.at[index, 'Grid_Row'] = i.split("-")[1]
        
    return grid


# A quick method to create an hourbefore column, used in the creation of the RainBefore variable
def create_hourbefore(data):
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['time'] - 60*60  # changes the hourbefore column to be 1 hour before the time column
    return data


# Adds weather from weather file into the accident file. Assumes weather file is formatted
def add_weather(data, weather):
    print("Adding Weather")
    # Set the variable types to these, as they can be finicky if not set correctly
    data.Unix = data.Unix.astype(int)
    weather.Unix = weather.Unix.astype(int)
    data.Grid_Num = data.Grid_Num.astype(int)
    weather.Grid_Num = weather.Grid_Num.astype(int)
    # Drop this column if the data already has it, as we will be replacing it later. Otherwise, comment this out.
    # data = data.drop(['precipIntensity'], axis=1)

    # Merge the data between the weather file and the accident file based on the hour, date, and grid num variables
    newdata = pandas.merge(data, weather[['Grid_Num', 'cloudCover', 'dewPoint',
                                           'humidity', 'precipIntensity', 'precipProbability', 'precipType',
                                           'pressure', 'temperature', 'Unix', 'uvIndex',
                                           'visibility', 'windBearing', 'windGust', 'windSpeed', 'Event',
                                           'Conditions', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear']],
                           on=['Unix', 'Grid_Num'])

    # Getting the RainBefore variable
    weather['hourbefore'] = weather.Unix.astype(int)
    weather['RainBefore'] = weather.Rain.astype(int)
    newdata['Unix'] = newdata['Unix'].astype(int)
    newdata['hourbefore'] = newdata['Unix'] - 60*60  # changes the hourbefore column to be 1 hour before the unix column
    newdata.hourbefore = newdata.hourbefore.astype(int)
    newdata = pandas.merge(newdata, weather[['Grid_Num', 'hourbefore', 'RainBefore']],
                           on=['hourbefore', 'Grid_Num'])
    # Code to aggregate weather if it isn't already #
    # newdata = finding_binaries(newdata)
    return newdata


def main():
    # Read in our data
    # Our weather files are in a feather format, as it is much faster to read in than if using a csv because the file
    # size is so large
    weather = feather.read_dataframe("../")
    data = pandas.read_csv("../")
    newData = add_weather(data, weather)

    newData.to_csv("../", index=False)


if __name__ == "__main__":
    main()
