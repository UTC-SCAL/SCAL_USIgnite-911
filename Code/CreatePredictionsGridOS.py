
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from math import *
from sklearn import preprocessing
import datetime
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

########################################################################################################################################################################

##Importing all files necessary. 

# #Test is the forecast MMR file created by forecast.py. The time the forecast was pulled is the last section. That is, 2019-04-03_6 would be April 3rd at 6AM.
forecastfiledone = "../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Forecast-for6-10-2019_2019-06-11_11.csv"
test = pandas.read_csv(forecastfiledone, sep=",")
blank = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Forecast Forum OS.csv", sep=",")
gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Vertices OS Layout.csv", sep=",")


#Importing the accidents. The loop is only necessary if we are operating with the raw file from the email.

# accidents = pandas.read_excel("../Excel & CSV Sheets/2019 Data/Final Form Reports/Accident Report_FinalForm.xlsx")

# accidents['Hour'] = 0
# for d, info in enumerate(accidents.values):
#      dateof = datetime.datetime.strptime(accidents.Response_Date.values[d], '%d/%m/%y %H:%M')
#      accidents.Hour.values[d] = dateof.hour


########################################################################################################################################################################

##Converting the lat and longs back to a readable format (Each entry in MMR matches the same index in Standard)
# test['Latitude'] = blank['Latitude']
# test['Longitude'] = blank['Longitude']

##Cutting the data set to only those entries that are reported as positive. 
# test = test[test['Prediction'] == 1]


########################################################################################################################################################################

##Creating a threshold for the predictions. If 75% probability is needed, change to .75. There will be no change to the predictions if the threshold remains at 0.5 . 

# threshhold = 0.50
# test = test[test['Probability'] >= threshhold]


########################################################################################################################################################################

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
    print(fulldata.size)
    fulldata.to_csv(filename, sep=",", index=False)

def standarize_forecast(forecast):
    # Read in the data you want to normalize/standardize/adjust
    # Get the columns of the data
    dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Data 2017+2018 MMR.csv", sep=",")
    dataset = dataset.drop(['Daily_Relative_Temp','Monthly_Relative_Temp', 'Clear', 'Month','Weekday'], axis=1)
    # print(len(dataset.columns.values))
    # exit()
    columns = dataset.columns.values[1:len(dataset.columns.values)]
    X = columns
    forecast = forecast[columns]
 
    # Drop any empties now, since we don't want empties here!
    # df = df.dropna()

    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()

    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(forecast)
    scaled_df = pandas.DataFrame(scaled_df, columns=columns)
    # scaled_df.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Forecast-for6-10-2019_2019-06-11_11_MMR.csv", index=False)
    # # Send it back
    # exit()
    return scaled_df


def add_Pred_andProb(forecast, scaled, forecastfile):
    forecast['Prediction'] = scaled['Prediction']
    forecast['Prediction'] = forecast['Prediction'].astype(int)
    forecast['Probability'] = scaled['Probability']
    forecast['Probability'] = forecast['Probability'].astype(float)
    forecast.to_csv(forecastfile, sep=",", index=False)


def match_predictions_using_grid(forecast, accidents, gridblocks):
    #Start out with no matches, so matches equals zero. 
    matches = 0
    #For each entry in forecast, look at every accident for that day. If the two happened within 3 hours of one another, and 
    # the distance between the two is less than roughly a gridblock, then they are considered a match. 
    for i, info in enumerate(forecast.values):
        for j, data in enumerate(accidents.values):
            forecastTime = forecast.TimeFrame.values[i]
            accTime = accidents.TimeFrame.values[j]
            if forecastTime == accTime:
                # Making the actual polygon using the coordinates above
                lats = []
                longs = []
                for k, value in enumerate(gridblocks):
                    if forecast.GridBlock.values[i] == gridblocks.ORIG_FID.values[k]:
                        lats.append(gridblocks.Y.values[k])
                        longs.append(gridblocks.X.values[k])
                poly_coords = ((lats[0], longs[0]), (lats[1], longs[1]), (lats[2], longs[2]), (lats[3], longs[3]), (lats[4], longs[4]))
                poly = Polygon(poly_coords)

                # take in the 911 incident lat and long one at a time
                call_lat = accidents.Latitude.values[j]
                call_long = accidents.Longitude.values[j]
                call_incident = Point(call_lat, call_long)
                # See if the 911 incident is in the current polygon (gridblock)
                if poly.contains(call_incident):
                    matches +=1
                else:
                    pass
    #Prints the total number of matches found using the haversine method. 
    print("\t Matches found using GridBlocks:", matches)

def match_predictions_using_ghost(forecast, accidents, gridblocks):
  #Start out with no matches, so matches equals zero. 
    matches = 0
    #For each entry in forecast, look at every accident for that day. If the two happened within 3 hours of one another, and 
    # the distance between the two is less than roughly a gridblock, then they are considered a match. 
    for i, info in enumerate(forecast.values):
        for j, data in enumerate(accidents.values):
            forecastTime = forecast.TimeFrame.values[i]
            accTime = accidents.TimeFrame.values[j]
            if forecastTime == accTime:
                # Making the actual polygon using the coordinates above
                lats = []
                longs = []
                for k, value in enumerate(gridblocks):
                    if forecast.GridBlock.values[i] == gridblocks.ORIG_FID.values[k]:
                        lats.append(gridblocks.Ghost_Lat.values[k])
                        longs.append(gridblocks.Ghost_Long.values[k])
                poly_coords = ((lats[0], longs[0]), (lats[1], longs[1]), (lats[2], longs[2]), (lats[3], longs[3]), (lats[4], longs[4]))
                poly = Polygon(poly_coords)

                # take in the 911 incident lat and long one at a time
                call_lat = accidents.Latitude.values[j]
                call_long = accidents.Longitude.values[j]
                call_incident = Point(call_lat, call_long)
                # See if the 911 incident is in the current polygon (gridblock)
                if poly.contains(call_incident):
                    matches +=1
                else:
                    pass
    #Prints the total number of matches found using the haversine method. 
    print("\t Matches found using GhostBlocks:", matches)


def haversine(long1, lat1, long2, lat2):
    # convert decimal degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # the radius of the earth in miles
    return c * r #The distance between the two locations

def predict_accidents(forecast, filename):
    dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Data 2017+2018 MMR.csv", sep=",")
    columns = dataset.columns.values[1:len(dataset.columns.values)]
    X = columns
    print(columns)
    # forecast = forecast[columns]
    ########################################################################################################################################################################

    ##This section makes sure that the correct columns are in the forecast files, just in case.
    # forecast = forecast.dropna()

    ########################################################################################################################################################################
    #Printing the size of the testing data, that is, the forecast file. 
    print("Size of forecast:", forecast.shape)
    #Creating the framework for the model. 
    # creating the model
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X.
    model.add(Dense(X.shape[0],
                    input_dim=X.shape[0], activation='sigmoid'))

    # Use for standard sized variable set
    model.add(Dense(X.shape[0]-5, activation='sigmoid'))
    # model.add(Dropout(.1))
    model.add(Dense(X.shape[0]-10, activation='sigmoid'))
    # model.add(Dense(X.shape[1]-15, activation='sigmoid'))
    # model.add(Dense(X.shape[1]-20, activation='sigmoid'))
    # model.add(Dropout(.1))

    model.add(Dense(1, activation='sigmoid'))

    ##Compiling a model, and pulling in the saved weights.
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
 
    ##The model created using the forecast and test data combined as the test. 
    # model.load_weights("model_forecast.h5")

    ##Our current set model. Min max reduced. 
    model.load_weights("model_gridOS_NoRel_NoClear.h5")

    ##The model created by sorted the entries by time, then training the model. 
    # model.load_weights("model_timesort_MMR.h5")

    ########################################################################################################################################################################
    # Okay, now let's calculate predictions.
    probability = model.predict(forecast)
    #Save the predicted values to the Probability column. 
    forecast["Probability"] = probability 

    # Then, let's round to either 0 or 1, since we have only two options (accident or no).
    predictions_round = [abs(round(x[0])) for x in probability]
    forecast["Prediction"] = predictions_round
 
    #Printing the found values, as well as the total number of predicted accidents for this forecast. 
    print("Head of probabilities: ",  probability[0:10])
    print("Head of predictions_round: ", predictions_round[0:10])
    print("Accidents predicted: ", sum(predictions_round))

    forecast.to_csv(filename,
                    sep=",",index=False)
    return forecast

    ########################################################################################################################################################################

#The print statements just make things easier to understand. 
#
#Print the number of accidents and the current threshold. 
# print("Accidents: ", len(accidents.Latitude.values))
# print("Threshhold: ", threshhold)
thistime = str(datetime.datetime.now().date())
thishour = str(datetime.datetime.now().hour)
fileending = thistime,thishour

filename = forecastfiledone.split(".csv",1)[0]+"_MMR.csv" 
##Finding the matches from standard data using haversine. First prints the number of accidents predicted. Note: The using_route function does not currently work, but is ready for future use.
print(test.columns)
print("Grid Layout: \t\t", len(test.Latitude.values))
scaled = standarize_forecast(test)
scaled = predict_accidents(scaled, filename)
add_Pred_andProb(test, scaled, forecastfiledone)
# match_predictions_using_have(forecastStand, accidents)
# match_predictions_using_route(test, accidents)

