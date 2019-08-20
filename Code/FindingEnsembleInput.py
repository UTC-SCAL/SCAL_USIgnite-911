import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import logging
# logging.getLogger('tensorflow').disabled = True
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
import feather
import numpy as np
import statistics
import glob
import os

# data = pandas.read_csv("Excel & CSV Sheets/Forecasts/2017-3-12/Forecast/CutGF_50-50_Forecast.csv")

files = glob.glob('./Excel & CSV Sheets/Forecasts/*/Forecast/*.csv')

##Empty lists/dicts for later use. Kept together for simplicity's sake. 
modeltypes = []
dates = []
modelframes = {}
predframes = {}
probframes = {}

##Each of the files from the glob is pulled in, and saved into the modelframes dictionary. 
for f in files: 
    model = (f.split("/")[5]).replace("_Forecast.csv", "")
    date = f.split("/")[3]
    reftitle = model + " " + date
    modeltypes.append(model)
    dates.append(date)
    modelframes[reftitle] = pandas.read_csv(f, sep = ",")

##This area gets only the unique model names, and the dates. 
modelnames = np.unique(modeltypes)
dates = np.unique(dates)

##This goes through all unique dates and creates a dataframe for both predictions and probability. 
for grp in dates:
    #do some calcs to get a dataframe called 'df'
    dfpred = pandas.DataFrame(columns = modelnames)
    dfpred = dfpred.rename_axis('Prediction')
    predframes[grp] = dfpred
 
    dfprob = pandas.DataFrame(columns = modelnames)
    dfprob = dfprob.rename_axis('Probability')
    probframes[grp] = dfprob


##This section goes through all models and finds the prob mean and pred mode for each unique gridblocks, 
# and sets those to the corresponding columns within the correct date. 
count = 0
for model in modelframes:
    # print(model)
    # exit()
    data = modelframes[model]
    data = data[data['Road_Count'] > 0]
    gridblocks = np.unique(data.Grid_Block)
    # gridblocks = gridblocks.sort()
    # print(gridblocks)
    # exit()
    means = []
    modes = []
    modeldate = model.split(" ")[1]
    modelname = model.split(" ")[0]
    print("Model number:",count, "  Model name:", modelname, "Model date:", modeldate)
    count += 1
    for i in gridblocks: 
        gridset = data[data['Grid_Block'] == i]
        try:
            pred = statistics.mode(gridset["Prediction"])
        except:
            pred = 1
        prob = statistics.mean(gridset["Probability"])
        modes.append(pred)
        means.append(prob)
    # print(len(means))
    probframes[modeldate][modelname] = means
    predframes[modeldate][modelname] = modes
    predframes[modeldate]['Grid_Block'] = gridblocks
    probframes[modeldate]['Grid_Block'] = gridblocks
    means.clear()
    modes.clear()


##This section saves the dataframes previously created into an 'Ensemble' folder within each date. 
for name in predframes:
    savepath = "Excel & CSV Sheets/Forecasts/" + name + "/Ensemble/"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    title =  savepath + name + "Prediction.csv"
    predframes[name].to_csv(title, index=False)

for name in probframes:
    savepath = "Excel & CSV Sheets/Forecasts/" + name + "/Ensemble/" 
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    title = savepath + name + "Probability.csv"
    probframes[name].to_csv(title, index=False)

