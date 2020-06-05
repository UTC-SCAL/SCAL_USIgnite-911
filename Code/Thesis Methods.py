"""
A general file to hold all of my misc methods I've made during my thesis research
"""
import pandas
import feather
import time
from datetime import datetime


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


# Find matches, using either the original DayFrames, or the alternate.
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
    TN = len(negData) - FN
    FP = len(posData) - TP
    print("\tTrue Positives: ", TP)
    print("\tFalse Negatives: ", FN)
    print("\tTrue Negatives: ", TN)
    print("\tFalse Positives: ", FP)
    print("\tRecall: ", TP/(TP+FN))
    print("\tSpecificity: ", TN/(FP+TN))


def basicFormat(rawAcc):
    """
    A basic method to add in some essential data to newly fetched accidents
    """
    columns = ['Response_Date', 'Month', 'Day', 'Year', 'Hour', 'Date', 'Grid_Num', 'Longitude', 'Latitude', 'WeekDay', 'DayOfWeek',
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

