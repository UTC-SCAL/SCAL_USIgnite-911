"""
A general file to hold all of my misc methods I've made during my thesis research
"""
import time
from datetime import datetime
import plotly.express as px
import pandas
from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot
from sklearn import preprocessing
import geopy.distance
from sklearn.decomposition import PCA
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.utils import shuffle
import numpy


def automatedModelAverageAggregator():
    """
    Method to read in all the files that have the model averages, and do an automated calculation of their column
    averages and placing them into a separate file
    """
    files = []

    columns = ['Model', 'Train_Acc', 'Train_Loss', 'Test_Acc', 'Test_Loss', 'AUC', 'TN', 'FP', 'FN', 'TP', 'Accuracy',
               'Precision', 'Recall', 'Specificity', 'FPR']

    averageFile = pandas.DataFrame(columns=columns)
    rowNum = 0

    for file in files:
        data = pandas.read_csv("../%s" % file)
        print(rowNum)
        if "Grid Fix" in file:
            if "FeatSelect" in file:
                modelName = "GF " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "GF " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Hour Shift" in file:
            if "FeatSelect" in file:
                modelName = "HS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "HS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Spatial Shift" in file:
            if "FeatSelect" in file:
                modelName = "SS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "SS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Total Shift" in file:
            if "FeatSelect" in file:
                modelName = "TS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "TS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Date Shift" in file:
            if "FeatSelect" in file:
                modelName = "DS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "DS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        else:
            print("Model naming error")
            exit()

        averageFile.at[rowNum, "Model"] = modelName
        averageFile.at[rowNum, "Train_Acc"] = data.Train_Acc.mean()
        averageFile.at[rowNum, "Train_Loss"] = data.Train_Loss.mean()
        averageFile.at[rowNum, "Test_Acc"] = data.Test_Acc.mean()
        averageFile.at[rowNum, "Test_Loss"] = data.Test_Loss.mean()
        averageFile.at[rowNum, "AUC"] = data.AUC.mean()
        averageFile.at[rowNum, "TN"] = data.TN.mean()
        averageFile.at[rowNum, "FP"] = data.FP.mean()
        averageFile.at[rowNum, "FN"] = data.FN.mean()
        averageFile.at[rowNum, "TP"] = data.TP.mean()
        averageFile.at[rowNum, "Accuracy"] = data.Accuracy.mean()
        averageFile.at[rowNum, "Precision"] = data.Precision.mean()
        averageFile.at[rowNum, "Recall"] = data.Recall.mean()
        averageFile.at[rowNum, "Specificity"] = data.Specificity.mean()
        averageFile.at[rowNum, "FPR"] = data.FPR.mean()
        rowNum = rowNum + 1

    averageFile.to_excel("../Jeremy Thesis/Model Result Averages.xlsx")


def add_weather(data, weather):
    print("Adding Weather")
    data.Unix = data.Unix.astype(int)
    weather.Unix = weather.Unix.astype(int)
    data.Grid_Num = data.Grid_Num.astype(int)
    weather.Grid_Num = weather.Grid_Num.astype(int)
    # Merge the weather variables for the hour of the accident based on time and grid block
    # Merge the event/conditions before columns based on hour before and grid block
    newdata = pandas.merge(data, weather[['Grid_Num', 'cloudCover', 'dewPoint',
                                          'humidity', 'precipIntensity', 'precipProbability', 'precipType',
                                          'pressure', 'temperature', 'Unix', 'uvIndex',
                                          'visibility', 'windBearing', 'windGust', 'windSpeed', 'Event',
                                          'Conditions', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear']],
                           on=['Unix', 'Grid_Num'])

    # Applying rain before to data
    weather['hourbefore'] = weather.Unix.astype(int)
    weather['RainBefore'] = weather.Rain.astype(int)
    newdata['hourbefore'] = newdata['Unix'] - 60 * 60
    newdata.hourbefore = newdata.hourbefore.astype(int)
    newdata = pandas.merge(newdata, weather[['Grid_Num', 'hourbefore', 'RainBefore']],
                           on=['hourbefore', 'Grid_Num'])
    return newdata


def createForecastForum(forumTemplate, saveDate, weather):
    """
    Method to create a filled out forecast forum that has all the variables you'd need
    saveDate format can be whatever you want it to be, a standard we use is m-d-yyyy
    """
    # Information about each grid number
    grid_info = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/HexGridInfo.csv")

    columns = ['Latitude', 'Longitude', 'Hour', 'Grid_Num', 'Join_Count', 'NBR_LANES', 'TY_TERRAIN',
               'FUNC_CLASS', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'Foggy', 'Rain', 'RainBefore', 'Snow',
               'Unix', 'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed',
               'visibility', 'uvIndex', 'pressure']

    for j, _ in enumerate(forumTemplate.values):
        timestamp = str(saveDate) + " " + str(forumTemplate.Hour.values[j])
        unixTime = time.mktime(datetime.strptime(timestamp, "%m-%d-%Y %H").timetuple())
        forumTemplate.at[j, "Unix"] = unixTime

    forumFile = add_weather(forumTemplate, weather)
    forumFile = forumFile.reindex(columns=columns)

    forumFile.WeekDay = forumFile.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    forumFile.DayFrame = forumFile.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    for i, _ in enumerate(forumFile.values):
        timestamp = str(saveDate) + " " + str(forumFile.Hour.values[i])
        thisDate = datetime.strptime(timestamp, "%m-%d-%Y %H")
        forumFile.at[i, "DayOfWeek"] = thisDate.weekday()

        row_num = grid_info.loc[grid_info["Grid_Num"] == forumFile.Grid_Num.values[i]].index[0]
        forumFile.at[i, 'Latitude'] = grid_info.Center_Lat.values[row_num]
        forumFile.at[i, 'Longitude'] = grid_info.Center_Long.values[row_num]
        forumFile.at[i, 'Join_Count'] = grid_info.Join_Count.values[row_num]
        forumFile.at[i, 'NBR_LANES'] = grid_info.NBR_LANES.values[row_num]
        forumFile.at[i, 'TY_TERRAIN'] = grid_info.TY_TERRAIN.values[row_num]
        forumFile.at[i, 'FUNC_CLASS'] = grid_info.FUNC_CLASS.values[row_num]
    forumFile.to_csv("../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % saveDate, index=False)


def finding_matches(accidents, forecastData, date):
    """
    Date format: m/d/yyyy
    """
    posData = forecastData[forecastData['Prediction'] == 1]
    negData = forecastData[forecastData['Prediction'] == 0]
    TP = 0
    FN = 0
    accCut = accidents[accidents['Date'] == date]
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posData.values):
            if (accCut.Grid_Num.values[i] == posData.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posData.DayFrame.values[j]):
                TP += 1
        for n, _ in enumerate(negData.values):
            if (accCut.Grid_Num.values[i] == negData.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negData.DayFrame.values[n]):
                FN += 1
    try:
        TN = len(negData) - FN
        FP = len(posData) - TP
        recall = TP/(TP+FN)
        specificity = TN / (FP + TN)
        precision = TP/(TP+FP)
        f1Score = 2 * ((recall * precision) / (recall + precision))

        return TP, FN, TN, FP, recall, specificity, precision, f1Score
    except:
        print("Error in calculating confusion matrix values")

    # print("\tTrue Positives: ", TP)
    # print("\tFalse Negatives: ", FN)
    # print("\tTrue Negatives: ", TN)
    # print("\tFalse Positives: ", FP)
    # try:
    #     print("\tRecall: ", recall)
    # except:
    #     print("\tRecall Calc Error")
    # try:
    #     print("\tSpecificity: ", TN / (FP + TN))
    # except:
    #     print("\tSpecificity Calc Error")
    # try:
    #     print("\tPrecision: ", precision)
    # except:
    #     print("\tRecision Calc Error")
    # try:
    #     print("\tF1 Score: ", f1Score)
    # except:
    #     print("\tF1 Score Calc Error")


def matchAccidentsWithDistance(accidents, predictions, date):
    # Read in the grid info
    gridInfo = pandas.read_csv("../Jeremy Thesis/HexGrid Shape Data.csv")
    # Cut your predictions to only the accidents
    posPredictions = predictions[predictions["Prediction"] == 1]
    negPredictions = predictions[predictions["Prediction"] == 0]
    # Cut your accident file to only the date you want to look at
    accCut = accidents[accidents['Date'] == date]
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                        (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    # These for loops handle the straight forward DayFrame and Grid Num matching for accidents and predictions
    TP = 0
    FN = 0
    # distTP = 0
    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posPredictions.values):
            if (accCut.Grid_Num.values[i] == posPredictions.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posPredictions.DayFrame.values[j]):
                TP += 1
            else:
                accCoords = (float(accCut.Latitude.values[i]), float(accCut.Longitude.values[i]))
                predictionGrid = posPredictions.Grid_Num.values[j]  # Prediction Grid Num
                # Note: the predicitonGrid value needs to be reduced by 1 since the Grid_Num is being used as a row num
                # since python does counting like [0...max], we need to decrease our look up number by 1
                # The way the gridInfo file is set up, Grid_Num 1 has row 0, and Grid_Num 694 has row 693
                centerLat = gridInfo.Center_Lat.values[predictionGrid - 1]
                centerLong = gridInfo.Center_Long.values[predictionGrid - 1]
                predictionCoords = (float(centerLat), float(centerLong))
                distance = geopy.distance.vincenty(accCoords, predictionCoords).miles
                if distance <= 0.3 and accCut.DayFrame.values[i] == posPredictions.DayFrame.values[j]:
                    TP += 1
        for n, _ in enumerate(negPredictions.values):
            if (accCut.Grid_Num.values[i] == negPredictions.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negPredictions.DayFrame.values[n]):
                FN += 1

    try:
        TN = len(negPredictions) - FN
        FP = len(posPredictions) - TP
        recall = TP / (TP + FN)
        specificity = TN / (FP + TN)
        precision = TP / (TP + FP)
        f1Score = 2 * ((recall * precision) / (recall + precision))

        return TP, FN, TN, FP, recall, specificity, precision, f1Score
    except:
        print("Error in calculating confusion matrix values")
        

def basicFormat(rawAcc):
    """
    A basic method to add in some essential data to newly fetched accidents
    """
    columns = ['Response_Date', 'Month', 'Day', 'Year', 'Hour', 'Date', 'Grid_Num', 'Longitude', 'Latitude', 'WeekDay',
               'DayOfWeek',
               'DayFrame']
    # weather = feather.read_dataframe("../")
    rawAcc = rawAcc.reindex(columns=columns)
    rawAcc.Hour = rawAcc.Hour.astype(str)
    rawAcc.Date = rawAcc.Date.astype(str)
    for i, _ in enumerate(rawAcc.values):
        rawAcc.Hour.values[i] = rawAcc.Response_Date.values[i].split(" ")[1].split(":")[0]
        rawAcc.Date.values[i] = rawAcc.Response_Date.values[i].split(" ")[0]
        rawAcc.Month.values[i] = rawAcc.Date.values[i].split("/")[0]
        rawAcc.Day.values[i] = rawAcc.Date.values[i].split("/")[1]
        rawAcc.Year.values[i] = rawAcc.Date.values[i].split("/")[2]
        timestamp = str(rawAcc.Date.values[i]) + " " + str(rawAcc.Hour.values[i])

        thisDate = datetime.strptime(timestamp, "%m/%d/%Y %H")
        rawAcc.at[i, "DayOfWeek"] = thisDate.weekday()

        unixTime = time.mktime(datetime.strptime(timestamp, "%m/%d/%Y %H").timetuple())
        rawAcc.at[i, "Unix"] = unixTime

    rawAcc.Hour = rawAcc.Hour.astype(int)

    # rawAcc = add_weather(rawAcc, weather)

    rawAcc.WeekDay = rawAcc.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    rawAcc.DayFrame = rawAcc.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    rawAcc.to_csv("../", index=False)


def modelResultGraph_oneWeek(data):
    data5050 = data[data['Model'].str.contains("5050")]
    data7525 = data[data['Model'].str.contains("7525")]
    dataNoSplit = data[data['Model'].str.contains("No")]

    specFig = px.line(dataNoSplit, x="Date", y="Specificity", color='Model')
    specFig.show()

    recFig = px.line(dataNoSplit, x="Date", y="Recall", color='Model')
    recFig.show()


def modelResultGraph_oneMonth(data):
    fig = px.line(data, x="Date", y="Specificity", color='ModelType')
    fig.show()


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """
    col1 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col2 = ['Accident', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col3 = ['Accident', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek']

    col4 = ['Accident', 'Grid_Num', 'cloudCover', 'humidity', 'precipIntensity',
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


def standardize(data):
    """
    This standardizes the data into the MinMaxReduced version used for model creation
    """
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    dataScaled = scaler.fit_transform(data)
    dataScaled = pandas.DataFrame(dataScaled, columns=columns)
    return dataScaled


def xgBoostFeatureImportance(data):
    """
    A method to compute the variable importance scores
    """
    cutData = test_type(data, 1)
    standData = standardize(cutData)

    print(standData.columns)
    # split data into X and y
    X = standData.iloc[:, 1:(len(standData.columns) + 1)].values  # Our independent variables
    Y = standData.iloc[:, 0].values  # Our dependent variable
    # fit model no training data
    model = XGBClassifier()
    model.fit(X, Y)
    # plot feature importance
    plot_importance(model)
    pyplot.show()


def featureSelectionColumns(data, modelRow):
    """
    A method for getting what columns to keep for the feature selection tests done for the different datasets
    It reads in the file that has the most important variables per test
    Then, cleans the list to remove any empties (since some tests have a smaller number of variables)
    Then, converts the values in the list to strings, then sets the columns of the data
    """
    columnData = pandas.read_excel("../Jeremy Thesis/Feature Selection Results.xlsx")
    columns = ["Accident"]  # columns we'll be appending
    rowNum = columnData[columnData["Model"] == str(modelRow)].index[0]  # get the actual row number based on the model
    dataRow = list(columnData.iloc[rowNum,])  # get the row that corresponds to the row number
    dataRow = [x for x in dataRow if str(x) != 'nan']  # clean the list of empties
    dataRow = dataRow[1:]
    columns = columns + dataRow
    return data.reindex(columns=columns)  # set the columns of the data


def pcaOnModelWeights(file, modelPath):
    """
    A method to get the weights for the different layers in the MLP model and apply PCA to them
    Simply supply the file you need and the saved .h5 model file for loading in weights
    Comment out any of the methods below you may or may not need to get your data in the proper format
    """
    data = pandas.read_csv("../%s" % file)
    fsModel = "TS 50-50 T1"  # used for selecting columns if using ExtraTreesClassifier for feature selection
    cutData = test_type(data, 1)  # selecting test type
    cutData = standardize(cutData)  # standardize data
    # cutData = featureSelectionColumns(cutData, fsModel)
    cutData = shuffle(cutData)  # shuffle the data
    X = cutData.iloc[:, 1:(len(cutData.columns) + 1)].values
    Y = cutData.iloc[:, 0].values

    # Make the model
    model = Sequential()
    model.add(Dense(X.shape[1], input_dim=X.shape[1], activation='sigmoid'))
    model.add(Dense(X.shape[1] - 5, activation='sigmoid'))
    model.add(Dropout(.1))
    try:
        model.add(Dense(X - 10, activation='sigmoid'))
    except:
        model.add(Dense(X - 5, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.load_weights("../%s" % modelPath)
    # Get the weights of the model's first layer
    weights = model.layers[0].get_weights()[0]
    # Apply PCA to those weights and save them to a file
    pca = PCA(n_components=len(cutData.columns[1:len(cutData.columns)]))
    principalComponents = pca.fit_transform(weights)
    principalDf = pandas.DataFrame(data=principalComponents, columns=cutData.columns[1:len(cutData.columns)])
    principalDf.to_csv("../", index=False)
    # variance explained if you want it
    print(pca.explained_variance_ratio_)


# Code for finding matches from the forecasts
# rawAcc = pandas.read_csv("../Jeremy Thesis/2020 Accidents to 6-4-2020.csv")
# forecasts = []
# saveIterator = 0
# saveDF = pandas.DataFrame(columns=['Model', 'Date', 'TP', 'FN', 'TN', 'FP', 'Recall', 'Specificity', 'Precision',
#                                    'F1 Score'])
# for forecast in forecasts:
#     forecastFile = pandas.read_csv("../%s" % forecast)
#
#     if 'FeatSelect' in forecast:
#         date = forecast.split("_")[4].split(".")[0].replace("-", "/")
#     elif 'LogReg' in forecast:
#         date = forecast.split("_")[4].split(".")[0].replace("-", "/")
#         modelName = forecast.split("/")[2].split(".")[0]
#     else:
#         date = forecast.split("_")[3].split(".")[0].replace("-", "/")
#     # print(date)
#     # print(modelName)
#     # exit()
#     cutRawAcc = rawAcc[rawAcc['Date'] == date]
#     print("Forecast on ", forecast)
#     TP, FN, TN, FP, recall, specificity, precision, f1Score = finding_matches(cutRawAcc, forecastFile, date)
#     saveDF.at[saveIterator, 'Model'] = modelName
#     saveDF.at[saveIterator, 'Date'] = date
#     saveDF.at[saveIterator, 'TP'] = TP
#     saveDF.at[saveIterator, 'FN'] = FN
#     saveDF.at[saveIterator, 'TN'] = TN
#     saveDF.at[saveIterator, 'FP'] = FP
#     saveDF.at[saveIterator, 'Recall'] = recall
#     saveDF.at[saveIterator, 'Specificity'] = specificity
#     saveDF.at[saveIterator, 'Precision'] = precision
#     saveDF.at[saveIterator, 'F1 Score'] = f1Score
#     saveIterator += 1
# saveDF.to_csv("../", index=False)

# lrData = pandas.read_csv("../Jeremy Thesis/Logistic Regression Tests/LogReg Forecast Results No Dist.csv")
# mlpData = pandas.read_csv("../Jeremy Thesis/Forecasting/MLP Top 5 Splits Forecast Results.csv")
# modelResultGraph_oneWeek(lrData)
data = pandas.read_csv("../Jeremy Thesis/Best Model Statistics/January Forecasts (LR vs MLP Best Models).csv")
modelResultGraph_oneMonth(data)
