import pandas
import os, sys
from datetime import datetime, timedelta
from darksky import forecast
import feather

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
    return data

##This method retrieves data from the all_weather file WITH BINARIES
def pull_binaries(data, weather):
    data['time'] = data.apply(lambda x: pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%m/%d/%y %H"),
                              axis=1)
    # This actually makes the column into the unix type
    data['time'] = data.apply(lambda x: x.time.strftime('%s'), axis=1)

    #This portion gets the hour before column
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['time'] - 60 * 60

    #The following line is needed to avoid the columnname_x problem that happens if the column already exists.
    data = data.drop(['Rain','Cloudy','Fog','Snow','Clear', 'RainBefore', 'Precipitation_Intensity'], axis=1)

    #The following three lines add the binaries, the rainbefore column, and then discards the time and hourbefore columns.
    newdata = pandas.merge(data, weather[['Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'precipIntensity', 'Grid_Block', 'time']],
                           on=['time', 'Grid_Block'])
    newdata = pandas.merge(newdata, weather[['RainBefore', "Grid_Block", 'hourbefore']],
                           on=['hourbefore', 'Grid_Block'])
    newdata = newdata.drop(['time','hourbefore'], axis=1)
    # This reorders the columns, change the different variables depending on what columns you want
    header_list = ("Accident", 'Latitude', 'Longitude', 'Date', 'Time', 'Event', 'Hour',
                       'Conditions', "EventBefore", "ConditionBefore",  "Weekday", "Precipitation_Intensity",
                       "Precip_Intensity_Max", "Clear", "Cloudy", "Rain", "Fog", "Snow", "RainBefore",
                       "Grid_Block", "Grid_Col", "Grid_Row", "Highway", "Land_Use_Mode", "Road_Count")
    newdata = newdata.reindex(columns=header_list)

    return newdata

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

##Creates the hour before column
def create_hourbefore(data):
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['time'] - 60*60  # changes the hourbefore column to be 1 hour before the time column
    return data

# Renaming some columns for later convenience, and cuts the weather file down to the columns we actually want
def concise_weatherfile(weather):
    weather['Grid_Block'] = (weather['Grid_Block']).astype(int)
    weather['time'] = weather['time'].astype(int)
    weather['Event'] = weather['icon']
    weather['Conditions'] = weather['summary']
    weather['EventBefore'] = weather['Event']
    weather['ConditionBefore'] = weather['Conditions']
    weather['hourbefore'] = weather['time'].astype(int)
    ##Cutting weather to the correct types of columns we want. 
    weather = weather[['time','Event', 'Conditions','Grid_Block','precipIntensity','hourbefore', 'EventBefore',
                           'ConditionBefore']]
    return weather

# Adds the weather from the weather file into the data file. Assumes that the weather file is straight from Darksky, 
# and has not been formatted at all. 
def add_weather(data, weather):
    print("Adding Weather")
    ##Drop this column if the data already has it, as we will be replacing it later. Otherwise, comment this out. 
    # data = data.drop(['precipIntensity'], axis=1)

    # Merge the weather variables for the hour of the accident based on time and grid block
    # Merge the event/conditions before columns based on hour before and grid block
    newdata = pandas.merge(data, weather[['EventBefore','ConditionBefore','hourbefore','Grid_Block']], on=['hourbefore','Grid_Block'])

    # Rename columns to a more convenient name. This is only if the data file already had these columns inside of it. 
    newdata['Event'] = newdata['Event_y']
    newdata['Conditions'] = newdata['Conditions_y']
    newdata['EventBefore'] = newdata['EventBefore_y']
    newdata['ConditionBefore'] = newdata['ConditionBefore_y']
    newdata["Unix"] = newdata["time"]
    # Code to aggregate weather #
    # newdata = aggregate_weather(newdata)
    return newdata


# Read in our data
weather = feather.read_dataframe("../")
data = pandas.read_csv("../")

# Saving the files: Choose which type you'd prefer
# Feather files are typically files > 800 mb
data.to_csv("../", index=False)
# feather.write_dataframe(newdata, "../")
