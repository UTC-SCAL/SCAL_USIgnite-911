try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
import numpy
import datetime
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import logging
logging.getLogger('tensorflow').disabled = True
import pytz
import pandas
import math
import feather
import tensorflow as tf
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn import preprocessing

start = datetime.datetime.now()
all_weather = feather.read_dataframe("../Ignore/Weather/ALL_Weather_with_Binary.feather")

data = pandas.read_csv("Excel & CSV Sheets/Grid Files/Grid Oriented Layout/Forecast Forum Ori Filled.csv", sep=",")
##Adjusting column types and such
data['Hour'] = data['Hour'].astype(int)
data['DayFrame'] = data['DayFrame'].astype(int)


## Step 0 - ONLY IF NEEDED. This takes a listing of gridblocks and creates the full forecast file 
def fillForecastFile(places, filename):
    ##Gets the forecast data for every 4 hours. 
    fulldata = places.copy()
    for i in range(0,25,4):
        if i ==0:
            pass
        else:
            name = ('places'+str(i))
            print(name)
            if i == 24:
                places.Hour = 23
            else:
                places.Hour = i
            if 0<=i<7 or 19<=i<=23:
                places.DayFrame = 1
            elif 7<=i<10:
                places.DayFrame = 2
            elif 10<=i<13:
                places.DayFrame = 3
            elif 13<=i<19:
                places.DayFrame = 4
            print(places.Hour[0:5], places.DayFrame[0:5])
            fulldata = fulldata.append(places)
    fulldata = fulldata.drop_duplicates()
    print("Finished data size:",fulldata.size)
    fulldata.to_csv(filename, sep=",", index=False)

## Step 0 - ONLY IF NEEDED
def finding_binaries(data):
    starttime = datetime.datetime.now()
    print("Beginning Lowercase conversion at:", starttime)
    data.Event = data.Event.apply(lambda x: x.lower())
    data.Conditions = data.Conditions.apply(lambda x: x.lower())
    data.EventBefore = data.EventBefore.apply(lambda x: x.lower())
    data.ConditionBefore = data.ConditionBefore.apply(lambda x: x.lower())
    lowertime = datetime.datetime.now()
    print("Lowercase conversion done, Beginning Binary Lambdas at:", lowertime - starttime)
    data['Rain'] = data.apply(lambda x : 1 if ("rain" in x.Event or "rain" in x.Conditions) else 0, axis=1)
    raintime = datetime.datetime.now()
    print("Rain completed in:", raintime - lowertime)
    data['Cloudy'] = data.apply(lambda x : 1 if ("cloud" in x.Event or "cloud" in x.Conditions) else 0, axis=1)
    cloudtime = datetime.datetime.now()
    print("Cloudy completed in:", cloudtime - raintime)
    data['Foggy'] = data.apply(lambda x : 1 if ("fog" in x.Event or "fog" in x.Conditions) else 0, axis=1)
    fogtime = datetime.datetime.now()
    print("Foggy completed in:", fogtime - cloudtime)
    data['Snow'] = data.apply(lambda x : 1 if ("snow" in x.Event or "snow" in x.Conditions) else 0, axis=1)
    snowtime = datetime.datetime.now()
    print("Snow completed in:", snowtime - fogtime)
    data['Clear'] = data.apply(lambda x : 1 if ("clear" in x.Event or "clear" in x.Conditions) else 0, axis=1)
    cleartime = datetime.datetime.now()
    print("Clear completed in:", cleartime - snowtime)
    return data

##Step 1 - Connect Weather to Forecast
def finding_weather(data, all_weather, yoa, moa, dayoa):
    print("Finding Weather for Forecast date of:",moa,"/",dayoa,"/",yoa)
    data['time'] = data['Hour'].map(lambda x : datetime.datetime(yoa, moa, dayoa, x, 0, 0).strftime('%s'))
    data['hourbefore'] = data['time'].map(lambda x : int(x) - 60*60)
    data['WeekDay'] = data.apply(lambda x : 1 if (int(datetime.datetime(yoa, moa, dayoa, x.Hour, 0, 0).isoweekday()) in range(1,6)) else 0, axis=1)
    data['WeekEnd'] = data.apply(lambda x : 0 if (int(datetime.datetime(yoa, moa, dayoa, x.Hour, 0, 0).isoweekday()) in range(1,6)) else 1, axis=1)
    data['time'] = data['time'].astype(int)
    data['hourbefore'] = data['hourbefore'].astype(int)
    # Merge the event/conditions columns based on time and grid block
    newdata = pandas.merge(data, all_weather[['Rain','Cloudy', 'Foggy','Snow','Clear','precipIntensity','time','Grid_Block']], on=['time','Grid_Block'])
    # Merge the event/conditions before columns based on hour before and grid block
    newdata = pandas.merge(newdata, all_weather[['RainBefore','hourbefore','Grid_Block']], on=['hourbefore','Grid_Block'])
    print("Weather fetch complete")
    newdata = newdata[['Hour','DayFrame','WeekDay','WeekEnd','Clear','Cloudy','Rain','Foggy','Snow','RainBefore','Grid_Block','Grid_Col',
    'Grid_Row','Highway','Land_Use_Mode','Road_Count','time','precipIntensity']]
    if len(newdata) == 0:
        print("Weather pull failed. Select Different Date")
        exit()
    return newdata

##Step 2 - Standardize Data. 
def standarize_data(data, testnum):
    data = data.drop_duplicates(keep='first')
    print("Scaling data with Test number:", testnum)
    # Drop any empties now, since we don't want empties here!
    # data = data.dropna()

    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()

    # Fit your data on the scaler object
    scaled = scaler.fit_transform(data)
    scaled = pandas.DataFrame(scaled, columns=data.columns)

        # Get the columns of the data needed
    if testnum == 2:
        scaled = scaled.drop(['Hour','WeekEnd','Grid_Block','Clear'],axis=1) #Test 2  
    elif testnum == 3:
        scaled = scaled.drop(['DayFrame','Grid_Block','time'],axis=1) #Test 3  
    elif testnum == 4:
        scaled = scaled.drop(['DayFrame','Hour', 'Grid_Block'],axis=1) #Test 4
    elif testnum == 5:
        scaled = scaled.drop(['Hour','time','Grid_Block'],axis=1) #Test 5
    elif testnum == 6:
        scaled = scaled.drop(['DayFrame','time'],axis=1) #Test 6
    else:
        pass

    # Send it back
    print("Data Scale Complete")
    return scaled, data

##Step 3 - Predict for accidents
##Data is SCALED version of data, filename is title to save predicted forecast under, 
##testnum is the Chosen test number, and modelname is the path to the model. 
def predict_accidents(data, testnum, modelname):
    print("Predicting Accident Hotspots with Test number", testnum, " and model:", modelname)
    
    ########################################################################################################################################################################

    ##This section makes sure that the correct columns are in the data files, just in case.
    data = data.dropna()
    X = data.columns.shape[0]
    ########################################################################################################################################################################
    #Printing the size of the testing data, that is, the data file. 
    print("\tSize of data:", data.shape)

    #Creating the framework for the model. 
    # creating the model
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X.
    model.add(Dense(X,
                    input_dim=X, activation='sigmoid'))
    # Use for standard sized variable set
    model.add(Dense(X-5, activation='sigmoid'))
    # model.add(Dropout(.1))
    model.add(Dense(X-10, activation='sigmoid'))

    model.add(Dense(1, activation='sigmoid'))

    ##Compiling a model, and pulling in the saved weights.
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])

    ##Our current set model. Min max reduced. 
    model.load_weights(modelname)

    ########################################################################################################################################################################
    # Okay, now let's calculate predictions.
    probability = model.predict(data)
    #Save the predicted values to the Probability column. 
    data["Probability"] = probability 

    # Then, let's round to either 0 or 1, since we have only two options (accident or no).
    predictions_round = [abs(round(x[0])) for x in probability]
    data["Prediction"] = predictions_round
 
    #Printing some of the found values, as well as the total number of predicted accidents for this data. 
    print("\tMin probability: ",  round(float(min(probability)*100), 2))
    print("\tMax probability: ",  round(float(max(probability)*100), 2))
    print("\tAccidents predicted: ", sum(data.Prediction))

    return data

##Step 4 - Add results to unscaled version of data
##Add Prediction and Probability to the unscaled version of the data. 
def add_Pred_andProb(data, scaled, folder, suffix):
    print("Adding Probability and Predicted Accidents to data file")
    scaledfile = folder + "MMR/" + suffix + "MMR.csv"
    filename = folder + "Forecast/" + suffix + "Forecast.csv"
    scaled['Prediction'] = scaled['Prediction'].astype(int)
    scaled['Probability'] = scaled['Probability'].astype(float)
    missing = scaled['Probability'].isnull().sum()
    data['Prediction'] = scaled['Prediction'].values
    data['Probability'] = scaled['Probability'].values
    missing = data['Probability'].isnull().sum()
    print("\tLength of Data Probability:", len(data)-missing)
    print("\tSaving forecasted data to: ", filename,scaledfile)
    scaled.to_csv(scaledfile, sep=",", index=False)
    data.to_csv(filename, sep=",", index=False)
    return scaled, data
    
##Step 5 - Find matches, using either the original DayFrames, or the alternate. 
def finding_matches(accidents, data):
    data = data[data['Prediction'] == 1]
    match = 0

    for i, _ in enumerate(accidents.values):
        for j, _ in enumerate(data.values):
            if (accidents.Grid_Block.values[i] == data.Grid_Block.values[j] and accidents.DayFrame.values[i] == data.DayFrame.values[j]):
                match += 1
    print("This many matches were found:", match)

def make_DayFrameAlt(data):
    data["DayFrameAlt"] = ""
    data.Hour = data.Hour.astype(int)
    for i, _ in enumerate(data.values):
        if 6 <= data.Hour.values[i] <= 12:
            data.DayFrameAlt.values[i] = 1
        elif 13 <= data.Hour.values[i] <= 18:
            data.DayFrameAlt.values[i] = 2
        elif 19 <= data.Hour.values[i] <= 23 or 0 <= data.Hour.values[i] <= 5:
            data.DayFrameAlt.values[i] = 3
    return data 

def finding_matches_alt(accidents, data):
    data = make_DayFrameAlt(data)
    accidents = make_DayFrameAlt(accidents)
    data = data[data['Prediction'] == 1]
    altmatch = 0
    for i, _ in enumerate(accidents.values):
        for j, _ in enumerate(data.values):
            if (accidents.Grid_Block.values[i] == data.Grid_Block.values[j] and accidents.DayFrameAlt.values[i] == data.DayFrameAlt.values[j]):
                altmatch += 1
    print("This many ALT matches were found:", altmatch)

def make_directory(model):
    modeltype = (model.split("/")[-1]).split("_")[1]
    if "75-25" in model:
        modelsplit = "75-25 Split" ##75-25
    elif "50-50" in model:
        modelsplit = "50-50 Split" ##50-50 
    else:
        modelsplit = "Test" ##Original

    if "CutGF" in model:
        modeltype= "CutGF"
    elif "FullGF" in model:
        modeltype = "FullGF" 
    elif "CutRan" in model:
        modeltype= "CutRan"
    elif "FullRan" in model:
        modeltype = "FullRan" 
    elif "Spatial" in model:
        modeltype = "Spatial" 
    elif "Temporal" in model:
        modeltype = "Temporal" 
 
    folder = "Excel & CSV Sheets/Forecasts/"+date+"/"
    suffix= modeltype +"_"+modelsplit+"_"
    print("\tSaving Folder:",folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder, suffix
#######################################################################################################################################################
##Which test version to run the model on, date wanted to predict for. 

##Cut GF
# testnum = 3
# model = "Graphs & Images/ResultsFromCutGridFixTesting/New Third Test - MMR/model_CutGF_MMR.h5"
# model = "Graphs & Images/ResultsFromCutGridFixTesting/50-50 Split/model_50-50_CutGF.h5"
# model = "Graphs & Images/ResultsFromCutGridFixTesting/75-25 Split/model_75-25_CutGF.h5"

##Cut Ran
testnum = 1
# model = "Graphs & Images/ResultsFromCutRandomTesting/New First Test/model_CutRan_MMR.h5"
# model = "Graphs & Images/ResultsFromCutRandomTesting/50-50 Split/model_CutRan_50-50.h5"
model = "Graphs & Images/ResultsFromCutRandomTesting/75-25 Split/model_CutRan_75-25.h5"

##Full GF
# testnum = 5
# model = "Graphs & Images/ResultsFromFullGridFixTesting/New Fifth Test - MMR/model_FullGF_MMR.h5"
# model = "Graphs & Images/ResultsFromFullGridFixTesting/50-50 Split/model_50-50_FullGF.h5"
# testnum = 1
# model = "Graphs & Images/ResultsFromFullGridFixTesting/75-25 Split/model_75-25_FullGF.h5"

##Full Ran 
# testnum = 6
# model = "Graphs & Images/ResultsFromFullRandomTesting/Sixth Test/model_FullRandom.h5"
# testnum = 5
# model = "Graphs & Images/ResultsFromFullRandomTesting/50-50 Split/model_FullRandom_50-50 Split.h5"
# model = "Graphs & Images/ResultsFromFullRandomTesting/75-25 Split/model_FullRandom_75-25 Split.h5"

##Spatial
# testnum = 5
# model = "Graphs & Images/ResultsfromSpatialShift/New Fifth Test - MMR/model_Spatial_MMR.h5"
# model = "Graphs & Images/ResultsfromSpatialShift/50-50 Split/model_50-50_Spatial.h5"
# model = "Graphs & Images/ResultsfromSpatialShift/75-25 Split/model_75-25_Spatial.h5"

##Temporals
# testnum = 1
# model = "Graphs & Images/ResultsfromTemporalShift/New First Test - MMR/model_Temporal_MMR.h5"
# model = "Graphs & Images/ResultsfromTemporalShift/50-50 Split/model_50-50_Temporal.h5"
# model = "Graphs & Images/ResultsfromTemporalShift/75-25 Split/model_75-25_Temporal.h5"

accidentfile = "Excel & CSV Sheets/Forecast Accident Dates/4_12_2019_Accidents.csv"

accidents = pandas.read_csv(accidentfile)

year = int(((accidentfile.split("/")[-1]).split("_")[2]).split(".csv")[0])
month = int((accidentfile.split("/")[-1]).split("_")[0])
day = int((accidentfile.split("/")[-1]).split("_")[1])
date = str(year)+"-"+str(month)+"-"+str(day)

##Step 1 - Add weather
data = finding_weather(data, all_weather, year, month, day)

##Step 2 - Standardize Data - returns scaled version 
scaled, data = standarize_data(data, testnum)

##Step 3 - Predict for Accidents on Given Day - returns scaled version of data
#Order of parameters - Scaled, testnumber, modelfilename
scaled = predict_accidents(scaled, testnum, model)

##Step 4 - Add results to unscaled data - saves data to given filename. 
#Order of parameters - data, scaled, folder to save forecast under
folder, suffix = make_directory(model)
scaled, data = add_Pred_andProb(data, scaled, folder, suffix)

##Step 5 - Finding matches:
print("Accidents Occurred: ", len(accidents))
finding_matches(accidents, data)
finding_matches_alt(accidents, data)
end = datetime.datetime.now()
print("Testing completed in:", end-start)