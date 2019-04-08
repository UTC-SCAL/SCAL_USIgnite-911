# import matplotlib
import matplotlib.pyplot as plt
import numpy
import datetime
import time
from darksky import forecast
import pytz
import pandas
import math
import os, sys
from os.path import exists
from selenium import webdriver
import schedule
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


places = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",")

# columns = ['Route','Log_Mile','Date','Hour','Unix','Temperature','Temp_Max','Temp_Min','Dewpoint','Humidity','Month',
# 'Weekday','Visibility','Cloud_Coverage','Precipitation_Intensity','Precip_Intensity_Max','Clear',
# 'Cloudy','Rain','Fog','Snow','RainBefore','Terrain','Land_Use','Access_Control','Operation',
# 'Thru_Lanes','Num_Lanes','Ad_Sys','Gov_Cont','Func_Class','Pavement_Width',	'Pavement_Type']
# hotspots = hotspots[columns]


def forecasting(places, month, day, year):
    start = datetime.datetime.now()
    places.Event = places.Event.astype(str)
    # places.Unix = places.Unix.astype(int)
    places.Conditions = places.Conditions.astype(str)
    places.Precipitation_Type = places.Precipitation_Type.astype(str)
    places.Precipitation_Intensity = places.Precipitation_Intensity.astype(float)
    places.Precip_Intensity_Max = places.Precip_Intensity_Max.astype(float)
    places.Temp_Max = places.Temp_Max.astype(float)
    places.Temp_Min = places.Temp_Min.astype(float)
    places.Precip_Intensity_Time = places.Precip_Intensity_Time.astype(str)
    places.Latitude = places.Latitude.astype(float)
    places.Longitude = places.Longitude.astype(float)
    places.EventBefore = places.EventBefore.astype(str)
    places.ConditionBefore = places.ConditionBefore.astype(str)
    thisdate = str(month)+'/'+str(day)+'/'+str(year)
    dt = datetime.datetime.strptime(thisdate, '%m/%d/%Y')
    print(thisdate, dt.weekday())
    places.Date = thisdate
    places.Weekday = dt.weekday()
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    hoa = 0
    mioa = 0
    soa = 0
    yoa = year
    moa = month
    dayoa = day
    filename = "../Excel & CSV Sheets/ETRIMS/Forecast-for"+str(month)+"-"+str(day)+"-"+str(year)+"_"+str(start.date())+"_"+str(start.hour)+".csv"
    print(filename)
    for d, stuff in enumerate(places.values[0:(len(places.loc[places['Hour'] == 0]))]):
        print(d)
        lat = places.Latitude.values[d]
        long = places.Longitude.values[d]
        t = datetime.datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
        call = key, lat, long

        try:
            forecastcall = forecast(*call, time=t, header={'Accept-Encoding': 'gzip'})
        
            # Hourly data
            for i in range(0,7):
                r = (i*len(places.loc[places['Hour'] == 0]))
                if d != 0:
                    r = (i*len(places.loc[places['Hour'] == 0]))+d
                hour = places.Hour.values[r]
                for k, value in enumerate(forecastcall.hourly):
                # Retrieving weather for previous weather
                    if k == hour:
                        places.Temperature.values[r] = value.temperature
                        places.Dewpoint.values[r] = value.dewPoint
                        places.Event.values[r] = value.icon
                        places.Humidity.values[r] = value.humidity
                        places.Month.values[r] = moa
                        places.Visibility.values[r] = value.visibility
                        places.Conditions.values[r] = value.summary
                        places.ConditionBefore.values[r] = forecastcall.hourly[k-1].summary
                        places.EventBefore.values[r] = forecastcall.hourly[k-1].icon
                # print(places.values[r])
                for j, value2 in enumerate(forecastcall.daily):
                    try:
                        places.Precipitation_Type.values[r] = value2.precipType
                    except:
                        places.Precipitation_Type.values[r] = "NA"
                    try:
                        places.Precipitation_Intensity.values[r] = value2.precipIntensity
                    except:
                        places.Precipitation_Intensity.values[r] = -1000
                    try:
                        places.Precip_Intensity_Max.values[r] = value2.precipIntensityMax
                    except:
                        places.Precip_Intensity_Max.values[r] = -1000
                    try:
                        places.Precip_Intensity_Time.values[r] = value2.precipIntensityMaxTime
                    except:
                        places.Precip_Intensity_Time.values[r] = -1000
                    try:
                        places.Temp_Max.values[r] = value2.temperatureMax
                    except:
                        places.Temp_Max.values[r] = -1000
                    try:
                        places.Temp_Min.values[r] = value2.temperatureMin
                    except:
                        places.Temp_Min.values[r] = -1000
                    try:
                        places.Cloud_Coverage.values[r] = value2.cloudCover
                    except:
                        places.Cloud_Coverage.values[r] = -1000
                    if "clear" in places.Event.values[r] or "clear" in places.Conditions.values[
                        r] \
                            or "Clear" in places.Event.values[r] or "Clear" in \
                            places.Conditions.values[r]:
                        places.Clear.values[r] = 1
                    else:
                        places.Clear.values[r] = 0

                    if "rain" in places.Event.values[r] or "rain" in places.Conditions.values[r] \
                            or "Rain" in places.Event.values[r] or "Rain" in \
                            places.Conditions.values[r] \
                            or "Drizzle" in places.Event.values[r] or "Drizzle" in \
                            places.Conditions.values[r] \
                            or "drizzle" in places.Event.values[r] or "drizzle" in \
                            places.Conditions.values[r]:
                        places.Rain.values[r] = 1
                    else:
                        places.Rain.values[r] = 0

                    if "snow" in places.Event.values[r] or "snow" in places.Conditions.values[i] \
                            or "Snow" in places.Event.values[r] or "Snow" in places.Conditions.values[r]:
                        places.Snow.values[r] = 1
                    else:
                        places.Snow.values[r] = 0

                    if "cloudy" in places.Event.values[r] or "cloudy" in \
                            places.Conditions.values[r] \
                            or "Cloudy" in places.Event.values[r] or "Cloudy" in \
                            places.Conditions.values[r] \
                            or "overcast" in places.Event.values[r] or "overcast" in \
                            places.Conditions.values[r] \
                            or "Overcast" in places.Event.values[r] or "Overcast" in \
                            places.Conditions.values[
                                r]:
                        places.Cloudy.values[r] = 1
                    else:
                        places.Cloudy.values[r] = 0

                    if "fog" in places.Event.values[r] or "foggy" in places.Conditions.values[r] \
                            or "Fog" in places.Event.values[r] or "Foggy" in \
                            places.Conditions.values[r]:
                        places.Fog.values[r] = 1
                    else:
                        places.Fog.values[r] = 0
                    if "rain" in places.EventBefore.values[r] or "rain" in \
                            places.ConditionBefore.values[r] \
                            or "Rain" in places.EventBefore.values[r] or "Rain" in \
                            places.ConditionBefore.values[r]:
                        places.RainBefore.values[r] = 1
                    else:
                        places.RainBefore.values[r] = 0
        except:
            pass
        if d % 400 == 0:
            places.to_csv(filename,sep=",", index=False)
    places.to_csv(filename,sep=",", index=False)
#     testing(places)
# def testing(places):
#     test = places
#     test = shuffle(test)
#     test = shuffle(test)
#     model_maker = pandas.read_csv("../Excel & CSV Sheets/Full Data_MMR.csv",sep=",")
#     columns = model_maker.columns.values[1:len(model_maker.column.values)]
#
#     test = test[columns]
#
#     X_test = test
#
#     print("Size of X_Test:", X_test.shape)
#
#     model = Sequential()
#
#     model.add(Dense(X_test.shape[1],
#                     input_dim=X_test.shape[1], activation='sigmoid'))
#     model.add(Dense(28, activation='sigmoid'))
#     model.add(Dropout(.1))
#     model.add(Dense(20, activation='sigmoid'))
#     model.add(Dense(18, activation='sigmoid'))
#     model.add(Dense(10, activation='sigmoid'))
#     model.add(Dropout(.1))
#     model.add(Dense(1, activation='sigmoid'))
#
#     #           3. Compiling a model.
#     model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
#     model.load_weights("model_MMR.h5")
#     # Okay, now let's calculate predictions.
#     predictions = model.predict(X_test)
#     test["Probability"] = predictions
#     # Then, let's round to either 0 or 1, since we have only two options.
#     predictions_round = [abs(round(x[0])) for x in predictions]
#     test["Prediction"] = predictions_round
#     # print(rounded)
#     print("Head of predicitons: ", predictions[0:10])
#     print("Head of predictions_round: ", predictions_round[0:10])
#
#     test.to_csv(filename, sep=",")

    end = datetime.datetime.now()
    print("Forecasting Complete. Duration:", end - start)
def generate_results(y_test,predictions, hist, fpr, tpr, roc_auc, date):
    font = {'family': 'serif',
            'weight': 'regular',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.yticks((0,.5,1), (0,.5,1))
    plt.xticks((0,.5,1), (0,.5,1))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic curve')
    title = '../Graphs & Images/ResultsFromForecast/roc.png'
    fig.savefig(title, bbox_inches='tight')
    # plt.subplot(212)
    fig = plt.figure()
    plt.xticks(range(0, 20), range(1, 21), rotation=90)
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    plt.axhline(y=0.5, color='gray', linestyle='-')
    plt.scatter(x=x, y=predictions[0:20], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:20], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    title = '../Graphs & Images/ResultsFromForecast/pred'+date+'.png'
    fig.savefig(title, bbox_inches='tight')

    font = {'family': 'serif',
            'weight': 'bold',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    a1 = fig.add_subplot(2,1,1)
    a1.plot(hist.history['acc'])
    a1.plot(hist.history['val_acc'])
    a1.set_ylabel('Accuracy')
    a1.set_xlabel('Epoch')
    a1.set_yticks((.5, .65, .8) )
    a1.set_xticks((0,(len(hist.history['val_acc'])/2),len(hist.history['val_acc'])))
    a1.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right', fontsize='small')
    # plt.show()
    # fig.savefig('acc.png', bbox_inches='tight')
    # summarize history for loss
    # fig = plt.figure()
    a2 = fig.add_subplot(2,1,2)
    # fig = plt.figure()
    a2.plot(hist.history['loss'])
    a2.plot(hist.history['val_loss'])
    a2.set_ylabel('Loss')
    a2.set_xlabel('Epoch')
    a2.set_yticks((.15,.20,.25,))
    a2.set_xticks((0,(len(hist.history['val_loss'])/2),len(hist.history['val_loss'])))
    a2.legend(['Train Loss', 'Test Loss'], loc='upper right', fontsize='small')
    # plt.show()
    title = '../Graphs & Images/ResultsFromForecast/lossandacc'+date+'.png'
    fig.savefig(title, bbox_inches='tight')


def job(t, places):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    thistime = datetime.datetime.now()
    if thistime.hour == 18:
        month = tomorrow.month
        day = tomorrow.day
        year = tomorrow.year
    else: 
        month = thistime.month
        day = thistime.day
        year = thistime.year
    print(t, "Using Date: ",month,"/",day,"/",year)
    forecasting(places,month,day,year)
    return

def waiting(time):
    print("Waiting:",time.strftime("%Y-%m-%d %H:%M"))
    return

print("Beginning code at:" , datetime.datetime.now())

schedule.every().day.at("18:00").do(job, "Fetching weather forecast", hotspots)
schedule.every().day.at("00:00").do(job, "Fetching weather forecast", hotspots)
schedule.every().day.at("06:00").do(job, "Fetching weather forecast", hotspots)
schedule.every().day.at("12:00").do(job, "Fetching weather forecast", hotspots)

while True:
    schedule.run_pending()
    schedule.every(30).minutes.do(waiting, datetime.datetime.now())
    time.sleep(30)

# print(hotspots.columns.values)

# test = pandas.read_csv(
#     "../Excel & CSV Sheets/TestDay.csv", sep=",")
# test = shuffle(test)
# test = shuffle(test)

# X = test.ix[:, 1:(len(test.columns)+1)].values
# y = (test.ix[:, 0].values).reshape((138, 1))
# print("Size of X_Test:", X.shape, "Size of y_test:", y.shape)

# model = Sequential()
# model.add(Dense(30, input_dim=30, activation='sigmoid'))
# model.add(Dense(28, activation='sigmoid'))
# model.add(Dropout(.1))
# model.add(Dense(20, activation='sigmoid'))
# model.add(Dense(18, activation='sigmoid'))
# model.add(Dense(10, activation='sigmoid'))
# model.add(Dropout(.1))
# model.add(Dense(1, activation='sigmoid'))

# #           3. Compiling a model.
# model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
# model.load_weights("")
# # Okay, now let's calculate predictions.
# predictions = model.predict(X_test)
# dataset["Probability"] = predictions
# # Then, let's round to either 0 or 1, since we have only two options.
# predictions_round = [abs(round(x[0])) for x in predictions]
# dataset["Prediction"] = predictions_round
# # print(rounded)
# print("Head of predicitons: ", predictions[0:10])
# print("Head of predictions_round: ", predictions_round)

# dataset.to_csv("../Excel & CSV Sheets/2019-02-25_13_forecast_full2.csv", sep=",")
# matches = 0

#
# print(matches)