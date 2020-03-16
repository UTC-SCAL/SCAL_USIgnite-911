import datetime
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import logging

logging.getLogger('tensorflow').disabled = True
import pandas
import feather
from keras.layers import Dense, Dropout
from keras.models import Sequential
# from tensorflow.keras.models import Sequential
from sklearn import preprocessing
from darksky.forecast import Forecast
import time
import pytz
from datetime import timedelta
import feather

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib

    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt


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


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """
    col1 = ['Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col2 = ['Clear', 'Cloudy', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col3 = ['Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col4 = ['Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
             'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
             'WeekDay', 'cloudCover', 'precipIntensity']

    col5 = ['Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
             'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
             'WeekDay', 'cloudCover', 'precipIntensity']

    col6 = ['Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']
    if type == 1:
        data = data.reindex(columns=col1)
    elif type == 2:
        data = data.reindex(columns=col2)
    elif type == 3:
        data = data.reindex(columns=col3)
    elif type == 4:
        data = data.reindex(columns=col4)
    elif type == 5:
        data = data.reindex(columns=col5)
    elif type == 6:
        data = data.reindex(columns=col6)

    return data


##Step 0 - ONLY IF NEEDED. This takes a listing of gridblocks and creates the full forecast file
def fillForecastFile(places, filename):
    ##Gets the forecast data for every 4 hours. 
    fulldata = places.copy()
    for i in range(0, 25, 4):
        if i == 0:
            pass
        else:
            name = ('places' + str(i))
            print(name)
            if i == 24:
                places.Hour = 23
            else:
                places.Hour = i
            # if 0<=i<7 or 19<=i<=23:
            #     places.DayFrame = 1
            # elif 7<=i<10:
            #     places.DayFrame = 2
            # elif 10<=i<13:
            #     places.DayFrame = 3
            # elif 13<=i<19:
            #     places.DayFrame = 4
            print(places.Hour[0:5])
            fulldata = fulldata.append(places)
    fulldata = fulldata.drop_duplicates()
    print("Finished data size:", fulldata.size)
    fulldata.to_csv(filename, sep=",", index=False)


##Step 0 - ONLY IF NEEDED. Creates binary variables for weather if not already in data
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
    weatherFile.Event = weatherFile.Event.apply(lambda x: x.lower() if pandas.notnull(x) else "empty")
    weatherFile.Conditions = weatherFile.Conditions.apply(lambda x: x.lower() if pandas.notnull(x) else "empty")
    # Here, in the lambda functions, we use if, else, and elif statements for finding Event and Condition entries that
    # are NoneType, as darksky doesn't always have the answer for us.
    weatherFile['Rain'] = weatherFile.apply(lambda x: 1 if ("rain" in x.Event or "rain" in x.Conditions)
    else ("-1" if "empty" in x.Event and "empty" in x.Conditions else 0), axis=1)
    weatherFile['Cloudy'] = weatherFile.apply(lambda x: 1 if ("cloud" in x.Event or "cloud" in x.Conditions)
    else ("-1" if "empty" in x.Event and "empty" in x.Conditions else 0), axis=1)
    weatherFile['Foggy'] = weatherFile.apply(lambda x: 1 if ("fog" in x.Event or "fog" in x.Conditions)
    else ("-1" if "empty" in x.Event and "empty" in x.Conditions else 0), axis=1)
    weatherFile['Snow'] = weatherFile.apply(lambda x: 1 if ("snow" in x.Event or "snow" in x.Conditions)
    else ("-1" if "empty" in x.Event and "empty" in x.Conditions else 0), axis=1)
    weatherFile['Clear'] = weatherFile.apply(lambda x: 1 if ("clear" in x.Event or "clear" in x.Conditions)
    else ("-1" if "empty" in x.Event and "empty" in x.Conditions else 0), axis=1)

    weatherFile.Rain = weatherFile.Rain.astype(int)
    weatherFile.Cloudy = weatherFile.Cloudy.astype(int)
    weatherFile.Foggy = weatherFile.Foggy.astype(int)
    weatherFile.Snow = weatherFile.Snow.astype(int)
    weatherFile.Clear = weatherFile.Clear.astype(int)
    return weatherFile


##Step 1 - Connect Weather to Forecast
def finding_weather(data, all_weather, yoa, moa, dayoa):
    print("Finding Weather for Forecast date of:", moa, "/", dayoa, "/", yoa)
    data['Unix'] = 0
    data['hourbefore'] = 0
    # If the data you are working with doesn't have an hour value, run the forloop below to create it
    # data['Hour'] = 0
    # date = str(moa) + "/" + str(dayoa) + "/" + str(yoa)
    # for i, values in enumerate(data.values):
    #     data.Hour.values[i] = data['Response.Date'].values[i].split(" ")[1].split(":")[0]
    data['Hour'] = data['Hour'].astype(int)
    data['Unix'] = data['Hour'].map(lambda x: datetime.datetime(yoa, moa, dayoa, x, 0, 0).strftime('%s'))
    data.Unix = data.Unix.astype(int)

    data['hourbefore'] = data['Unix'].map(lambda x: x - 60 * 60)
    data['hourbefore'] = data['hourbefore'].astype(int)
    all_weather['hourbefore'] = all_weather.Unix.astype(int)
    all_weather['RainBefore'] = all_weather.Rain.astype(int)
    data['DayOfWeek'] = 0
    data['WeekDay'] = 0
    data['DayFrame'] = 0
    data.DayFrame = data.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23
        else (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    print("Beginning length:", len(data))
    # Merge the event/conditions columns based on time and grid block
    newdata = pandas.merge(data, all_weather[['cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
                                              'pressure', 'temperature', 'visibility', 'windGust', 'windSpeed', 'Rain',
                                              'Cloudy', 'Foggy', 'Snow',
                                              'Clear', 'Unix', 'Grid_Num']], on=['Unix', 'Grid_Num'])
    # Merge the event/conditions before columns based on hour before and grid block
    print("Mid length:", len(newdata))
    # exit()
    newdata = pandas.merge(newdata, all_weather[['Grid_Num', 'hourbefore', 'RainBefore']],
                           on=['hourbefore', 'Grid_Num'])
    for i, values in enumerate(newdata.values):
        timestamp = str(date) + " " + str(newdata.Hour.values[i])
        # A try/except statement for taking in what format the date is in, because 911 are buttheads
        try:
            thisDate = datetime.datetime.strptime(timestamp, "%m/%d/%Y %H")
        except:
            thisDate = datetime.datetime.strptime(timestamp, "%m/%d/%y %H")
        newdata.DayOfWeek.values[i] = thisDate.weekday()
    newdata.WeekDay = newdata.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    print("Final length:", len(newdata))
    print("Weather fetch complete")
    # newdata = newdata[['Unix', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'FUNC_CLASS',
    #    'Hour', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
    #    'pressure', 'temperature', 'visibility', 'windGust', 'windSpeed',
    #    'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']]
    if len(newdata) == 0:
        print("Weather pull failed. Select Different Date")
        exit()
    return newdata


def fetchWeather(date):
    """
        Ok, so, this code is a modified version of Jeremy's from updatingWeatherFiles. However, this one is adjusted for use in fetching weather we don't have yet. 
        (So future predictions.)
    """
    print("Fetching Weather")

    # Read in the center points file to get the used grid locations and their lat/longs
    forecastforum = pandas.read_csv("Excel & CSV Sheets/Grid Hex Layout/Forecast Forum Hex Layout.csv")

    ##First Batch Columns
    # columns = ['cloudCover','dewPoint','humidity','precipIntensity','pressure','temperature','visibility',
    # 'windGust','windSpeed','icon','summary']
    ##Second Batch Columns 
    columns = ['cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'precipProbability', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windBearing', 'windGust', 'windSpeed', 'icon', 'summary']

    key = find_cred("darksky")
    for k, i in enumerate(forecastforum.Grid_Num.values):
        lati = forecastforum.Latitude.values[k]
        longi = forecastforum.Longitude.values[k]
        j = str(date)
        year = int(j.split("-")[0])
        month = int(j.split("-")[1])
        day = int(j.split("-")[2])
        hour = forecastforum.Hour.values[k]
        if hour == 0:
            print(i)
            t = datetime.datetime(year, month, day, hour, 0, 0).isoformat()
            call = key, lati, longi
            # try: 
            forecastcall = Forecast(*call, time=t)
            hourly_list = [item._data for item in forecastcall.hourly]
            for l, _ in enumerate(hourly_list):
                if l == 0:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                    yesterday = datetime.datetime.strptime(date, '%Y-%m-%d') - timedelta(hours=1)
                    t2 = yesterday.isoformat()
                    call = key, lati, longi
                    forecastcallyesterday = Forecast(*call, time=t2)
                    hourly_listyesterday = [item._data for item in forecastcallyesterday.hourly]
                    entryyesterday = hourly_listyesterday[23]
                    if 'rain' in entryyesterday['icon'].lower() or 'rain' in entryyesterday['summary'].lower():
                        forecastforum.at[k, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k, 'RainBefore'] = 0
                elif l == 3:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 1, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 1, 'RainBefore'] = 0
                elif l == 4:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 1, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                elif l == 7:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 2, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 2, 'RainBefore'] = 0
                elif l == 8:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 2, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                elif l == 11:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 3, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 3, 'RainBefore'] = 0
                elif l == 12:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 3, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                elif l == 15:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 4, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 4, 'RainBefore'] = 0
                elif l == 16:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 4, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                elif l == 19:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 5, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 5, 'RainBefore'] = 0
                elif l == 20:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 5, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                elif l == 22:
                    entry = hourly_list[l]
                    if 'rain' in entry['icon'].lower() or 'rain' in entry['summary'].lower():
                        forecastforum.at[k + 6, 'RainBefore'] = 1
                    else:
                        forecastforum.at[k + 6, 'RainBefore'] = 0
                elif l == 23:
                    entry = hourly_list[l]
                    for d, things in enumerate(hourly_list[l]):
                        if things in columns:
                            try:
                                forecastforum.at[k + 6, things] = entry[things]
                            except:
                                print("Failure at DarkSky")
                else:
                    pass
    # print(forecastforum.head())
    forecastforum.columns = ['Event' if x == 'icon' else 'Conditions' if x == 'summary' else x for x in
                             forecastforum.columns]
    forecastforum = finding_binaries(forecastforum)
    # forecastforum.to_csv("/Users/peteway/Desktop/Testing_NS.csv")
    # exit()
    print("Forecast Fetched.")
    # exit()
    return forecastforum
    # except:
    #     print("Error at Darksky:", call, t)


##Step 2 - Standardize Data.
def standarize_data(data):
    data = data.drop_duplicates(keep='first')
    print("Scaling data")
    # Drop any empties now, since we don't want empties here!
    data = data.dropna()

    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled = scaler.fit_transform(data)
    scaled = pandas.DataFrame(scaled, columns=data.columns)

    # Send it back
    print("Data Scale Complete")
    return scaled, data


##Step 3 - Predict for accidents
##Data is SCALED version of data, and modelname is the path to the model. 
def predict_accidents(data, modelname):
    print("Predicting Accident Hotspots with model:", modelname)

    ########################################################################################################################################################################

    ##This section makes sure that the correct columns are in the data files, just in case.
    data = data.dropna()
    X = data.columns.shape[0]
    ########################################################################################################################################################################
    # Printing the size of the testing data, that is, the data file.
    print("\tSize of data:", data.shape)

    # #Creating the framework for the model.
    # # creating the model
    # model = Sequential()
    # ##X.shape[1] is the number of columns inside of X.
    # # Use for standard sized variable set
    # model.add(Dense(X-5, activation='sigmoid'))
    # model.add(Dense(X-10, activation='sigmoid'))
    #
    # model.add(Dense(1, activation='sigmoid'))
    #
    # ##Compiling a model, and pulling in the saved weights.
    # model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])

    ## These lines are used for the forecasting, because for some reason the above code doesn't like to work
    ## for any files that I try to run, so I'm keeping this here for future use
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X.
    model.add(Dense(X, input_dim=X, activation='sigmoid'))

    # Use for standard sized variable set
    model.add(Dense(X - 5, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(X - 10, activation='sigmoid'))

    model.add(Dense(1, activation='sigmoid'))

    ##Our current set model.
    model.load_weights(modelname)
    ########################################################################################################################################################################
    # Okay, now let's calculate predictions.
    probability = model.predict(data)
    # Save the predicted values to the Probability column.
    data["Probability"] = probability

    # Then, let's round to either 0 or 1, since we have only two options (accident or no).
    predictions_round = [abs(round(x[0])) for x in probability]
    data["Prediction"] = predictions_round

    # Printing some of the found values, as well as the total number of predicted accidents for this data.
    print("\tMin probability: ", round(float(min(probability) * 100), 2))
    print("\tMax probability: ", round(float(max(probability) * 100), 2))
    print("\tAccidents predicted: ", sum(data.Prediction))

    return data


##Step 3 - Predict for accidents (This version is slightly tweaked to work with the averaged weekday models)
##Data is SCALED version of data, filename is title to save predicted forecast under,
##testnum is the Chosen test number, and modelname is the path to the model.
def predict_accidents_weekdays(data, modelname):
    print("Predicting Accident Hotspots with Test number", testnum, " and model:", modelname)

    ########################################################################################################################################################################

    ##This section makes sure that the correct columns are in the data files, just in case.
    data = data.dropna()
    X = data.columns.shape[0]
    ########################################################################################################################################################################
    # Printing the size of the testing data, that is, the data file.
    print("\tSize of data:", data.shape)

    # Creating the framework for the model.
    # creating the model
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X.
    model.add(Dense(X, input_dim=X, activation='sigmoid'))
    # Use for standard sized variable set
    model.add(Dense(X - 5, activation='sigmoid'))
    model.add(Dropout(.1))  # Uncommented this to match weekday ang model layout
    model.add(Dense(X - 10, activation='sigmoid'))

    model.add(Dense(1, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))  # Added to match weekday avg model layout

    ##Compiling a model, and pulling in the saved weights.
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])

    ##Our current set model. Min max reduced.
    model.load_weights(modelname)

    ########################################################################################################################################################################
    # Okay, now let's calculate predictions.
    probability = model.predict(data)
    # Save the predicted values to the Probability column.
    data["Probability"] = probability

    # Then, let's round to either 0 or 1, since we have only two options (accident or no).
    predictions_round = [abs(round(x[0])) for x in probability]
    data["Prediction"] = predictions_round

    # Printing some of the found values, as well as the total number of predicted accidents for this data.
    print("\tMin probability: ", round(float(min(probability) * 100), 2))
    print("\tMax probability: ", round(float(max(probability) * 100), 2))
    print("\tAccidents predicted: ", sum(data.Prediction))

    return data


##Step 4 - Add results to unscaled version of data
##Add Prediction and Probability to the unscaled version of the data. 
def add_Pred_andProb(data, scaled, folder, suffix):
    print("Adding Probability and Predicted Accidents to data file")
    scaledfile = "../" + folder + "MMR/" + suffix + "MMR.csv"
    filename = "../" + folder + "Forecast/" + suffix + "Forecast.csv"
    scaled['Prediction'] = scaled['Prediction'].astype(int)
    scaled['Probability'] = scaled['Probability'].astype(float)
    missing = scaled['Probability'].isnull().sum()
    data['Prediction'] = scaled['Prediction']
    data['Probability'] = scaled['Probability']
    missing = data['Probability'].isnull().sum()
    print("\tLength of Data Probability:", len(data) - missing)
    print("\tSaving forecasted data to: ", filename)
    # scaled.to_csv(scaledfile, sep=",", index=False)
    data.to_csv(filename, sep=",", index=False)
    return scaled, data


##Step 5 - Find matches, using either the original DayFrames, or the alternate. 
def finding_matches(accidents, data):
    data = data[data['Prediction'] == 1]
    match = 0

    for i, _ in enumerate(accidents.values):
        for j, _ in enumerate(data.values):
            if (accidents.Grid_Num.values[i] == data.Grid_Num.values[j] and accidents.DayFrame.values[i] ==
                    data.DayFrame.values[j]):
                match += 1
    print("This many matches were found:", match)


def make_DayFrameAlt(data):
    data["DayFrameAlt"] = ""
    data.Hour = data.Hour.astype(int)
    for i, _ in enumerate(data.values):
        if 6 <= data.Hour.values[i] <= 12:
            data.DayFrameAlt.values[i] = 1
        elif 13 <= data.Hour.values[i] <= 18:
            data.DayFrameAlt.values[i] = 2
        elif 19 <= data.Hour.values[i] <= 23 or 0 <= data.Hour.values[i] <= 5:
            data.DayFrameAlt.values[i] = 3
    return data


def finding_matches_alt(accidents, data):
    data = make_DayFrameAlt(data)
    accidents = make_DayFrameAlt(accidents)
    data = data[data['Prediction'] == 1]
    altmatch = 0
    for i, _ in enumerate(accidents.values):
        for j, _ in enumerate(data.values):
            if (accidents.Grid_Num.values[i] == data.Grid_Num.values[j] and accidents.DayFrameAlt.values[i] ==
                    data.DayFrameAlt.values[j]):
                altmatch += 1
    print("This many ALT matches were found:", altmatch)


def make_directory(model, batchnum, date):
    modeltype = (model.split("/")[-1]).split("_")[1]
    if "75-25" in model or "7525" in model:
        modelsplit = "75-25 Split"  ##75-25
    elif "50-50" in model or "5050" in model:
        modelsplit = "50-50 Split"  ##50-50
    else:
        modelsplit = "NoSplit"  ##Original

    if "GF" in model:
        modeltype = "GF"
    elif "TS" in model:
        modeltype = "TS"

    if batchnum == 1:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"
    elif batchnum == 2:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"
    elif batchnum == 3:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"
    elif batchnum == 4:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"
    elif batchnum == 5:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"
    elif batchnum == 6:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(batchnum)
        # date = (date.split("-")[1]) + "-" + (date.split("-")[2]) + "-" + (date.split("-")[0])
        folder = "Excel & CSV Sheets/Forecasts/" + date + "/Hex/"

    print("\tSaving Folder:", folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    folderMMR = "../Excel & CSV Sheets/Forecasts/" + date + "/Hex/MMR/"
    if not os.path.exists(folderMMR):
        os.makedirs(folderMMR)

    folderpred = "../Excel & CSV Sheets/Forecasts/" + date + "/Hex/TestingforPredictions/"
    if not os.path.exists(folderpred):
        os.makedirs(folderpred)

    folderfore = "../Excel & CSV Sheets/Forecasts/" + date + "/Hex/Forecast/"
    if not os.path.exists(folderfore):
        os.makedirs(folderfore)

    return folder, suffix


# This version of make_directory is a little less specific with naming
def make_directory_alt(model):
    modeltype = (model.split("/")[-1]).split(".")[0]
    folder = "Excel & CSV Sheets/Forecasts/" + date + "/"
    suffix = modeltype + "_"
    print("\tSaving Folder:", folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder, suffix


def return_empty_df(dataframe):
    """
    A quick utility method to return a sub dataframe that only has the rows that are missing values in a certain column
    :param dataframe: the dataframe you want to search through
    :return: a smaller dataframe containing the rows with missing values in the desired column
    """
    nullFile = dataframe[dataframe['Event'].isnull()]
    nullFile.to_csv("../")


#######################################################################################################################
# start = datetime.datetime.now()
date = "01-23-2020"
# optional year month day variables for convenient, only if you need them
year = int(date.split("-")[2])
month = int(date.split("-")[0])
day = int(date.split("-")[1])
weather = feather.read_dataframe("../Ignore/2020 Weather Mar 13.feather")

##REMEMBER TO SET WHICH BATCH COLUMN VERISON!!!
# This is the file that has the accidents for the date you want to predict for
data = pandas.read_csv("../Excel & CSV Sheets/Forecast Accident Dates/01-23-2020 Forecast.csv")
# data = finding_weather(data, weather, year, month, day)
testnum = 4
data = test_type(data, testnum)
# Save the data with the added weather if you want/need to
# data.to_csv("../Excel & CSV Sheets/Forecast Accident Dates/" + date + " Forecast.csv", index=False)
# exit()
# print(data.isnull().sum(axis = 0))    ##Finds number of NAs per column 

scaled, data = standarize_data(data)


modelname = "../"
scaled = predict_accidents(scaled, modelname)  # This version is used for our original models

folder, suffix = make_directory(modelname, testnum, date)

scaled, data = add_Pred_andProb(data, scaled, folder, suffix)

# data.to_csv("/Users/peteway/Desktop/Testing.csv")
# end = datetime.datetime.now()
# print("Forecasting Completed in:", end - start)
exit()

# Use this command and the two lines at the bottom of this file if you want to time this code
# start = datetime.datetime.now()

# This is a template for the forecasting file created with this code
origdata = pandas.read_csv(
    "Excel & CSV Sheets/Hamilton County Accident System Hex/Forecasting/Forecast Forum Hex Layout.csv", sep=",")

weather19 = feather.read_dataframe("../Ignore/HexWeather/2019 Weather Binaries.feather")
weather18 = feather.read_dataframe("../Ignore/HexWeather/2018 Weather Binaries.feather")
weather17 = feather.read_dataframe("../Ignore/HexWeather/2017 Weather Binaries.feather")

weather19["Grid_Num"] = weather19["Grid_Num"].astype(int)
weather19['hourbefore'] = weather19['Unix']
weather19['RainBefore'] = weather19['Rain']

weather18["Grid_Num"] = weather18["Grid_Num"].astype(int)
weather18['hourbefore'] = weather18['Unix']
weather18['RainBefore'] = weather18['Rain']

weather17["Grid_Num"] = weather17["Grid_Num"].astype(int)
weather17['hourbefore'] = weather17['Unix']
weather17['RainBefore'] = weather17['Rain']

##Adjusting column types and such
origdata['Hour'] = origdata['Hour'].astype(int)

##Which test version to run the model on, date wanted to predict for. 


models = ["Graphs & Images/Hex Grid/Grid Fix/Cut 75-25/model_GF_hex_uncut.h5",
          "Graphs & Images/Hex Grid/Grid Fix/Cut 50-50/model_GF_hex_uncut.h5",
          "Graphs & Images/Hex Grid/Grid Fix/Second Run/model_GF_hex_uncut.h5",
          "Graphs & Images/Hex Grid/Random/Cut 50-50/model_rand_hex.h5",
          "Graphs & Images/Hex Grid/Random/Cut 75-25/model_rand_hex.h5",
          "Graphs & Images/Hex Grid/Random/First Run/model_rand_uncut.h5"]
dates = ["1/1/2019", "2/4/2018", "3/12/2017", "3/17/2019", "4/12/2019", "4/22/2018", "5/11/2019", "5/16/2017",
         "7/9/2017", "8/16/2018"]

# model = "Graphs & Images/Hex Grid/Grid Fix/Cut 75-25/model_GF_hex_uncut.h5"
# model = "Graphs & Images/Hex Grid/Grid Fix/Cut 50-50/model_GF_hex_uncut.h5"
# model = "Graphs & Images/Hex Grid/Grid Fix/Second Run/model_GF_hex_uncut.h5"

##Full Ran 
# model = "Graphs & Images/Hex Grid/Random/Cut 50-50/model_rand_hex.h5"
# model = "Graphs & Images/Hex Grid/Random/Cut 75-25/model_rand_hex.h5"
# model = "Graphs & Images/Hex Grid/Random/First Run/model_rand_uncut.h5"

# date = "1/1/2019"
columns = ['Unix', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'FUNC_CLASS',
           'Hour', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
           'pressure', 'temperature', 'visibility', 'windGust', 'windSpeed',
           'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
accidentfile = "Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/Hex Forecast Accidents.csv"
accidentfile = pandas.read_csv(accidentfile)
# print(accidentfile.Date.values[0])
# exit()
for date in dates:
    print("Date is ", date)

    accidents = accidentfile[accidentfile['Date'] == date]
    accidents = accidents.reindex(columns=columns)

    year = int(date.split("/")[2])
    month = int(date.split("/")[0])
    day = int(date.split("/")[1])

    # Read in the weather file you want to use
    if year == 2018:
        all_weather = weather18
    elif year == 2017:
        all_weather = weather17
    elif year == 2019:
        all_weather = weather19
    else:
        print("Error with year:", year, date)

    # Based on how the file name has the date ordered, choose a date declaration to use
    # date = str(year)+"-"+str(month)+"-"+str(day)
    date = str(month) + "-" + str(day) + "-" + str(year)

    ##Step 1 - Add weather
    data = finding_weather(origdata, all_weather, year, month, day)

    # print(scaled.columns)
    # exit()

    ##Step 3 - Predict for Accidents on Given Day - returns scaled version of data
    # Order of parameters - Scaled, testnumber, modelfilename
    for model in models:
        print(model)
        ##Step 2 - Standardize Data - returns scaled version 
        columns = ['Unix', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'FUNC_CLASS',
                   'Hour', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
                   'pressure', 'temperature', 'visibility', 'windGust', 'windSpeed',
                   'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
        data = data[columns]
        scaled, data = standarize_data(data)

        scaled = scaled[columns]
        scaled = predict_accidents(scaled, model)  # This version is used for our original models

        ##Step 4 - Add results to unscaled data - saves data to given filename. 
        # Order of parameters - data, scaled, folder to save forecast under
        # Choose which make_directory method you want to use, they both do the same thing but the alt version is simplified
        folder, suffix = make_directory(model)  # Use this method for the original models
        # folder, suffix = make_directory_alt(model)

        scaled, data = add_Pred_andProb(data, scaled, folder, suffix)

        ##Step 5 - Finding matches:
        print("Accidents Occurred: ", len(accidents))
        # finding_matches(accidents, data)
        # finding_matches_alt(accidents, data)

        # Timing the code, if you want
        # end = datetime.datetime.now()
        # print("Testing completed in:", end-start)
    data = origdata
