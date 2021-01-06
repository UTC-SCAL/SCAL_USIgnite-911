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
    dates = ['1-1-2020', '1-2-2020', '1-3-2020', '1-4-2020', '1-5-2020', '1-6-2020', '1-7-2020',
             '1-8-2020', '1-9-2020', '1-10-2020', '1-11-2020', '1-12-2020', '1-13-2020', '1-14-2020',
             '1-15-2020', '1-16-2020', '1-17-2020', '1-18-2020', '1-19-2020', '1-20-2020', '1-21-2020',
             '1-22-2020', '1-23-2020', '1-24-2020', '1-25-2020', '1-26-2020', '1-27-2020', '1-28-2020',
             '1-29-2020', '1-30-2020', '1-31-2020']
    for date in dates:
        print("Date is ", date)
        # This file read-in requires that the date provided match the format of the date in the file name
        predictData = pandas.read_csv(
            "../Main Dir/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))
        # Drop rows with empty values, otherwise it throws off our accuracies
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
        predictData.to_csv("../Main Dir/Logistic Regression Tests/LogReg_%s_Forecast_%s.csv" % (modelType, date),
                           index=False)


# The data to create the model from
data = pandas.read_csv("../Main Dir/Spatial Shift Negatives/SS Data 50-50 Split.csv")
# The type model, it reflects the negative sampling used and the data ratio split
modelType = 'SS 5050'
# set what variables to use
cutData = logReg_test_type(data, 7)
# standardize the data
standData = standardize(cutData)

# Dropping columns per Logit Table Results #
# All vars dropped variables (Test Type 1)
# standData = standData.drop(['Unix', 'Hour', 'WeekDay', 'DayOfWeek', 'NBR_LANES', "RainBefore", 'pressure', 'dewPoint'],
#                             axis=1)

# No weather dropped variables (Test Type 3)
# standData = standData.drop(['Unix', 'FUNC_CLASS'], axis=1)
# Test Type 3 alternate drops based on VIF scores
# standData = standData.drop(['Latitude', 'Longitude', 'Unix', 'FUNC_CLASS'], axis=1)

# Test Type 7 variable drops based on VIF scores
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow'], axis=1) # v1
standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'Cloudy',
                            'Foggy', 'Rain', 'RainBefore'], axis=1) # v2
# standData = standData.drop(['Unix', 'FUNC_CLASS', 'Latitude', 'Longitude', 'TY_TERRAIN', 'WeekDay', 'Snow', 'NBR_LANES',
#                         'Clear', 'Foggy'], axis=1)  # v3

# No location dropped variables (Test Type 4)
# standData = standData.drop(['pressure', 'RainBefore'], axis=1)

# Col 5 vars to drop based on VIF scores
# standData = standData.drop(['dewPoint', 'Latitude', 'Longitude'], axis=1)
# standData = standData.drop(['cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'uvIndex',
#                             'visibility', 'windSpeed'], axis=1)
# Col 6 variables dropped (OLS without weather)
# standData = standData.drop(['Unix'], axis=1)

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
