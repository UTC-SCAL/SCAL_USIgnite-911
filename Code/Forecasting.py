"""
Author: Jeremy Roland
Purpose: A one stop place to find all needed methods for forecasting
"""

import pandas
from datetime import datetime
import time
import geopy.distance


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


# Create new forecast templates for new dates of the year
def createForecastForum(forumTemplate, saveDate, weather):
    """
    Method to create a filled out forecast forum that has all the variables you'd need
    saveDate format can be whatever you want it to be, a standard we use is m-d-yyyy
    """
    # Information about each grid number
    grid_info = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    # The columns we want for our forecast forum
    columns = ['Latitude', 'Longitude', 'Hour', 'Grid_Num', 'Join_Count', 'NBR_LANES', 'TY_TERRAIN',
               'FUNC_CLASS', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'Foggy', 'Rain', 'RainBefore', 'Snow',
               'Unix', 'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed',
               'visibility', 'uvIndex', 'pressure', 'RoadwayFeatureMode', 'yieldSignCount', 'stopSignCount',
               'speedMode']
    # Set Unix timestamps
    for j, _ in enumerate(forumTemplate.values):
        timestamp = str(saveDate) + " " + str(forumTemplate.Hour.values[j])
        # unixTime = time.mktime(datetime.strptime(timestamp, "%m-%d-%Y %H").timetuple())
        unixTime = time.mktime(datetime.strptime(timestamp, "%Y-%m-%d %H").timetuple())
        forumTemplate.at[j, "Unix"] = unixTime
    # Add weather variables and reset the columns
    forumFile = add_weather(forumTemplate, weather)
    forumFile = forumFile.reindex(columns=columns)
    # Add in some extra variables
    forumFile.WeekDay = forumFile.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    forumFile.DayFrame = forumFile.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                             (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    for i, _ in enumerate(forumFile.values):
        # Iterate through our file and add in the final time, location, and roadway variables
        timestamp = str(saveDate) + " " + str(forumFile.Hour.values[i])
        thisDate = datetime.strptime(timestamp, "%Y-%m-%d %H")
        forumFile.at[i, "DayOfWeek"] = thisDate.weekday()

        row_num = grid_info.loc[grid_info["Grid_Num"] == forumFile.Grid_Num.values[i]].index[0]
        forumFile.at[i, 'Latitude'] = grid_info.Center_Lat.values[row_num]
        forumFile.at[i, 'Longitude'] = grid_info.Center_Long.values[row_num]
        forumFile.at[i, 'Join_Count'] = grid_info.Join_Count.values[row_num]
        forumFile.at[i, 'NBR_LANES'] = grid_info.NBR_LANES.values[row_num]
        forumFile.at[i, 'TY_TERRAIN'] = grid_info.TY_TERRAIN.values[row_num]
        forumFile.at[i, 'FUNC_CLASS'] = grid_info.FUNC_CLASS.values[row_num]
        forumFile.at[i, 'RoadwayFeatureMode'] = grid_info.RoadwayFeatureMode.values[row_num]
        forumFile.at[i, 'yieldSignCount'] = grid_info.yieldSignCount.values[row_num]
        forumFile.at[i, 'stopSignCount'] = grid_info.stopSignCount.values[row_num]
        forumFile.at[i, 'speedMode'] = grid_info.speedMode.values[row_num]
    # A new forecast forum will be saved for each date, which is what the saveDate variable is used for
    # Drop any duplicates that the above statement may make
    forumFile.drop_duplicates(keep="first", inplace=True)
    forumFile.to_csv("../Main Dir/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % saveDate,
                     index=False)


# The standard method to match actual accidents to our predicted hotspots
def finding_matches(accidents, forecastData, date):
    """
    Date format: m/d/yyyy
    """
    # Split the data into accident predictions and non accident predictions
    # posPredictData = forecastData[forecastData['Prediction'] == 1]
    # negPredictData = forecastData[forecastData['Prediction'] == 0]
    # Cut the positive predictions to only those that have a probability over a certain threshold
    # posPredictData = forecastData[forecastData['Probability'] >= .75]
    # negPredictData = forecastData[forecastData['Probability'] < .75]
    posPredictData = forecastData[forecastData['Probability'] >= .60]
    negPredictData = forecastData[forecastData['Probability'] < .60]

    TP = 0
    FN = 0
    # Cut our file of all our accidents (future dates not included in our training/testing dataset) to the date we want
    accCut = accidents[accidents['Date'] == date]
    # Add in the dayframe variable
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                        (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    # Iterate through our actual accidents and our predictions to find matches
    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posPredictData.values):
            if (accCut.Grid_Num.values[i] == posPredictData.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posPredictData.DayFrame.values[j]):
                TP += 1
        for n, _ in enumerate(negPredictData.values):
            if (accCut.Grid_Num.values[i] == negPredictData.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negPredictData.DayFrame.values[n]):
                FN += 1
    # Calculate our confusion matrix values
    try:
        TN = len(negPredictData) - FN
        FP = len(posPredictData) - TP
        recall = TP/(TP+FN)
        specificity = TN / (FP + TN)
        precision = TP/(TP+FP)
        f1Score = 2 * ((recall * precision) / (recall + precision))

        return TP, FN, TN, FP, recall, specificity, precision, f1Score
    except:
        print("Error in calculating confusion matrix values")
        TN = len(negPredictData) - FN
        FP = len(posPredictData) - TP
        recall = -1
        specificity = -1
        precision = -1
        f1Score = -1

        return TP, FN, TN, FP, recall, specificity, precision, f1Score


# The standard method to match actual accidents to our predicted hotspots
# This version of finding_matches uses mileage distance to match an accident to a grid num
def finding_matches_distance(accidents, forecastData, date):
    """
    Date format: m/d/yyyy
    """
    gridInfo = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    # Split the data into accident predictions and non accident predictions
    posPredictData = forecastData[forecastData['Prediction'] == 1]
    negPredictData = forecastData[forecastData['Prediction'] == 0]
    # Cut the positive predictions to only those that have a probability over a certain threshold
    # posPredictData = forecastData[forecastData['Probability'] >= .75]
    # negPredictData = forecastData[forecastData['Probability'] < .75]
    # posPredictData = forecastData[forecastData['Probability'] >= .60]
    # negPredictData = forecastData[forecastData['Probability'] < .60]

    TP = 0  # True Positive
    NTP = 0  # Neighbor True Positive
    FN = 0  # False Negative
    # Cut our file of all our accidents (future dates not included in our training/testing dataset) to the date we want
    accCut = accidents[accidents['Date'] == date]
    # Create a match found variable to mark an accident record as having found a matching prediction for
    # This is used to cut our accident list down to the non matches for finding false negatives later on
    accCut['MatchFound'] = 0
    # Add in the dayframe variable
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                        (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    # Iterate through our actual accidents and our predictions to find matches
    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posPredictData.values):
            # Note: the grid value needs to be reduced by 1 since the Grid_Num is being used as a row num
            # since python does counting like [0...max], we need to decrease our look up number by 1
            # The way the gridCoords file is set up, Grid_Num 1 has row 0, and Grid_Num 694 has row 693

            # Get our accident's grid number, then get the center point of that grid number from our grid info file
            accGridNum = accCut.Grid_Num.values[i]
            accCenterLat = gridInfo.Center_Lat.values[accGridNum - 1]
            accCenterLong = gridInfo.Center_Long.values[accGridNum - 1]
            # Make that center point into a gps point object
            accCoords = (float(accCenterLat), float(accCenterLong))

            # Get our prediction grid's grid number, then get the center point of that grid number
            predGridNum = posPredictData.Grid_Num.values[j]
            predCenterLat = gridInfo.Center_Lat.values[predGridNum - 1]
            predCenterLong = gridInfo.Center_Long.values[predGridNum - 1]
            # Make the center point into a gps point object
            predCoords = (float(predCenterLat), float(predCenterLong))

            # Get the distance in miles between the center point of our hotspot and the actual accident
            # The distance used can be altered accordingly
            # The distance between each hexagon in our grid is 0.509... miles,
            # so round it up to 0.51 to find out if the grids are neighbors
            distance = geopy.distance.vincenty(accCoords, predCoords).miles

            if (accCut.Grid_Num.values[i] == posPredictData.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posPredictData.DayFrame.values[j]):
                TP += 1
                accCut.MatchFound.values[i] = 1
                # print("Direct Matches")
                # print("Acc Grid Num: ", accCut.Grid_Num.values[i])
                # print("Pred Grid Num: ", posPredictData.Grid_Num.values[j])
                # print("Acc DayFrame: ", accCut.DayFrame.values[i], accCut.Hour.values[i])
                # print("Pred DayFrame: ", posPredictData.DayFrame.values[j])
                break
            elif distance <= 0.51 and accCut.DayFrame.values[i] == posPredictData.DayFrame.values[j]:
                NTP += 1
                accCut.MatchFound.values[i] = 1
                break
    # Cut our accidents to only those records where a matching grid num and dayframe wasn't found
    accCut = accCut[accCut['MatchFound'] == 0]
    for b, _ in enumerate(accCut.values):
        for n, _ in enumerate(negPredictData.values):
            if (accCut.Grid_Num.values[b] == negPredictData.Grid_Num.values[n] and accCut.DayFrame.values[b] ==
                    negPredictData.DayFrame.values[n]):
                FN += 1
                break

    # Calculate our confusion matrix values
    TP = TP + NTP
    # FN = FN - NTP
    try:
        TN = len(negPredictData) - FN
        FP = len(posPredictData) - TP
        recall = TP/(TP+FN)
        specificity = TN / (FP + TN)
        precision = TP/(TP+FP)
        f1Score = 2 * ((recall * precision) / (recall + precision))

        return TP, FN, TN, FP, recall, specificity, precision, f1Score, NTP
    except:
        print("Error in calculating confusion matrix values")
        TN = len(negPredictData) - FN
        FP = len(posPredictData) - TP
        recall = -1
        specificity = -1
        precision = -1
        f1Score = -1

        return TP, FN, TN, FP, recall, specificity, precision, f1Score, NTP


# A formatting method to be used when you are matching actual accidents to our prediction hotspots
# If you are going to be matching some predictions to their actual accidents, use this method
def forecastMatchingFormatter(rawAcc, forecasts):
    """
    rawAcc: the file that has the actual accidents. At time of writing, the file is: 2020 Accidents to 11-18-2020.csv
    forecasts: a list of file names that correspond to the file paths of the predictions you have done
        ex: Main Dir/Logistic Regression Tests/LogReg_SS 5050_Forecast_1-1-2020.csv
    """
    # An iterator value used for storing the confusion matrix values
    saveIterator = 0
    # Create an empty dataframe with these columns to hold our matching results
    saveDF = pandas.DataFrame(columns=['Model', 'Date', 'TP', 'FN', 'TN', 'FP', 'Recall', 'Specificity', 'Precision',
                                       'F1 Score'])
    # Iterate through our list of forecast file paths, where each one is read in and treated like a file path
    for forecast in forecasts:
        forecastFile = pandas.read_csv("../%s" % forecast)
        # These are here for distinguishing between MLP forecasts and Logistic Regression forecasts
        # The way I set up my file names, these splits work, but you may need to change them based on how you save
        # file names
        if 'FeatSelect' in forecast:
            date = forecast.split("_")[4].split(".")[0].replace("-", "/")
        elif 'LogReg' in forecast:
            date = forecast.split("_")[3].split(".")[0].replace("-", "/")
            modelName = forecast.split("/")[2].split("_")[1]
        else:
            date = forecast.split("_")[3].split(".")[0].replace("-", "/")

        # Use these 3 lines to test out that you are splitting your file name into the modelName and date values
        # print(date)
        # print(modelName)
        # exit()

        # Cut our raw accident file to cover only the date we predicted for
        # Depending on the format of your date variable, you may have to change it
        date = date.replace("/", '-')
        cutRawAcc = rawAcc[rawAcc['Date'] == date]
        print("Forecast on ", forecast)
        # If you want to use the distance matching version of finding_matches, then change what method is called
        # TP, FN, TN, FP, recall, specificity, precision, f1Score = finding_matches(cutRawAcc, forecastFile, date)
        TP, FN, TN, FP, recall, specificity, precision, f1Score, NTP = \
            finding_matches_distance(cutRawAcc, forecastFile, date)
        # Save all of our confusion matrix values, date of prediction, and model name to the dataframe
        saveDF.at[saveIterator, 'Model'] = modelName
        saveDF.at[saveIterator, 'Date'] = date
        saveDF.at[saveIterator, 'TP'] = TP
        saveDF.at[saveIterator, 'NTP'] = NTP
        saveDF.at[saveIterator, 'FN'] = FN
        saveDF.at[saveIterator, 'TN'] = TN
        saveDF.at[saveIterator, 'FP'] = FP
        saveDF.at[saveIterator, 'Recall'] = recall * 100
        saveDF.at[saveIterator, 'Specificity'] = specificity * 100
        saveDF.at[saveIterator, 'Precision'] = precision * 100
        saveDF.at[saveIterator, 'F1 Score'] = f1Score * 100
        saveIterator += 1
    saveDF.to_csv("../Main Dir/Logistic Regression Tests/2021 Tests.csv", index=False)


########################################## Creating New Forecasting Files ##############################################
# Read in the template file
# template = pandas.read_csv("../Main Dir/Forecasting/Forecast Files/Forecast Forum Template.csv")
# Read in your weather
# weather = feather.read_dataframe("../")
# weather = pandas.read_csv("../")
# A nifty pandas feature that enables you to select a range of dates, instead of listing them all out
# Format: yyyy-mm-dd
# beginDate = '2021-01-01'
# endDate = '2021-01-31'
# dates = pandas.date_range(beginDate, endDate)
# Iterate through our dates list, and make a forecast file for each date
# for date in dates:
#     date = str(date).split(" ")[0]
#     createForecastForum(template, date, weather)
########################################################################################################################

################################# Matching Forecast Predictions to Actual Accidents ####################################
# Read in the file that has the accidents retrieved from the email fetching code
# Ensure the date format of the rawAccidents file is yyyy-mm-dd
rawAccidents = pandas.read_csv("../Main Dir/Accident Data/EmailAccidentData_2021-02-08.csv")
# Make a list of the file paths for the forecasts you've made, this will be passed in as a method parameter
forecastFiles = []
forecastMatchingFormatter(rawAccidents, forecastFiles)
########################################################################################################################
