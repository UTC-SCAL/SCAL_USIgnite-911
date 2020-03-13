"""
Code file for finding the important features of the dataset
"""
import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import numpy


def PCA_testing(data):
    """
    Principal Component Analysis
    But, this takes away the labels of your data, so it's hard to impossible to really know which principal components
        it returns. I wouldn't really recommend this one.
    """
    # First, we read in our data
    data.avgReactionTime = data.avgReactionTime.astype(float)
    data.Avg_RT_App = data.Avg_RT_App.astype(float)

    # Next, we scale the data, which we have two types to use (Standard and Normalizing)
    # Separating out the features
    features = data.columns.values[1:len(data.columns.values)]
    x = data.loc[:, features].values  # Separating out the target

    ## Put your independent variable here ##
    y = data.loc[:, ['']].values  # Standardizing the features

    x = StandardScaler().fit_transform(x)

    # Now, reduce the dimensionality of the dataset
    # In this step, the labels of the variables are removed, so they basically lose their meaning
    pca = PCA(n_components=10)
    principalComponents = pca.fit_transform(x)
    principalDf = pandas.DataFrame(data=principalComponents, columns=['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8',
                                                                      'pc9', 'pc10'])

    # Concatenate the principal component dataframe to our dependent variable
    ## Put your independent variable here ##
    finalDf = pandas.concat([principalDf, data[['']]], axis=1)

    # Save the dataframe containing the principal components
    finalDf.to_csv("../")

    # Print off an explanation of the variance ratios for the different principal components
    # This tells us how much information (variance) can be attributed to each of the principal components
    print(pca.explained_variance_ratio_)
    # We can also print out the correlations that each PC has on the variables in the dataset
    pcaCorrelations = pandas.DataFrame(pca.components_, columns=features, index=['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6',
                                                                                 'pc7', 'pc8', 'pc9', 'pc10'])
    print(pcaCorrelations)
    pcaCorrelations.to_csv("../")


def univariateSelection(data):
    """
    This returns straight numbers for reflecting importance
    Below, there are sections for normalizing the data if you want to see how that affects your data
    """
    # If we want to MinMaxReduce the data (normalize it)
    ## Uncomment these 4 lines to normalize your data ##
    # columns = data.columns.values[0:len(data.columns.values)]
    # scaler = preprocessing.MinMaxScaler()
    # scaled_df = scaler.fit_transform(data)
    # data = pandas.DataFrame(scaled_df, columns=columns)

    features = data.columns.values[1:len(data.columns.values)]
    X = data.loc[:, features].values  # Separating out the target variables

    ## Put your dependent variable here ##
    y = data.loc[:, ['']].values  # dependent variable

    # Below, you can change the value of k to return more or less variables for your "best" variables in the dataset
    bestFeatures = SelectKBest(score_func=chi2, k=10)
    fit = bestFeatures.fit(X, y)
    dfScores = pandas.DataFrame(fit.scores_)
    dfColumns = pandas.DataFrame(features)

    #concat two dataframes for better visualization
    featureScores = pandas.concat([dfColumns, dfScores], axis=1)
    featureScores.columns = ['Specs','Score']  # naming the dataframe columns
    # Also, change the 10 below to whatever value you set K to
    print(featureScores.nlargest(10,'Score'))  # print 10 best features


def featureSelection(data):
    """
    This returns a horizontal bar graph showing the most important features
    """
    # If we want to MinMaxReduce the data (normalize it)
    ## Uncomment these 4 lines to normalize your data ##
    # columns = data.columns.values[0:len(data.columns.values)]
    # scaler = preprocessing.MinMaxScaler()
    # scaled_df = scaler.fit_transform(data)
    # data = pandas.DataFrame(scaled_df, columns=columns)

    features = data.columns.values[1:len(data.columns.values)]
    X = data.loc[:, features].values  # Separating out the target variables

    ## Put your dependent variable here ##
    y = data.loc[:, ['']].values  # dependent variable

    model = ExtraTreesClassifier()
    model.fit(X, y)
    print(model.feature_importances_)  # use inbuilt class feature_importances of tree based classifiers

    # plot graph of feature importances for better visualization
    feat_importances = pandas.Series(model.feature_importances_, index=features)
    # Below, change the nlargest() input to however many variables you want showed
    feat_importances.nlargest(10).plot(kind='barh')
    plt.show()


def correlationHeatmap(data):
    """
    This returns a heatmap of all the variables, showing how each variable correlates with your dependent variable and
        the other variables in the dataset
    """
    # If we want to MinMaxReduce the data (normalize it)
    ## Uncomment these 4 lines to normalize your data ##
    # columns = data.columns.values[0:len(data.columns.values)]
    # scaler = preprocessing.MinMaxScaler()
    # scaled_df = scaler.fit_transform(data)
    # data = pandas.DataFrame(scaled_df, columns=columns)

    corr = data.corr()
    # Drop self-correlations
    dropSelf = numpy.zeros_like(corr)
    dropSelf[numpy.triu_indices_from(dropSelf)] = True
    # Generate color map
    colormap = sns.diverging_palette(220, 10, as_cmap=True)
    # Generate the heatmap, allowing annotations and place floats in the map
    sns.heatmap(corr, cmap=colormap, annot=False, fmt='.2f', mask=dropSelf)
    # xticks
    plt.xticks(range(len(corr.columns)), corr.columns)
    # yticks
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.show()


def appendingAccidentFiles():
    # Read in the files you want to append together
    acc1 = pandas.read_csv("../")
    acc2 = pandas.read_csv("../")
    acc3 = pandas.read_csv("../")

    # append the files together
    bigBOI = pandas.concat([acc1, acc2, acc3], axis=0, join='outer', ignore_index=False)

    # printing before and after lengths to see if we dropped any duplicate values
    print(len(bigBOI))
    bigBOI.drop_duplicates(keep="first", inplace=True)
    print(len(bigBOI))

    # Save the concatenated files
    bigBOI.to_csv("../")


def creatingDateData(data):
    # Splitting the date into year, day, and month values
    # Depending on how the date is formatted, you'll need to change the split value and position
    # Ex: if the date is formatted as yyyy-mm-dd, the split value will be split("-")[0] for year
    data['Year'] = data.apply(lambda x: x.Date.split("-")[0], axis=1)
    data['Day'] = data.apply(lambda x: x.Date.split("-")[2], axis=1)
    data['Month'] = data.apply(lambda x: x.Date.split("-")[1], axis=1)
    data.to_csv("../")


data = pandas.read_csv("")
# Drop any variables, if you want
# data = data.drop([], axis=1)
# uncomment which method you want to run
# For these tests, you'll have to define what your dependent variable is
# PCA_testing(data)
# univariateSelection(data)
# featureSelection(data)
# correlationHeatmap(data)
