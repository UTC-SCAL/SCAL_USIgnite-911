"""
This is a heavily altered version of Pete's OneStopForecasting_hex.py code. I've changed it to suit my needs for thesis
This version is much less generalized and requires specific file naming schemes
"""
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import logging

logging.getLogger('tensorflow').disabled = True
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn import preprocessing

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib

    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """
    col1 = ['Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col2 = ['Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col3 = ['Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek']

    col4 = ['Grid_Num', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)

    return dataChanged


# Standardize Data.
def standarize_data(data):
    """
    This standardizes the data into the MinMaxReduced version used for model creation
    """
    beginLen = len(data.values)
    dataDropped = data.drop_duplicates(keep='first')
    print("Dropped ", beginLen - len(dataDropped) , " duplicates")
    print("Scaling data")
    # Drop any empties now, since we don't want empties here!
    dataDropped = dataDropped.dropna()
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    dataScaled = scaler.fit_transform(dataDropped)
    dataScaled = pandas.DataFrame(dataScaled, columns=dataDropped.columns)
    return dataScaled


# Predict for accidents
# Data is SCALED version of data, and modelname is the path to the model.
def predict_accidents(data, modelname):
    print("Predicting Accident Hotspots with model: ", modelname)

    ##################################################################################################################
    # This section makes sure that the correct columns are in the data files, just in case.
    data = data.dropna()
    X = data.columns.shape[0]
    ##################################################################################################################
    # Printing the size of the testing data, that is, the data file.
    print("\tSize of data: ", data.shape)

    # Creating the framework for the model.

    #  These lines are used for the forecasting, because for some reason the above code doesn't like to work
    #  for any files that I try to run, so I'm keeping this here for future use
    model = Sequential()
    model.add(Dense(X, input_dim=X, activation='sigmoid'))
    model.add(Dense(X - 5, activation='sigmoid'))
    model.add(Dropout(.1))
    try:
        model.add(Dense(X - 10, activation='sigmoid'))
    except:
        model.add(Dense(X - 5, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

    # Our current set model.
    model.load_weights("../" + modelname)
    ##################################################################################################################
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


# Add prediction and probability to unscaled version of data
def add_Pred_andProb(data, scaled,date):

    # Get the model's split
    if "75-25" in model or "7525" in model:
        modelsplit = "7525 Split"
    elif "50-50" in model or "5050" in model:
        modelsplit = "5050 Split"
    else:
        modelsplit = "NoSplit"
    # Get the model's type
    if "GF" in model:
        modeltype = "GF"
    elif "TS" in model:
        modeltype = "TS"
    elif "DS" in model:
        modeltype = "DS"
    elif "HS" in model:
        modeltype = 'HS'
    elif "SS" in model:
        modeltype = "SS"
    else:
        print("Error in make_directory modeltype name")
        exit()
    # Check if the model used had feature selection or not
    if 'FeatSelect' in model:
        suffix = modeltype + "_" + modelsplit + "_FeatSelect_Test" + str(testType)
    else:
        suffix = modeltype + "_" + modelsplit + "_Test" + str(testType)

    folder = "../Jeremy Thesis/Forecasting/" + str(date) + "/"

    print("Adding Probability and Predicted Accidents to data file")
    filename = folder + suffix + "Forecast.csv"
    data['Prediction'] = scaled['Prediction'].astype(float)
    data['Probability'] = scaled['Probability'].astype(float)
    missing = data['Probability'].isnull().sum()
    print("\tLength of Data Probability:", len(data) - missing)
    print("\tSaving forecasted data to: ", filename)
    data.to_csv(filename, sep=",", index=False)
    return scaled, data


# Find matches, using either the original DayFrames, or the alternate.
def finding_matches(accidents, data):
    data = data[data['Prediction'] == 1]
    match = 0

    for i, _ in enumerate(accidents.values):
        for j, _ in enumerate(data.values):
            if (accidents.Grid_Num.values[i] == data.Grid_Num.values[j] and accidents.DayFrame.values[i] ==
                    data.DayFrame.values[j]):
                match += 1
    print("This many matches were found: ", match)


# Just a commented out list to remind myself what models I want to use
# modelsForThesis = ['Jeremy Thesis/Total Shift/Model Results/model_TS_50-50Split_Test1.h5',
#           'Jeremy Thesis/Total Shift/Model Results/model_TS_50-50Split_FeatSelect_Test1.h5',
#           'Jeremy Thesis/Total Shift/Model Results/model_TS_50-50Split_Test2.h5',
#           'Jeremy Thesis/Spatial Shift/Model Results/model_SS_50-50Split_Test1.h5',
#           'Jeremy Thesis/Total Shift/Model Results/model_TS_50-50Split_FeatSelect_Test2.h5']
# Read in the model you want to use
model = ''
# Have a list of the days you want to predict for
# Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
dates = ['1-1-2020', '1-2-2020', '1-3-2020', '1-4-2020', '1-5-2020', '1-6-2020', '1-7-2020']

for date in dates:
    print("Date is ", date)
    # This file read-in requires that the date provided match the format of the date in the file name
    data = pandas.read_csv("../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))

    print(model)
    # These determine what variables to keep
    if 'Test1' in model:
        data = test_type(data, 1)
        testType = 1
    elif 'Test2' in model:
        data = test_type(data, 2)
        testType = 2
    elif 'Test3' in model:
        data = test_type(data, 3)
        testType = 3
    elif 'Test4' in model:
        data = test_type(data, 4)
        tesType = 4
    else:
        print("Error in Test type assignment")
        exit()
    # This conditional changes the column values for the two feature selection based models I was using. It's very
    # situational, so I'm not going to bother generalizing it for any model that used feature selection
    if 'FeatSelect' in model:
        if "TS" and "50-50" and "Test1" in model:
            data = data.reindex(columns=['Join_Count', 'Hour', 'DayFrame', 'Latitude', 'Longitude', 'Grid_Num',
                                         'Unix', 'humidity', 'windSpeed', 'uvIndex', 'temperature', 'dewPoint',
                                         'pressure', 'visibility', 'cloudCover'])
        elif "TS" and "50-50" and "Test2" in model:
            data = data.reindex(columns=['Join_Count', 'DayFrame', 'Grid_Num', 'temperature', 'humidity',
                                         'windSpeed', 'pressure', 'visibility', 'cloudCover', 'uvIndex',
                                         'DayOfWeek', 'precipIntensity', 'FUNC_CLASS', 'NBR_LANES',	'WeekDay'])

    scaled = standarize_data(data)
    scaled = predict_accidents(scaled, model)
    scaled, data = add_Pred_andProb(data, scaled, date)

    # Finding matches:
    # finding_matches(accidents, data)
    # finding_matches_alt(accidents, data)
