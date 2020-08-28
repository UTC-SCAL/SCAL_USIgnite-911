# This file is kept empty for testing small chunks of code easily.
# Please clear this file when you are done working on the code, and put it into whatever file it needs to go in.
from sklearn import preprocessing
import pandas


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


data = pandas.read_csv("../Jeremy Thesis/Total Shift/Data/TS Data 50-50 Split.csv")
cutData = test_type(data, 1)
standData = standardize(cutData)
X = standData.iloc[:, 1:(len(standData.columns) + 1)].values  # Our independent variables
Y = standData.iloc[:, 0].values  # Our dependent variable

