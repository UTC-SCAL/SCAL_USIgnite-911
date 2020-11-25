"""
Author: Jeremy Roland
Purpose: This was a testing run to create a logistic regression model to predict where our accident hotspots were
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
from sklearn.utils import shuffle


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
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

    col5 = ['Accident', 'Hour', 'Join_Count', 'Grid_Num', 'DayFrame']

    col6 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES',
            'TY_TERRAIN', 'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek']

    col7 = ['Accident', 'Unix', 'Hour', 'Grid_Num', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col8 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'precipIntensity', 'visibility',  'DayFrame', 'WeekDay', 'DayOfWeek']

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
    elif type == 6:
        dataChanged = data.reindex(columns=col6)
    elif type == 7:
        dataChanged = data.reindex(columns=col7)
    elif type == 8:
        dataChanged = data.reindex(columns=col8)

    return dataChanged


# A test type method specific for the logistic regression testing
def logReg_test_type(data, type):
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


# This performs the actual predictions
def logRegForecast(X, Y, newColumns):
    # Have a list of the days you want to predict for
    # Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
    dates = []
    for date in dates:
        print("Date is ", date)
        # This file read-in requires that the date provided match the format of the date in the file name
        predictData = pandas.read_csv(
            "../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))
        predictData = predictData.dropna()

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
        predictData["Prediction"] = y_pred
        predictData.to_csv("../Jeremy Thesis/Logistic Regression Tests/LogReg_Forecast_%s.csv" % date, index=False)


data = pandas.read_csv("../")
cutData = test_type(data, 1)  # set what variables to use
standData = standardize(cutData)  # standardize the data

# Dropping columns per Logit Table Results #
# All vars dropped variables (Test Type 1)
# standData = standData.drop(['Unix', 'NBR_LANES', 'dewPoint', 'pressure', 'temperature', 'RainBefore'], axis=1)
# No weather dropped variables (Test Type 3)
# standData = standData.drop(['Unix'], axis=1)
# No location dropped variables (Test Type 4)
# standData = standData.drop(['pressure', 'RainBefore'], axis=1)

newColumns = list(standData.columns[1:(len(standData.columns) + 1)])
X = standData.iloc[:, 1:(len(standData.columns) + 1)].values  # Our independent variables
Y = standData.iloc[:, 0].values  # Our dependent variable

# Perform predictions
# In general, I think it's a good idea to run the other code below this method first to get a better understanding
# of your data
# logRegForecast(X, Y, newColumns)
# exit()

# Make a Logic Table
logit_model = sm.Logit(Y, X)
result = logit_model.fit()
print(result.summary(xname=newColumns))

# Split the data and create the model
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
logreg = LogisticRegression(solver='newton-cg', class_weight='balanced')
logreg.fit(X_train, y_train)

# Predicting on the training set and printing the accruacy
y_pred = logreg.predict(X_test)
logAcc = logreg.score(X_test, y_test) * 100
print('Accuracy of logistic regression classifier on test set: ', round(logAcc, 2))

# Getting the confusion matrix values for the predictions (TN, FP, FN, TN)
confusion_matrix = confusion_matrix(y_test, y_pred)
print("TP: ", confusion_matrix[0][0])
print("FP: ", confusion_matrix[0][1])
print("FN: ", confusion_matrix[1][0])
print("TN: ", confusion_matrix[1][1])

# Getting the Precision, Recall, F1 Score, and Support
print(classification_report(y_test, y_pred))

# Plotting the ROC curve
# logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
# fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:, 1])
# plt.figure()
# plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
# plt.plot([0, 1], [0, 1], 'r--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve')
# plt.legend(loc="lower right")
# plt.show()
