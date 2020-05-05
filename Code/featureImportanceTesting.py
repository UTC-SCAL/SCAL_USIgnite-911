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


def featureSelection(data, figName, modelName):
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
    feat_importances.nlargest(15).plot(kind='barh')
    plt.xlim(0, .50)
    plt.title(figName)
    plt.savefig("../Jeremy Thesis/"+modelName+"/Feature Selection/"+figName+".png", bbox_inches='tight')
    # plt.show()


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


def automatedRunner():
    """
    An automated code runner to go through a list of files and runs feature selection for those files
    I made this for my thesis, but I thought I'd save it just for potential future use
    """
    files = ['Jeremy Thesis/Grid Fix/Data/GF Data No Split.csv', 'Jeremy Thesis/Grid Fix/Data/GF Data 50-50 Split.csv', 'Jeremy Thesis/Grid Fix/Data/GF Data 75-25 Split.csv',
             'Jeremy Thesis/Hour Shift/Data/HS Data No Split.csv', 'Jeremy Thesis/Hour Shift/Data/HS Data 50-50 Split.csv', 'Jeremy Thesis/Hour Shift/Data/HS Data 75-25 Split.csv',
             'Jeremy Thesis/Spatial Shift/Data/SS Data No Split.csv', 'Jeremy Thesis/Spatial Shift/Data/SS Data 50-50 Split.csv', 'Jeremy Thesis/Spatial Shift/Data/SS Data 75-25 Split.csv',
             'Jeremy Thesis/Total Shift/Data/TS Data No Split.csv', 'Jeremy Thesis/Total Shift/Data/TS Data 50-50 Split.csv', 'Jeremy Thesis/Total Shift/Data/TS Data 75-25 Split.csv', ]
    for file in files:
        data = pandas.read_csv("../%s" % file)
        for i in range(1, 5):
            testNum = i
            cutData = test_type(data, testNum)
            if "Grid Fix" in file:
                modelName = "Grid Fix"
                figName = "Feature Selection GF " + file.split(" ")[4] + " Split Test %d" % testNum
            elif "Hour Shift" in file:
                modelName = "Hour Shift"
                figName = "Feature Selection HS " + file.split(" ")[4] + " Split Test %d" % testNum
            elif "Spatial Shift" in file:
                modelName = "Spatial Shift"
                figName = "Feature Selection SS " + file.split(" ")[4] + " Split Test %d" % testNum
            elif "Total Shift" in file:
                modelName = "Total Shift"
                figName = "Feature Selection TS " + file.split(" ")[4] + " Split Test %d" % testNum
            else:
                modelName = 0
            featureSelection(cutData, figName, modelName)


# PCA_testing(data)
# univariateSelection(data)
# featureSelection(cutData, figName, modelName)
# correlationHeatmap(data)