"""
Author: Jeremy Roland
Purpose: The main file for creating a logistic regression prediction model
"""

from sklearn import preprocessing
import pandas
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import feather
from datetime import datetime


# A test type method specific for the logistic regression testing
def logReg_test_type(data, type):
    # All variables
    col1 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    # No weather variables
    col3 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS',  'DayFrame', 'WeekDay',
            'DayOfWeek']
    # Same as col3, but with aggregated weather added in
    col7 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS',  'DayFrame', 'WeekDay',
            'DayOfWeek', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
    # Same as col8, but with roundAbout variable
    col8 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'roundAbout', 'DayFrame', 'WeekDay',
            'DayOfWeek', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
    # Same as col7, but with some added roadway info
    col9 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN', 'RoadwayFeatureMode', 'yieldSignCount',
            'stopSignCount', 'speedMode', 'FUNC_CLASS', 'DayFrame', 'WeekDay',
            'DayOfWeek', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
    # No roadway variables, except grid num
    col4 = ['Accident', 'Unix', 'Hour',
            'Grid_Num', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    # Variables included after the OLS testing
    col5 = ['Accident', 'Longitude','Latitude','Unix','Join_Count','Grid_Num','TY_TERRAIN','cloudCover','dewPoint',
            'humidity', 'precipIntensity','temperature','uvIndex','visibility','windSpeed','Rain','Cloudy','DayFrame']
    # Variables included after the OLS testing, without weather
    col6 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Join_Count', 'Grid_Num', 'TY_TERRAIN', 'DayFrame']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)
    elif type == 5:
        dataChanged = data.reindex(columns=col5)
    elif type == 6:
        dataChanged = data.reindex(columns=col6)
    elif type == 7:
        dataChanged = data.reindex(columns=col7)
    elif type == 8:
        dataChanged = data.reindex(columns=col8)
    elif type == 9:
        dataChanged = data.reindex(columns=col9)

    return dataChanged


# A new version of determining test types, to avoid over cluttering the previous method
def logReg_test_type_2(data, type):
    # All variables
    col1 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'pressure', 'temperature', 'uvIndex',
            'visibility', 'windSpeed', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek', 'RoadwayFeatureMode', 'yieldSignCount', 'stopSignCount', 'speedMode']
    # All variables, but with the newly added specific roadway/intersection variables
    col5 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
               'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
               'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
               'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
               'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
               'DayOfWeek', 'RoadwayFeatureMode', 'yieldSignCount', 'stopSignCount',
               'speedMode', 'oneWayStop', 'oneWayStopCount', 'twoWayStop',
               'twoWayStopCount', 'oneWayYield', 'oneWayYieldCount', 'twoWayYield',
               'twoWayYieldCount', 'threeWayStop', 'threeWayStopCount', 'fourWayStop',
               'fourWayStopCount', 'trafficSignal', 'trafficSignalCount']
    # No weather variables
    col2 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek', 'RoadwayFeatureMode', 'yieldSignCount', 'stopSignCount',
            'speedMode']
    # Same as col2, but with aggregated weather added in
    col3 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek', 'RoadwayFeatureMode', 'yieldSignCount', 'stopSignCount',
            'speedMode', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore']
    # No roadway variables, except grid num
    col4 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Grid_Num', 'cloudCover', 'dewPoint', 'humidity',
            'precipIntensity', 'pressure', 'temperature', 'uvIndex',
            'visibility', 'windSpeed', 'Rain', 'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)
    elif type == 5:
        dataChanged = data.reindex(columns=col5)

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


# This performs the actual predictions
def logRegForecast(X, Y, newColumns, modelType):
    # Have a list of the days you want to predict for
    # Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
    beginDate = '2021-01-01'
    endDate = '2021-01-31'
    dates = pandas.date_range(beginDate, endDate)
    for date in dates:
        date = str(date).split(" ")[0]
        print("Date is ", date)
        # This file read-in requires that the date provided match the format of the date in the file name
        # predictData = pandas.read_csv(
        #     "../Main Dir/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))
        predictData = pandas.read_csv(
            "../Main Dir/Forecasting/Forecast Files Trimmed/Forecast Forum %s-Filled.csv" % str(date))
        # Drop rows with empty values, otherwise it throws off our accuracies
        predictData = predictData.dropna()
        if "speedMode" in predictData.columns:
            predictData = predictData[predictData['speedMode'] > 0]

        # Split the data into training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
        # Create our logistic regression model
        logreg = LogisticRegression(solver='newton-cg', class_weight='balanced')
        # Fit the model to our training data
        logreg.fit(X_train, y_train)

        # These determine what variables to keep
        predictData = predictData.reindex(columns=newColumns)
        # Standardize the data
        standPredictData = standardize(predictData)
        # Perform predictions
        y_pred = logreg.predict(standPredictData)
        y_prob = logreg.predict_proba(standPredictData)[:, 1]  # get the actual probabilities
        predictData["Prediction"] = y_pred
        predictData['Probability'] = y_prob
        predictData.to_csv("../Main Dir/Logistic Regression Tests/LogReg_%s_Forecast_%s.csv" % (modelType, date),
                           index=False)


# Add weather to accidents
def add_weather(data, weather):
    print("Adding Weather")
    data.Unix = data.Unix.astype(int)
    weather.Unix = weather.Unix.astype(int)
    data.Grid_Num = data.Grid_Num.astype(int)
    weather.Grid_Num = weather.Grid_Num.astype(int)
    # Merge the weather variables for the hour of the accident based on time and grid num
    newdata = pandas.merge(data, weather[['Grid_Num', 'Unix', 'Clear']], on=['Unix', 'Grid_Num'])

    return newdata


# The data to create the model from
data = pandas.read_csv("../Main Dir/Spatial Shift Negatives/SS Data 50-50 Split (2020 Update).csv")
print(data.columns)
exit()
# The type model, it reflects the negative sampling used and the data ratio split
modelType = 'SS 5050'
# set what variables to use
# cutData = logReg_test_type(data, 1)
cutData = logReg_test_type_2(data, 5)
# standardize the data
standData = standardize(cutData)

##################################### Dropping columns from logReg_test_type ###########################################
# All vars dropped variables (Test Type 1)
# standData = standData.drop(['Unix', 'Hour', 'WeekDay', 'DayOfWeek', 'NBR_LANES', "RainBefore", 'pressure',
#                             'dewPoint'], axis=1)

# No weather dropped variables (Test Type 3)
# standData = standData.drop(['Unix', 'FUNC_CLASS'], axis=1)
# Test Type 3 alternate drops based on VIF scores
# standData = standData.drop(['Latitude', 'Longitude', 'Unix', 'FUNC_CLASS'], axis=1)

# Test Type 7 variable drops based on VIF scores
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow'],
#                            axis=1) # v1
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'Cloudy',
#                             'Foggy', 'Rain', 'RainBefore'], axis=1) # v2
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow',
#                             'NBR_LANES', 'Clear', 'Foggy'], axis=1)  # v3
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'Cloudy',
#                             'Foggy', 'Rain', 'RainBefore', 'speedMode'], axis=1) # v4
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'Cloudy',
#                             'Foggy', 'Rain', 'RainBefore', 'yieldSignCount', 'stopSignCount'], axis=1) # v5
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'Cloudy',
#                             'Foggy', 'Rain', 'RainBefore', 'yieldSignCount', 'stopSignCount', 'speedMode'],
#                              axis=1)  # v6

# No location dropped variables (Test Type 4)
# standData = standData.drop(['pressure', 'RainBefore'], axis=1)

# Col 5 vars to drop based on VIF scores
# standData = standData.drop(['dewPoint', 'Latitude', 'Longitude'], axis=1)
# standData = standData.drop(['cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'uvIndex',
#                             'visibility', 'windSpeed'], axis=1)
# Col 6 variables dropped (OLS without weather)
# standData = standData.drop(['Unix'], axis=1)
########################################################################################################################

###################################### Dropping Variables for logReg_test_type_2 #######################################
# (Test Type 1)
# Dropping variables based on logit table
# standData = standData.drop(['pressure', 'TY_TERRAIN', 'NBR_LANES'], axis=1)
# Dropping variables based on VIF scores (dropped until all scores were < 10) then dropping more based on logit table
# standData = standData.drop(['pressure', 'TY_TERRAIN', 'NBR_LANES', 'temperature', 'Latitude', 'Longitude', 'Cloudy',
#                             'FUNC_CLASS', 'humidity', 'visibility', 'dewPoint', 'RainBefore', 'Unix', 'speedMode',
#                             'DayOfWeek'], axis=1)  # T1 v2
# Dropping more vars based on VIF scores (dropped until all scores were < 5)
# standData = standData.drop(['pressure', 'TY_TERRAIN', 'NBR_LANES', 'temperature', 'Latitude', 'Longitude', 'Cloudy',
#                             'FUNC_CLASS', 'humidity', 'visibility', 'dewPoint', 'RainBefore', 'Unix', 'speedMode',
#                             'DayOfWeek', 'cloudCover', 'Hour'], axis=1)  # T1 v3
# Same as T1 V2, but dropped stopSignCount and yieldSignCount instead of speedMode
# standData = standData.drop(['pressure', 'TY_TERRAIN', 'NBR_LANES', 'temperature', 'Latitude', 'Longitude', 'Cloudy',
#                             'FUNC_CLASS', 'humidity', 'visibility', 'dewPoint', 'RainBefore', 'Unix', 'stopSignCount',
#                             'yieldSignCount'], axis=1)  # T1 v4
# T1 V4, but dropping variables based on VIF score (dropped until all scores were < 5) then dropping more vars based
# on logit table
# standData = standData.drop(['pressure', 'TY_TERRAIN', 'NBR_LANES', 'temperature', 'Latitude', 'Longitude', 'Cloudy',
#                             'FUNC_CLASS', 'humidity', 'visibility', 'dewPoint', 'RainBefore', 'Unix', 'stopSignCount',
#                             'yieldSignCount', 'Hour', 'cloudCover', 'WeekDay', 'Clear'], axis=1)  # T1 v5

########################################################################################################################

################ Dropping Variables for logReg_test_type_2 with new roadway/intersection variables #####################
# Dropping variables based on logit table, focusing on count version of etrims data, dropped additional vars based
# on VIF values (dropped until all values were < 10)
# standData = standData.drop(['RoadwayFeatureMode', 'stopSignCount', 'yieldSignCount', 'oneWayStop','twoWayStop',
#                             'oneWayYield', 'twoWayYield', 'threeWayStop', 'fourWayStop', 'trafficSignal', 'pressure',
#                             'NBR_LANES', 'TY_TERRAIN', 'twoWayYieldCount', 'temperature', 'Latitude', 'Longitude',
#                             'Cloudy', 'humidity', 'FUNC_CLASS', 'visibility', 'dewPoint'], axis=1)  # V1
# Dropping more variables based on logit tables
# standData = standData.drop(['RoadwayFeatureMode', 'stopSignCount', 'yieldSignCount', 'oneWayStop','twoWayStop',
#                             'oneWayYield', 'twoWayYield', 'threeWayStop', 'fourWayStop', 'trafficSignal', 'pressure',
#                             'NBR_LANES', 'TY_TERRAIN', 'twoWayYieldCount', 'temperature', 'Latitude', 'Longitude',
#                             'Cloudy', 'humidity', 'FUNC_CLASS', 'visibility', 'dewPoint', 'RainBefore', 'Unix',
#                             'fourWayStopCount'], axis=1)  # V2
# Dropped more variables based on VIF scores (dropped til all scores were < 5)
standData = standData.drop(['RoadwayFeatureMode', 'stopSignCount', 'yieldSignCount', 'oneWayStop','twoWayStop',
                            'oneWayYield', 'twoWayYield', 'threeWayStop', 'fourWayStop', 'trafficSignal', 'pressure',
                            'NBR_LANES', 'TY_TERRAIN', 'twoWayYieldCount', 'temperature', 'Latitude', 'Longitude',
                            'Cloudy', 'humidity', 'FUNC_CLASS', 'visibility', 'dewPoint', 'RainBefore', 'Unix',
                            'fourWayStopCount', 'cloudCover', 'Hour', 'WeekDay'], axis=1)  # V3
########################################################################################################################

# Statement to cut out the entries that have a speedMode of -1, meaning no speed information was available for the
# associated grid num
# only triggers if speedMode is in the list of columns being used
if "speedMode" in standData.columns:
    standData = standData[standData['speedMode'] > 0]

newColumns = list(standData.columns[1:(len(standData.columns) + 1)])
X = standData.iloc[:, 1:(len(standData.columns) + 1)].values  # Our independent variables
Y = standData.iloc[:, 0].values  # Our dependent variable

# Perform predictions
# In general, I think it's a good idea to run the other code below this method first to get a better understanding
# of your data
logRegForecast(X, Y, newColumns, modelType)
exit()

# Make a Logic Table
logit_model = sm.Logit(Y, X)
result = logit_model.fit()
print(result.summary(xname=newColumns))

# Split the data and create the model
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
# logreg = LogisticRegression(solver='newton-cg', class_weight='balanced')
# logreg.fit(X_train, y_train)

# Predicting on the training set and printing the accuracy
# y_pred = logreg.predict(X_test)
# logAcc = logreg.score(X_test, y_test) * 100
# print('Accuracy of logistic regression classifier on test set: ', round(logAcc, 2))

# Getting the confusion matrix values for the predictions (TN, FP, FN, TN)
# confusion_matrix = confusion_matrix(y_test, y_pred)
# print("TP: ", confusion_matrix[0][0])
# print("FP: ", confusion_matrix[0][1])
# print("FN: ", confusion_matrix[1][0])
# print("TN: ", confusion_matrix[1][1])

# Getting the Precision, Recall, F1 Score, and Support
# print(classification_report(y_test, y_pred))

# The following code is used to perform predictions directly on future accidents, not potential hotspots #
# dateSelect = '1/31/2020'  # Select what date you want to use

# rawAcc = pandas.read_csv("../Main Dir/Accident Data/2020 Accidents to 11-18-2020.csv")
# weather = feather.read_dataframe("../Ignore/2020 Weather Aug 30.feather")
# grid_info = pandas.read_csv("../Pre Thesis/Grid Hex Layout/HexGridInfo.csv")

# cutAcc = rawAcc[rawAcc['Date'] == dateSelect]  # cut the accidents to the date you want
# cutAcc = cutAcc[cutAcc['Grid_Num'].notna()]  # drop accidents with missing Grid_Num
# Add in necessary variables
# cutAcc['Join_Count'] = 0
# cutAcc['NBR_LANES'] = 0
# cutAcc['DayFrame'] = 0
# cutAcc['DayOfWeek'] = 0

# cutAcc.DayFrame = cutAcc.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23
# else (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
# cutAcc.Hour = cutAcc.Hour.astype(int)
# cutAcc.Date = cutAcc.Date.astype(str)
#
# for i, _ in enumerate(cutAcc.values):
#     timestamp = str(cutAcc.Date.values[i]) + " " + str(int(cutAcc.Hour.values[i]))
#     thisDate = datetime.strptime(timestamp, "%m/%d/%Y %H")
#     cutAcc.DayOfWeek.values[i] = thisDate.weekday()
#     # Adding in roadway info
#     try:
#         info_row_num = grid_info.loc[grid_info["Grid_Num"] == cutAcc.Grid_Num.values[i]].index[0]
#         cutAcc.Join_Count.values[i] = grid_info.Join_Count.values[info_row_num]
#         cutAcc.NBR_LANES.values[i] = grid_info.NBR_LANES.values[info_row_num]
#     except:
#         print("Error in assigning roadway info")
# # Adding in weather, we only need 1 weather variable
# cutAcc = add_weather(cutAcc, weather)
# # Reset our columns
# foreColumns = ['Accident', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'DayFrame', 'DayOfWeek', 'Clear']
# cutAcc['Accident'] = 1
# cutAcc = cutAcc.reindex(columns=foreColumns)
# # Standardize our data
# standAcc = standardize(cutAcc)
# # Reset the accident column to be all 1's, bc for some reason the standardize function sets its values to 0.0
# standAcc['Accident'] = 1.0
#
# fore_X_test = standAcc.iloc[:, 1:(len(standAcc.columns) + 1)].values  # Our independent variables
# fore_Y_test = standAcc.iloc[:, 0].values  # Our dependent variable
#
# # Predicting on the training set and printing the accuracy
# fore_y_pred = logreg.predict(fore_X_test)
# logAcc = logreg.score(fore_X_test, fore_Y_test) * 100
# print('Accuracy: ', round(logAcc, 2))
#
# # Getting the confusion matrix values for the predictions (TN, FP, FN, TN)
# confusion_matrix = confusion_matrix(fore_Y_test, fore_y_pred)
# print("TP: ", confusion_matrix[1][1])
# print("FN: ", confusion_matrix[1][0])
