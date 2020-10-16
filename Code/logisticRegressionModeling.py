from sklearn import preprocessing
import pandas
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def logReg_test_type(data, type):
    col1 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col3 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS',  'DayFrame', 'WeekDay',
            'DayOfWeek']

    col4 = ['Accident', 'Unix', 'Hour',
            'Grid_Num', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
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


def dropCols(data, testType):
    """
    Drops variables based on p-values from logit table 
    """
    if testType == 1:
        droppedData = data.drop(['Unix', 'NBR_LANES', 'dewPoint', 'pressure', 'temperature', 'RainBefore'], axis=1)
    elif testType == 3:
        droppedData = data.drop(['Unix'], axis=1)
    elif testType == 4:
        droppedData = data.drop(['pressure', 'RainBefore'], axis=1)
    return droppedData


def logRegForecast(X, Y, newColumns, testType, modelName):
    # Have a list of the days you want to predict for
    # Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
    dates = ['1-1-2020', '1-2-2020', '1-3-2020', '1-4-2020', '1-5-2020', '1-6-2020', '1-7-2020', '1-8-2020', '1-9-2020',
             '1-10-2020', '1-11-2020', '1-12-2020', '1-13-2020', '1-14-2020', '1-15-2020', '1-16-2020', '1-17-2020',
             '1-18-2020', '1-19-2020', '1-20-2020', '1-21-2020', '1-22-2020', '1-23-2020', '1-24-2020', '1-25-2020',
             '1-26-2020', '1-27-2020', '1-28-2020', '1-29-2020', '1-30-2020', '1-31-2020']
    for date in dates:
        print("Date is ", date)
        # This file read-in requires that the date provided match the format of the date in the file name
        predictData = pandas.read_csv(
            "../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))
        predictData = predictData.dropna()

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
        logreg = LogisticRegression(solver='newton-cg', class_weight='balanced')
        logreg.fit(X_train, y_train)

        # These determine what variables to keep
        predictData = predictData.reindex(columns=newColumns)
        standPredictData = standardize(predictData)

        y_pred = logreg.predict(standPredictData)
        predictData["Prediction"] = y_pred
        saveName = modelName + "_T" + str(testType) + "_" + str(date)
        predictData.to_csv("../Jeremy Thesis/Logistic Regression Tests/LogReg_Forecast_%s.csv" % saveName, index=False)


dataFiles = ['Jeremy Thesis/Spatial Shift/Data/SS Data 50-50 Split.csv']
testTypes = [3]

for dataFile in dataFiles:
    for testType in testTypes:
        data = pandas.read_csv("../%s" % dataFile)
        modelName = dataFile.split("/")[3].split(".")[0]
        print("LogReg for", modelName, 'T%d' % testType)
        cutData = logReg_test_type(data, testType)  # set what variables to use
        standData = standardize(cutData)  # standardize the data

        # Dropping columns per Logit Table Results #
        droppedData = dropCols(standData, testType)

        newColumns = list(droppedData.columns[1:(len(droppedData.columns) + 1)])
        X = droppedData.iloc[:, 1:(len(droppedData.columns) + 1)].values  # Our independent variables
        Y = droppedData.iloc[:, 0].values  # Our dependent variable

        # Perform predictions
        logRegForecast(X, Y, newColumns, testType, modelName)

        # Split the data and create the model
        # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
        # logreg = LogisticRegression(solver='newton-cg', class_weight='balanced')
        # logreg.fit(X_train, y_train)

        # Predicting on the training set and printing the accruacy
        # y_pred = logreg.predict(X_test)
        # logAcc = logreg.score(X_test, y_test) * 100

        # Getting the confusion matrix values for the predictions (TN, FP, FN, TN)
        # logRegCM = confusion_matrix(y_test, y_pred)
        # print("TP: ", logRegCM[0][0])
        # print("FP: ", logRegCM[0][1])
        # print("FN: ", logRegCM[1][0])
        # print("TN: ", logRegCM[1][1])

        # Getting the Precision, Recall, F1 Score, and Support
        # print(classification_report(y_test, y_pred))
