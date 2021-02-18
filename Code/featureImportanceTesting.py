"""
Author: Jeremy Roland
Purpose: Code file for finding the important features of the dataset
"""
import pandas
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.formula.api import ols
import numpy


def test_type(data, type):
    """
    An easy to use method for selecting which variables to use for the testing you do
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
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)

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


def univariateSelection(data):
    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    scaledData = pandas.DataFrame(scaled_df, columns=columns)

    features = scaledData.columns.values[1:len(scaledData.columns.values)]
    X = scaledData.loc[:, features].values  # Separating out the target variables
    y = scaledData.loc[:, ['Accident']].values  # dependent variable

    bestFeatures = SelectKBest(score_func=chi2, k=15)
    fit = bestFeatures.fit(X, y)
    dfScores = pandas.DataFrame(fit.scores_)
    dfColumns = pandas.DataFrame(features)

    # concat two dataframes for better visualization
    featureScores = pandas.concat([dfColumns, dfScores], axis=1)
    featureScores.columns = ['Specs', 'Score']  # naming the dataframe columns
    print(featureScores.nlargest(15, 'Score'))  # print 10 best features


def featureSelection(data):
    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    scaledData = pandas.DataFrame(scaled_df, columns=columns)

    features = scaledData.columns.values[1:len(scaledData.columns.values)]
    X = scaledData.loc[:, features].values  # Separating out the target variables
    y = scaledData.loc[:, ['Accident']].values  # dependent variable

    model = ExtraTreesClassifier()
    model.fit(X, y)
    print(model.feature_importances_)  # use inbuilt class feature_importances of tree based classifiers

    # plot graph of feature importances for better visualization
    feat_importances = pandas.Series(model.feature_importances_, index=features)
    feat_importances.nlargest(15).plot(kind='barh')
    plt.xlim(0, .50)
    plt.title("")
    plt.show()


def correlationHeatmap(data):
    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    scaledData = pandas.DataFrame(scaled_df, columns=columns)

    # Version 1
    # get correlations of each features in dataset
    # corrmat = scaledData.corr()
    # top_corr_features = corrmat.index
    # plt.figure(figsize=(30, 30))
    # #plot heat map
    # g = sns.heatmap(data[top_corr_features].corr(), annot=True, cmap="RdYlGn")
    # plt.show()

    # Version 2
    # This version allows for the creation of a heatmap that removes redundancy (takes away the top right half of the
    # heatmap for less noise)
    # Create the correlation dataframe
    corr = abs(scaledData.corr())
    # Drop self-correlations
    dropSelf = numpy.zeros_like(corr)
    dropSelf[numpy.triu_indices_from(dropSelf)] = True
    # Generate color map
    # colormap = sns.diverging_palette(220, 10, as_cmap=True)
    # Generate the heatmap, allowing annotations and place floats in the map
    sns.heatmap(corr, cmap='Greens', annot=True, fmt='.2f', mask=dropSelf)
    # xticks
    plt.xticks(range(len(corr.columns)), corr.columns)
    # yticks
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.show()


def calculate_vif(data):
    vif = pandas.DataFrame()
    vif["variables"] = data.columns
    vif["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    print(vif)


def get_ols(formula, data):
    """
    Formula should be in the following form: 'dependentVariable~indepVar+indepVar+indepVar+...'
    """
    mlr = ols(formula, data)
    estimates = mlr.fit()
    print(estimates.summary())


# Read in the file and set what the test number is, that's all you've gotta change
file = "Main Dir/Spatial Shift Negatives/SS Data 50-50 Split (2020 Update).csv"
testNum = 5

data = pandas.read_csv("../%s" % file)
cutData = logReg_test_type_2(data, testNum)
cutData = cutData.drop(['RoadwayFeatureMode', 'oneWayStop', 'twoWayStop', 'oneWayYield', 'twoWayYield',
                            'threeWayStop', 'fourWayStop', 'trafficSignal', 'pressure', 'TY_TERRAIN', 'NBR_LANES',
                            'oneWayYieldCount', 'fourWayStopCount'], axis=1)

if "speedMode" in cutData.columns:
    cutData = cutData[cutData['speedMode'] > 0]

cutData = standardize(cutData)
calculate_vif(cutData)
