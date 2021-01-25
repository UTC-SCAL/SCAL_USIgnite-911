"""
Author: Jeremy Roland
Purpose: A one stop place to find all the needed methods to work with the accident data. Here you can add in any
    variables you may need, and even match up predictions with accidents
"""

import pandas
from shapely.geometry import Point, Polygon
from datetime import datetime
import time
import geopy.distance
import feather


# Match up accidents to their grid numbers
def matchAccidentToGridNum(hexShapeFile, accDataFile):
    # Iterate over our accidents
    for j, _ in enumerate(accDataFile.values):
        # Our accident GPS coords as a Point object
        accPoint = Point(accDataFile.Longitude.values[j], accDataFile.Latitude.values[j])
        # Iterate over our grid hexes
        for i, _ in enumerate(hexShapeFile.values):
            latList = hexShapeFile.Latitudes.values[i].split(",")
            longList = hexShapeFile.Longitudes.values[i].split(",")
            longList = list(map(lambda x: float(x), longList))
            latList = list(map(lambda x: float(x), latList))
            # A polygon object made of the GPS coords of the hex shape
            gridHex = Polygon(zip(longList, latList))
            # Check if the accident point object is within the hex shape polygon
            if accPoint.within(gridHex):
                accDataFile.Grid_Num.values[j] = hexShapeFile.Grid_Num.values[i]
                break
    # Save the newly altered accident file that now should have grid nums
    accDataFile.to_csv("../", index=False)


# Add weather to accidents
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

    # Applying rain before to data
    weather['hourbefore'] = weather.Unix.astype(int)
    weather['RainBefore'] = weather.Rain.astype(int)
    newdata['hourbefore'] = newdata['Unix'] - 60 * 60
    newdata.hourbefore = newdata.hourbefore.astype(int)
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
               'visibility', 'uvIndex', 'pressure']
    # Set Unix timestamps
    for j, _ in enumerate(forumTemplate.values):
        timestamp = str(saveDate) + " " + str(forumTemplate.Hour.values[j])
        unixTime = time.mktime(datetime.strptime(timestamp, "%m-%d-%Y %H").timetuple())
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
        thisDate = datetime.strptime(timestamp, "%m-%d-%Y %H")
        forumFile.at[i, "DayOfWeek"] = thisDate.weekday()

        row_num = grid_info.loc[grid_info["Grid_Num"] == forumFile.Grid_Num.values[i]].index[0]
        forumFile.at[i, 'Latitude'] = grid_info.Center_Lat.values[row_num]
        forumFile.at[i, 'Longitude'] = grid_info.Center_Long.values[row_num]
        forumFile.at[i, 'Join_Count'] = grid_info.Join_Count.values[row_num]
        forumFile.at[i, 'NBR_LANES'] = grid_info.NBR_LANES.values[row_num]
        forumFile.at[i, 'TY_TERRAIN'] = grid_info.TY_TERRAIN.values[row_num]
        forumFile.at[i, 'FUNC_CLASS'] = grid_info.FUNC_CLASS.values[row_num]
    # A new forecast forum will be saved for each date, which is what the saveDate variable is used for
    forumFile.to_csv("../Main Dir/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % saveDate, index=False)


# The standard method to match actual accidents to our predicted hotspots
def finding_matches(accidents, forecastData, date):
    """
    Date format: m/d/yyyy
    """
    # Split the data into accident predictions and non accident predictions
    posData = forecastData[forecastData['Prediction'] == 1]
    negData = forecastData[forecastData['Prediction'] == 0]
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
        for j, _ in enumerate(posData.values):
            if (accCut.Grid_Num.values[i] == posData.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posData.DayFrame.values[j]):
                TP += 1
        for n, _ in enumerate(negData.values):
            if (accCut.Grid_Num.values[i] == negData.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negData.DayFrame.values[n]):
                FN += 1
    # Calculate our confusion matrix values
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


# An alternate method of matching actual accidents to our predicted hotspots
# This method goes for a more lax approach to matching, simply testing if an accident was within a certain mileage
# distance from the center of one of our hotspots
def matchAccidentsWithDistance(accidents, predictions, date):
    # Read in the grid info
    gridInfo = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
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
    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posPredictions.values):
            accCoords = (float(accCut.Latitude.values[i]), float(accCut.Longitude.values[i]))
            predictionGrid = posPredictions.Grid_Num.values[j]  # Prediction Grid Num
            # Note: the predictionGrid value needs to be reduced by 1 since the Grid_Num is being used as a row num
            # since python does counting like [0...max], we need to decrease our look up number by 1
            # The way the gridInfo file is set up, Grid_Num 1 has row 0, and Grid_Num 694 has row 693
            centerLat = gridInfo.Center_Lat.values[predictionGrid - 1]
            centerLong = gridInfo.Center_Long.values[predictionGrid - 1]
            predictionCoords = (float(centerLat), float(centerLong))
            # Get the distance in miles between the centerpoint of our hotspot and the actual accident
            # The distance used can be altered accordingly
            distance = geopy.distance.vincenty(accCoords, predictionCoords).miles
            if distance <= 0.3 and accCut.DayFrame.values[i] == posPredictions.DayFrame.values[j]:
                TP += 1
        for n, _ in enumerate(negPredictions.values):
            if (accCut.Grid_Num.values[i] == negPredictions.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negPredictions.DayFrame.values[n]):
                FN += 1
    # Calculate our confusion matrix values
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


# A method to add in essential variables to newly fetched accidents
def newAccidentFormatter(rawAcc):
    # The columns we want
    columns = ['Response_Date', 'Month', 'Day', 'Year', 'Hour', 'Date', 'Grid_Num', 'Longitude', 'Latitude', 'WeekDay',
               'DayOfWeek', 'DayFrame']
    rawAcc = rawAcc.reindex(columns=columns)
    rawAcc.Hour = rawAcc.Hour.astype(str)
    rawAcc.Date = rawAcc.Date.astype(str)
    for i, _ in enumerate(rawAcc.values):
        # Manipulate the existing variables into the formats we want them in
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
    rawAcc.WeekDay = rawAcc.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    rawAcc.DayFrame = rawAcc.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    rawAcc.to_csv("../", index=False)


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
        cutRawAcc = rawAcc[rawAcc['Date'] == date]
        print("Forecast on ", forecast)
        # If you want to use the distance matching version of finding_matches, then change what method is called
        TP, FN, TN, FP, recall, specificity, precision, f1Score = finding_matches(cutRawAcc, forecastFile, date)
        # Save all of our confusion matrix values, date of prediction, and model name to the dataframe
        saveDF.at[saveIterator, 'Model'] = modelName
        saveDF.at[saveIterator, 'Date'] = date
        saveDF.at[saveIterator, 'TP'] = TP
        saveDF.at[saveIterator, 'FN'] = FN
        saveDF.at[saveIterator, 'TN'] = TN
        saveDF.at[saveIterator, 'FP'] = FP
        saveDF.at[saveIterator, 'Recall'] = recall * 100
        saveDF.at[saveIterator, 'Specificity'] = specificity * 100
        saveDF.at[saveIterator, 'Precision'] = precision * 100
        saveDF.at[saveIterator, 'F1 Score'] = f1Score * 100
        saveIterator += 1
    saveDF.to_csv("../", index=False)


rawAcc = pandas.read_csv("../Main Dir/Accident Data/2020 Accidents to 11-18-2020.csv")
forecasts = []
forecastMatchingFormatter(rawAcc, forecasts)
