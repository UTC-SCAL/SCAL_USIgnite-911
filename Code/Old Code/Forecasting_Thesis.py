"""
Author: Jeremy Roland
Purpose: This is a heavily altered version of Pete's OneStopForecasting_hex.py code. I've changed it to suit my needs
for thesis. This version is much less generalized and requires specific file naming schemes
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
    Remember: For forecasting, you DON'T need Accident as the first variable
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
    col8 = ['Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN', 'FUNC_CLASS',
            'precipIntensity', 'visibility', 'DayFrame', 'WeekDay', 'DayOfWeek']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)

    return dataChanged


def test_type_alt(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    This method differs from test_type in that tests 3 and 4 include the redundant variables that were removed from
    test 2
    Remember: For forecasting, you DON'T need Accident as the first variable
    """
    col3 = ['Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek']

    col4 = ['Unix', 'Hour', 'Grid_Num', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    if type == 3:
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
    # print("Scaling data")
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
    # print("\tSize of data: ", data.shape)

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
    # print("\tMin probability: ", round(float(min(probability) * 100), 2))
    # print("\tMax probability: ", round(float(max(probability) * 100), 2))
    # print("\tAccidents predicted: ", sum(data.Prediction))

    return data


# Add prediction and probability to unscaled version of data
def add_Pred_andProb(data, scaled, date):

    # Get the model's split
    if "75-25" in model or "7525" in model:
        modelsplit = "7525 Split"
    elif "50-50" in model or "5050" in model:
        modelsplit = "5050 Split"
    else:
        modelsplit = "NoSplit"
    # Get the model's negative sampling type
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

    # folder = "../Jeremy Thesis/Forecasting/" + str(date) + "/"
    folder = "../Jeremy Thesis/Forecasting/"

    # print("Adding Probability and Predicted Accidents to data file")

    ## Be sure to change this to reflect what model you are using ##
    filename = folder + suffix + "Forecast_" + str(date) + ".csv"

    data['Prediction'] = scaled['Prediction'].astype(int)
    data['Probability'] = scaled['Probability'].astype(float)
    # Include this to drop any potential predictions that didn't go through
    # This mainly would be used if the data you use causes some variables to be dropped, making the code think there
    # are duplicates
    data.dropna(subset=['Prediction'], inplace=True)
    print("\tSaving forecasted data to: ", filename)
    data.to_csv(filename, sep=",", index=False)
    return scaled, data


def featureSelectionAlter(data, model):
    """
    A method to change the columns based on the model type, split, and test type
    NOTE: this only covers the models I wanted to test for Thesis work, which are the models in the main section
        of the code
    Remember: For forecasting, you DON'T need Accident as the first variable
    """
    if "TS" and "50-50" and "Test1" in model:
        fs_data = data.reindex(columns=['Join_Count', 'Hour', 'DayFrame', 'Latitude', 'Longitude', 'Grid_Num',
                                     'Unix', 'humidity', 'windSpeed', 'uvIndex', 'temperature', 'dewPoint',
                                     'pressure', 'visibility', 'cloudCover'])
    elif "TS" and "50-50" and "Test2" in model:
        fs_data = data.reindex(columns=['Join_Count', 'DayFrame', 'Grid_Num', 'temperature', 'humidity',
                                     'windSpeed', 'pressure', 'visibility', 'cloudCover', 'uvIndex',
                                     'DayOfWeek', 'precipIntensity', 'FUNC_CLASS', 'NBR_LANES', 'WeekDay'])
    elif "TS" and "75-25" and "Test1" in model:
        fs_data = data.reindex(columns=['Join_Count', 'Latitude', 'Hour', 'Longitude', 'DayFrame', 'uvIndex', 'Unix',
                                        'Grid_Num', 'humidity', 'windSpeed', 'temperature', 'dewPoint', 'pressure',
                                        'visibility', 'cloudCover'])
    elif "SS" and "75-25" and "Test1" in model:
        fs_data = data.reindex(columns=['Join_Count', 'Latitude','Longitude','Unix','uvIndex','Grid_Num','humidity',
                                        'windSpeed','temperature','Hour','dewPoint','pressure','visibility', 'DayFrame',
                                        'cloudCover'])
    elif "TS" and "NoSplit" and "Test1" in model:
        fs_data = data.reindex(columns=['Join_Count', 'Latitude', 'Longitude', 'Hour', 'uvIndex', 'Unix', 'humidity',
                                        'DayFrame', 'temperature', 'Grid_Num', 'dewPoint', 'windSpeed', 'pressure',
                                        'visibility', 'cloudCover'])
    elif "TS" and "NoSplit" and "Test2" in model:
        fs_data = data.reindex(columns=['Join_Count', 'temperature', 'humidity', 'windSpeed', 'pressure', 'DayFrame',
                                        'uvIndex', 'Grid_Num', 'visibility', 'cloudCover', 'DayOfWeek',
                                        'precipIntensity', 'FUNC_CLASS', 'NBR_LANES', 'WeekDay'])
    else:
        print("Error in determining which feature selection is applied")
        print(model)
        exit()
    return fs_data


model = ''
# Have a list of the days you want to predict for
# Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
dates = []

for date in dates:
    print("Date is ", date)
    # This file read-in requires that the date provided match the format of the date in the file name
    data = pandas.read_csv("../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))

    # print(model)
    # These determine what variables to keep
    if 'Test1' in model:
        data = test_type(data, 1)
        testType = 1
    elif 'Test2' in model:
        data = test_type(data, 2)
        testType = 2
    elif 'Test3' in model:
        data = test_type(data, 3)
        # data = test_type_alt(data, 3)
        testType = 3
    elif 'Test4' in model:
        data = test_type(data, 4)
        # data = test_type_alt(data, 4)
        testType = 4
    else:
        print("Error in Test type assignment")
        exit()
    # Code to alter the columns of the data if the model being used has feature selection applied
    if 'FeatSelect' in model:
        # this is the extratreesclassifier feature selection, which is the default feature selection for our MLP model
        data = featureSelectionAlter(data, model)

    scaled = standarize_data(data)
    scaled = predict_accidents(scaled, model)
    scaled, data = add_Pred_andProb(data, scaled, date)
