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


hotspots = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",")

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
                date = datetime.datetime(yoa, moa, dayoa, int(places.Hour.values[r]), mioa, soa)
                unixtime = date.strftime('%s')
                places.Unix.values[r] = unixtime
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

    test = places
    test = shuffle(test)
    test = shuffle(test)

    columns =['Latitude','Longitude','Log_Mile','Hour','Temperature','Temp_Max','Temp_Min','Dewpoint','Humidity',
        'Month','Weekday','Visibility','Cloud_Coverage','Precipitation_Intensity','Precip_Intensity_Max',
            'Clear',	'Cloudy',	'Rain',	'Fog',	'Snow',	'RainBefore',	'Terrain',	'Land_Use',
                'Access_Control',	'Operation',	'Thru_Lanes',	'Num_Lanes',	'Ad_Sys',
                    'Gov_Cont',	'Func_Class',	'Pavement_Width',	'Pavement_Type']


    test = test[columns]

    X_test = test

    print("Size of X_Test:", X_test.shape)

    model = Sequential()
    model.add(Dense(32, input_dim=32, activation='sigmoid'))
    model.add(Dense(28, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(20, activation='sigmoid'))
    model.add(Dense(18, activation='sigmoid'))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(1, activation='sigmoid'))

    #           3. Compiling a model.
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
    model.load_weights("modelreduced.h5")
    # Okay, now let's calculate predictions.
    predictions = model.predict(X_test)
    test["Probability"] = predictions
    # Then, let's round to either 0 or 1, since we have only two options.
    predictions_round = [abs(round(x[0])) for x in predictions]
    test["Prediction"] = predictions_round
    # print(rounded)
    print("Head of predicitons: ", predictions[0:10])
    print("Head of predictions_round: ", predictions_round[0:10])

    test.to_csv(filename, sep=",")

    end = datetime.datetime.now()
    print("Forecasting Complete. Duration:", end-start)


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


def get_etrims(dataset):
    print("Getting Accident Road Geometrics")
    driver = webdriver.Firefox(executable_path=r"/home/admin/PycharmProjects/911Project/geckodriver")
    driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

    usr = driver.find_element_by_id("UserName")
    pw = driver.find_element_by_id("Password")

    usr.send_keys("JJVPG56")
    pw.send_keys("Saturn71")  # updated 2/26/2019
    driver.find_element_by_class_name("btn").click()

    dataset.Route = dataset.Route.astype(str)

    for i, info in enumerate(dataset.values):
        latitude = dataset.Latitude.values[i]
        longitude = dataset.Longitude.values[i]

        site = "https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/lrsforlatlong?latitude=" \
               + str(latitude) + "&longitude=" + str(longitude) + "&d=1538146112919"

        driver.get(site)
        raw = str(driver.page_source)
        milepoint = float(raw[raw.index("<MilePoint>") + len("<MilePoint>"): raw.index("</MilePoint>")])
        # routeid = raw[raw.index("<RouteId>") + len("<RouteId>"): raw.index("</RouteId>")]

        # dataset.Route.values[i] = routeid
        dataset.Log_Mile.values[i] = milepoint

    geometrics = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_New.csv",
        sep=",")
    segments = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv",
        sep=",")
    descriptions = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON RAW.csv",
        sep=",")
    traffic = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",
        sep=",")
    for k, info in enumerate(dataset.values):
        for i, value in enumerate(geometrics.values):
            if dataset.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > dataset.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    dataset.Num_Lanes.values[k] = geometrics.Num_Lns.values[i]
                    dataset.Thru_Lanes.values[k] = geometrics.Thru_Lanes.values[i]
        for l, value in enumerate(segments.values):
            if dataset.Route.values[k] == segments.ID_NUMBER.values[l]:
                if segments.ELM.values[l] > dataset.Log_Mile.values[k] > segments.BLM.values[l]:
                    dataset.Ad_Sys.values[k] = segments.Ad_Sys.values[l]
                    dataset.Gov_Cont.values[k] = segments.Gov_Cont.values[l]
                    dataset.Func_Class.values[k] = segments.Func_Class.values[l]
        for m, value in enumerate(traffic.values):
            if dataset.Route.values[k] == traffic.ID_NUMBER.values[m]:
                if traffic.ELM.values[m] > dataset.Log_Mile.values[k] > traffic.BLM.values[m]:
                    dataset.AADT.values[k] = traffic.AADT.values[m]
                    dataset.DHV.values[k] = traffic.DHV.values[m]
        for n, value in enumerate(descriptions.values):
            if dataset.Route.values[k] == descriptions.ID_NUMBER.values[n]:
                if descriptions.ELM.values[n] > dataset.Log_Mile.values[k] > descriptions.BLM.values[n]:
                    if descriptions.Feature_Type[n] == 19:
                        dataset.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
                        dataset.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
        for i, value in enumerate(geometrics.values):
            if dataset.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > dataset.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    dataset.Terrain.values[k] = geometrics.Terrain.values[i]
                    dataset.Land_Use.values[k] = geometrics.Land_Use.values[i]
                    dataset.Access_Control.values[k] = geometrics.Acc_Ctrl.values[i]
                    dataset.Illumination.values[k] = geometrics.Illum.values[i]
                    dataset.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
                    dataset.Operation.values[k] = geometrics.Operation.values[i]
    print("Getting weather stuff")
    for i, value in enumerate(dataset.values):
        if "clear" in dataset.Event.values[i] or "clear" in dataset.Conditions.values[
            i] \
                or "Clear" in dataset.Event.values[i] or "Clear" in \
                dataset.Conditions.values[i]:
            dataset.Clear.values[i] = 1
        else:
            dataset.Clear.values[i] = 0

        if "rain" in dataset.Event.values[i] or "rain" in dataset.Conditions.values[i] \
                or "Rain" in dataset.Event.values[i] or "Rain" in \
                dataset.Conditions.values[i] \
                or "Drizzle" in dataset.Event.values[i] or "Drizzle" in \
                dataset.Conditions.values[i] \
                or "drizzle" in dataset.Event.values[i] or "drizzle" in \
                dataset.Conditions.values[i]:
            dataset.Rain.values[i] = 1
        else:
            dataset.Rain.values[i] = 0

        if "snow" in dataset.Event.values[i] or "snow" in dataset.Conditions.values[i] \
                or "Snow" in dataset.Event.values[i] or "Snow" in \
                dataset.Conditions.values[i]:
            dataset.Snow.values[i] = 1
        else:
            dataset.Snow.values[i] = 0

        if "cloudy" in dataset.Event.values[i] or "cloudy" in \
                dataset.Conditions.values[i] \
                or "Cloudy" in dataset.Event.values[i] or "Cloudy" in \
                dataset.Conditions.values[i] \
                or "overcast" in dataset.Event.values[i] or "overcast" in \
                dataset.Conditions.values[i] \
                or "Overcast" in dataset.Event.values[i] or "Overcast" in \
                dataset.Conditions.values[
                    i]:
            dataset.Cloudy.values[i] = 1
        else:
            dataset.Cloudy.values[i] = 0

        if "fog" in dataset.Event.values[i] or "foggy" in dataset.Conditions.values[i] \
                or "Fog" in dataset.Event.values[i] or "Foggy" in \
                dataset.Conditions.values[i]:
            dataset.Fog.values[i] = 1
        else:
            dataset.Fog.values[i] = 0
        if "rain" in dataset.EventBefore.values[i] or "rain" in \
                dataset.ConditionBefore.values[i] \
                or "Rain" in dataset.EventBefore.values[i] or "Rain" in \
                dataset.ConditionBefore.values[i]:
            dataset.RainBefore.values[i] = 1
        else:
            dataset.RainBefore.values[i] = 0
    return dataset


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
# model.load_weights("model.h5")
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

# for i, info in enumerate(forecast.values):
#     for j, data in enumerate(monday.values):
#         forecastHour = forecast.Hour.values[i]
#         mondayHour = monday.Hour.values[j]
#         hourDiff = abs(forecastHour - mondayHour)
#         if hourDiff < 3:
#             lat1 = forecast.Latitude.values[i]
#             long1 = forecast.Longitude.values[i]
#
#             lat2 = monday.Latitude.values[j]
#             long2 = monday.Longitude.values[j]
#             latChange = math.fabs(lat1 - lat2)
#             longChange = math.fabs(long1 - long2)
#             if latChange < 0.01 and longChange < 0.01:
#                 matches +=1
#
# print(matches)