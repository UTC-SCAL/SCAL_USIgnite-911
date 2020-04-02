"""
Code file for finding the important features of the dataset
"""
import pandas
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import numpy


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """
    col1 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col2 = ['Accident', 'Clear', 'Cloudy', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col3 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col4 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
             'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
             'WeekDay', 'cloudCover', 'precipIntensity']

    col5 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
             'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
             'WeekDay', 'cloudCover', 'precipIntensity']

    col6 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']
    if type == 1:
        data = data.reindex(columns=col1)
    elif type == 2:
        data = data.reindex(columns=col2)
    elif type == 3:
        data = data.reindex(columns=col3)
    elif type == 4:
        data = data.reindex(columns=col4)
    elif type == 5:
        data = data.reindex(columns=col5)
    elif type == 6:
        data = data.reindex(columns=col6)

    return data


def univariateSelection(data):
    # Drop this column since it has a negative in it, and feature selection doesn't accept negatives
    # data = data.drop(['ConflictEffect'], axis=1)

    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    data = pandas.DataFrame(scaled_df, columns=columns)

    features = data.columns.values[1:len(data.columns.values)]
    X = data.loc[:, features].values  # Separating out the target variables
    y = data.loc[:, ['Accident']].values  # dependent variable

    bestFeatures = SelectKBest(score_func=chi2, k=10)
    fit = bestFeatures.fit(X, y)
    dfScores = pandas.DataFrame(fit.scores_)
    dfColumns = pandas.DataFrame(features)

    #concat two dataframes for better visualization
    featureScores = pandas.concat([dfColumns, dfScores], axis=1)
    featureScores.columns = ['Specs','Score']  # naming the dataframe columns
    print(featureScores.nlargest(10,'Score'))  # print 10 best features


def featureSelection(data, testNum):
    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    data = pandas.DataFrame(scaled_df, columns=columns)

    features = data.columns.values[1:len(data.columns.values)]
    X = data.loc[:, features].values  # Separating out the target variables
    y = data.loc[:, ['Accident']].values  # dependent variable

    model = ExtraTreesClassifier()
    model.fit(X, y)
    print(model.feature_importances_)  # use inbuilt class feature_importances of tree based classifiers

    # plot graph of feature importances for better visualization
    feat_importances = pandas.Series(model.feature_importances_, index=features)
    feat_importances.nlargest(20).plot(kind='barh')
    plt.xlim(0, .50)
    plt.title("Feature Selection Total Shift No Split Test % d MMR" % testNum)
    plt.show()


def correlationHeatmap(data):
    # If we want to MinMaxReduce the data (normalize it)
    # Get the columns of the data
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(data)
    data = pandas.DataFrame(scaled_df, columns=columns)

    # Version 1
    # get correlations of each features in dataset
    # corrmat = data.corr()
    # top_corr_features = corrmat.index
    # plt.figure(figsize=(30, 30))
    # #plot heat map
    # g = sns.heatmap(data[top_corr_features].corr(), annot=True, cmap="RdYlGn")
    # plt.show()

    # Version 2
    # This version allows for the creation of a heatmap that removes redundancy (takes away the top right half of the
    # heatmap for less noise)
    # Create the correlation dataframe
    corr = abs(data.corr())
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


data = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/TS Negatives No Split.csv")
# data = data.drop(['City', 'Latitude', 'Longitude', 'precipProbability', 'precipType', 'Event', 'Conditions',
#                   'hourbefore', 'Date', 'GRID_ID', 'windBearing', 'windGust', 'pressure', 'Unix', 'cloudCover',
#                   'dewPoint'], axis=1)
data = data.reindex(columns=['Accident', 'Join_Count', 'temperature', 'humidity', 'windSpeed', 'Hour', 'uvIndex',
                             'Grid_Num', 'visibility', 'DayFrame', 'precipIntensity', 'DayOfWeek', 'FUNC_CLASS', 'NBR_LANES'])
data.to_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/TS Negatives 75-25 Split Top 13.csv")
exit()
testNum = 0
# data = test_type(data, testNum)
# PCA_testing(data)
# univariateSelection(data)
featureSelection(data, testNum)
# correlationHeatmap(data)
