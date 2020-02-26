import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
import feather
import string


# Method to log into the corresponding DarkSky or Etrims service through a file on this machine
# The file itself isn't on GitHub, so if you don't have it message Jeremy or Pete for the file
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


##finds binary variables for the given event/conditions. 
def finding_binaries(data):
    # starttime = datetime.datetime.now()
    # print("Beginning Lowercase conversion at:", starttime)
    data.Event = data.Event.apply(lambda x: x.lower())
    data.Conditions = data.Conditions.apply(lambda x: x.lower())
    data.EventBefore = data.EventBefore.apply(lambda x: x.lower())
    data.ConditionBefore = data.ConditionBefore.apply(lambda x: x.lower())
    # lowertime = datetime.datetime.now()
    # print("Lowercase conversion done, Beginning Binary Lambdas at:", lowertime - starttime)
    data['Rain'] = data.apply(lambda x : 1 if ("rain" in x.Event or "rain" in x.Conditions) else 0, axis=1)
    # raintime = datetime.datetime.now()
    # print("Rain completed in:", raintime - lowertime)
    data['Cloudy'] = data.apply(lambda x : 1 if ("cloud" in x.Event or "cloud" in x.Conditions) else 0, axis=1)
    # cloudtime = datetime.datetime.now()
    # print("Cloudy completed in:", cloudtime - raintime)
    data['Foggy'] = data.apply(lambda x : 1 if ("fog" in x.Event or "fog" in x.Conditions) else 0, axis=1)
    # fogtime = datetime.datetime.now()
    # print("Foggy completed in:", fogtime - cloudtime)
    data['Snow'] = data.apply(lambda x : 1 if ("snow" in x.Event or "snow" in x.Conditions) else 0, axis=1)
    # snowtime = datetime.datetime.now()
    # print("Snow completed in:", snowtime - fogtime)
    data['Clear'] = data.apply(lambda x : 1 if ("clear" in x.Event or "clear" in x.Conditions) else 0, axis=1)
    # cleartime = datetime.datetime.now()
    # print("Clear completed in:", cleartime - snowtime)
    data = data.drop_duplicates(subset=['Unix', 'Grid_Block'], keep='last')
    return data


# Creates the unix time column for the provided file
def make_unix_with_hour(data):
    # Taking the date and hour from the data file and converting it to the
    # year-month-day hour:minute:second format (note: apparently it assumes minute and second are 0 if not supplied)
    data['time'] = data.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
    # This actually makes the column
    data['time'] = data.apply(lambda x : x.time.strftime('%s'), axis=1)
    return data


# Creates the unix time column for the weather file (same method as above)
def make_unix_with_time(data):
    data['time'] = data.apply(lambda x : pandas.datetime.strptime(x.time, "%Y-%m-%d %H:%M:%S"), axis=1)
    data['time'] = data.apply(lambda x : x.time.strftime('%s'), axis=1)
    return data


# Creates dt, which is the actual date time column, if we need it
def create_datetime_from_unix(data):
    data['dt'] = pandas.to_datetime(data['time'],unit='s', utc=True)
    return data


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


def create_hourbefore(data):
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['time'] - 60*60  # changes the hourbefore column to be 1 hour before the time column
    return data


# Adds weather from weather file into the data file. Assumes weather file is formatted
def add_weather(data, weather):
    print("Adding Weather")
    ##Drop this column if the data already has it, as we will be replacing it later. Otherwise, comment this out.
    # data = data.drop(['precipIntensity'], axis=1)

    # Merge the weather variables for the hour of the accident based on time and grid block
    # Merge the event/conditions before columns based on hour before and grid block
    # newdata = pandas.merge(data, weather[['Grid_Block', 'Unix', 'humidity', 'windSpeed', 'windBearing', 'uvIndex',
    #                                       'precipIntensity', 'apparentTemperature', 'windGust', 'cloudCover', 'temperature',
    #                                       'dewPoint', 'visibility', 'precipType', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear',
    #                                       'RainBefore', 'cloudCover', 'dewPoint', 'ozone', 'precipAccumulation',
    #                                       'precipIntensity', 'precipProbability', 'pressure', 'Event', 'Conditions',
    #                                       'EventBefore', 'ConditionBefore', 'hourbefore']],
    #                        on=['Unix', 'Grid_Block'])

    # Applying rain before to data
    weather['hourbefore'] = weather.Unix.astype(int)
    weather['RainBefore'] = weather.Rain.astype(int)
    data.hourbefore = data.hourbefore.astype(int)
    newdata = pandas.merge(data, weather[['Grid_Num', 'hourbefore', 'RainBefore']],
                           on=['hourbefore', 'Grid_Num'])
    # Code to aggregate weather #
    # newdata = aggregate_weather(newdata)
    return newdata


def main():
    # Read in our data
    weather = feather.read_dataframe("../")
    data = pandas.read_csv("../")

    data = add_weather(data, weather)
    data.to_csv("../", index=False)


if __name__ == "__main__":
    main()
