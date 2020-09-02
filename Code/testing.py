# This file is kept empty for testing small chunks of code easily.
# Please clear this file when you are done working on the code, and put it into whatever file it needs to go in.
import numpy as np
import lime
import lime.lime_tabular
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn import preprocessing
import pandas
from sklearn.model_selection import train_test_split


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


def wrapPrediction(predict):
    return lambda x: np.array([predict([x]), 1 - predict([x])])


data = pandas.read_csv("../Jeremy Thesis/Total Shift/Data/TS Data 50-50 Split.csv")
cutData = test_type(data, 1)
standData = standardize(cutData)

X = standData.iloc[:, 1:(len(standData.columns) + 1)].values
Y = standData.iloc[:, 0].values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=7)

model = Sequential()
model.add(Dense(X.shape[1], input_dim=X.shape[1], activation='sigmoid'))
model.add(Dense(X.shape[1] - 5, activation='sigmoid'))
model.add(Dropout(.1))
try:
    model.add(Dense(X.shape[1] - 10, activation='sigmoid'))
except:
    model.add(Dense(X.shape[1] - 5, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

# Our current set model.
model.load_weights("../Jeremy Thesis/Total Shift/Model Results/model_TS_50-50Split_Test1.h5")

explainer = lime.lime_tabular.LimeTabularExplainer(X_train, feature_names=standData.columns,
                                                   class_names=['Accident', 'No Accident'], discretize_continuous=True)
i = np.random.randint(0, X_test.shape[1])
exp = explainer.explain_instance(X_test[i], wrapPrediction(model.predict), num_features=2)

exp.show_in_notebook(show_table=True, show_all=False)
