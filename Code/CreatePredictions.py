
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from math import *
import datetime

filename = "../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-03_12_minmax_withpred.csv"
forecastMMR = pandas.read_csv(filename,sep=",")

filename = "../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-03_12_noMM.csv"
forecastStand = pandas.read_csv(filename,sep=",")

forecastMMR['Latitude'] = forecastStand['Latitude']
forecastMMR['Longitude'] = forecastStand['Longitude']

forecastMMR = forecastMMR[forecastMMR['Prediction'] == 1]
forecastStand = forecastStand[forecastStand['Prediction'] == 1]

threshhold = 0.95

forecastMMR = forecastMMR[forecastMMR['Probability'] >= threshhold]
forecastStand = forecastStand[forecastStand['Probability'] >= threshhold]


accidents = pandas.read_csv("/Users/pete/Downloads/Accident Report.csv", sep=",")
accidents['Hour'] = 0
for d, info in enumerate(accidents.values):
     dateof = datetime.datetime.strptime(accidents.Response_Date.values[d], '%d/%m/%y %H:%M')
     accidents.Hour.values[d] = dateof.hour


def match_predictions(forecast, accidents):
    matches = 0
    for i, info in enumerate(forecast.values):
        for j, data in enumerate(accidents.values):
            forecastHour = forecast.Hour.values[i]
            accHour = accidents.Hour.values[j]
            hourDiff = abs(forecastHour - accHour)
            if hourDiff < 2:
                lat1 = forecast.Latitude.values[i]
                long1 = forecast.Longitude.values[i]
                lat2 = accidents.Latitude.values[j]
                long2 = accidents.Longitude.values[j]
                distance = haversine(long1, lat1, long2, lat2)
                if distance < 0.15:
                    matches +=1
    print("\t Matches found:", matches)

def haversine(long1, lat1, long2, lat2):
    # convert decimal degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # the radius of the earth in miles
    return c * r

def predict_accidents(test):

    dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data_MMR.csv", sep=",")
    columns = dataset.columns.values[1:len(dataset.columns.values)]
    test = test[columns]
    test = test.dropna()

    X_test = test

    print("Size of X_Test:", X_test.shape)

    model = Sequential()
    model.add(Dense(X_test.shape[1], input_dim=X_test.shape[1], activation='sigmoid'))
    model.add(Dense(25, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(20, activation='sigmoid'))
    model.add(Dense(18, activation='sigmoid'))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(1, activation='sigmoid'))

    #           3. Compiling a model.
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
    model.load_weights("model_MMR.h5")
    # Okay, now let's calculate predictions.
    predictions = model.predict(X_test)
    test["Probability"] = predictions
    # Then, let's round to either 0 or 1, since we have only two options.
    predictions_round = [abs(round(x[0])) for x in predictions]
    test["Prediction"] = predictions_round
    # print(rounded)
    print("Head of predicitons: ", predictions[0:10])
    print("Head of predictions_round: ", predictions_round[0:10])
    print("Accidents predicted: ", sum(predictions_round))

    test.to_csv("../", sep=",",index=False)


# lat1= 35.044795
# long1 = -85.305500
# lat2 = 35.046121
# long2 =  -85.304835
# lat3 = 35.044294
# long3 = -85.304191
# lat4 = 35.045603
# long4 =  -85.303515

# distance = haversine(lat1, long1, lat2, long2)
# print("From loc1 to loc2:",distance)
# distance2 = haversine(lat1, long1, lat3, long3)
# print("From loc1 to loc3:",distance2)
# distance3 = haversine(lat1, long1, lat4, long4)
# print("From loc1 to loc4:",distance3)
print("Accidents: ", len(accidents.Latitude.values))
print("Threshhold: ", threshhold)
print("MMR: \n\t", len(forecastMMR.Latitude.values))
match_predictions(forecastMMR, accidents)
print("Standard: \n\t", len(forecastStand.Latitude.values))
match_predictions(forecastStand, accidents)