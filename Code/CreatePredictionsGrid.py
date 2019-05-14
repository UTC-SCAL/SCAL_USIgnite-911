
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from math import *
from sklearn import preprocessing
import datetime

########################################################################################################################################################################

##Importing all files necessary. 

#Test is the forecast MMR file created by forecast.py. The time the forecast was pulled is the last section. That is, 2019-04-03_6 would be April 3rd at 6AM.
forecastfile = "../Excel & CSV Sheets/Grid Layout Test Files/Forecast-for5-14-2019_2019-05-14_12.csv"
test = pandas.read_csv(forecastfile, sep=",")
blank = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Blank Forecast Forum.csv", sep=",")


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

def standarize_forecast(forecast):
    # Read in the data you want to normalize/standardize/adjust
    # Get the columns of the data
    dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Full Data Grid MMR.csv", sep=",")
    columns = dataset.columns.values[1:len(dataset.columns.values)]
    X = columns
    forecast = dataset[columns]

    # Drop any empties now, since we don't want empties here!
    # df = df.dropna()

    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()

    # Fit your data on the scaler object
    scaled_df = scaler.fit_transform(forecast)
    scaled_df = pandas.DataFrame(scaled_df, columns=columns)

    # Send it back
    return scaled_df


def add_Pred_andProb(forecast, scaled, forecastfile):
    forecast['Prediction'] = scaled['Prediction']
    forecast['Prediction'] = forecast['Prediction'].astype(int)
    forecast['Probability'] = scaled['Probability']
    forecast['Probability'] = forecast['Probability'].astype(float)
    forecast.to_csv(forecastfile, sep=",", index=False)


#Note: This function is not currently usable, as the Log_Mile and Route are not included in the forecast miles once they are adjusted for the model. 
def match_predictions_using_route(forecast, accidents):
    matches = 0
    for i, info in enumerate(forecast.values):
        for j, data in enumerate(accidents.values):
            forecastHour = forecast.Hour.values[i]
            accHour = accidents.Hour.values[j]
            hourDiff = abs(forecastHour - accHour)
            forecastlog = forecast.Log_Mile.values[i] 
            acclog= accidents.Log_Mile.values[j]
            ##If the forecast entry and the accident are along the same route, happened within 2 hours of one another, and the distance is less than .25, consider
            #the two a match. 
            if (forecast.Route.values[i] == accidents.Route.values[j]) and (hourDiff < 2) and ((abs(forecastlog-acclog)) < .25):
                matches +=1
    #Total number of matches between forecast and accident. 
    print("\t Matches found using Route:", matches)

def match_predictions_using_have(forecast, accidents):
    #Start out with no matches, so matches equals zero. 
    matches = 0
    #For each entry in forecast, look at every accident for that day. If the two happened within 3 hours of one another, and 
    # the distance between the two is less than roughly a block, then they are considered a match. 
    for i, info in enumerate(forecast.values):
        for j, data in enumerate(accidents.values):
            forecastHour = forecast.Hour.values[i]
            accHour = accidents.Hour.values[j]
            hourDiff = abs(forecastHour - accHour)
            if hourDiff < 3:
                lat1 = forecast.Latitude.values[i]
                long1 = forecast.Longitude.values[i]
                lat2 = accidents.Latitude.values[j]
                long2 = accidents.Longitude.values[j]
                distance = haversine(long1, lat1, long2, lat2)
                if distance < 0.15:
                    matches +=1
    #Prints the total number of matches found using the haversine method. 
    print("\t Matches found using Haversine:", matches)

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

def predict_accidents(forecast):
    dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Full Data Grid MMR.csv", sep=",")
    columns = dataset.columns.values[1:len(dataset.columns.values)]
    X = columns
    ########################################################################################################################################################################

    ##This section makes sure that the correct columns are in the forecast files, just in case.
    forecast = forecast.dropna()

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
    model.load_weights("model_grid.h5")

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

    forecast.to_csv("../Excel & CSV Sheets/Grid Layout Test Files/Forecast-for5-14-2019_2019-05-14_12_grid.csv",
                    sep=",",index=False)
    return forecast

    ########################################################################################################################################################################

#The print statements just make things easier to understand. 
#
#Print the number of accidents and the current threshold. 
# print("Accidents: ", len(accidents.Latitude.values))
# print("Threshhold: ", threshhold)

##Finding the matches from standard data using haversine. First prints the number of accidents predicted. Note: The using_route function does not currently work, but is ready for future use.
print(test.columns)
print("Grid Layout: \t\t", len(test.Latitude.values))
scaled = standarize_forecast(test)
scaled = predict_accidents(scaled)
add_Pred_andProb(test, scaled, forecastfile)
# match_predictions_using_have(forecastStand, accidents)
# match_predictions_using_route(test, accidents)

