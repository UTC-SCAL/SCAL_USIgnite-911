# # Use the plaidml backend dynamically if AMD GPU is in use

# try:
#     import tensorflow as tf
#     from tensorflow.python.client import device_lib
#     LST = [x.device_type for x in device_lib.list_local_devices()]
#     if not 'GPU' in LST:
#         import os
#         os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
# except ImportError:
#     import os
#     os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"


# from keras.models import Sequential
# from keras.layers import Dense
# from keras.models import model_from_yaml
# import numpy
# import os
# # Import matplotlib pyplot safely
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy
import pandas
# import talos
# from keras.callbacks import EarlyStopping
# from keras.layers import Dense, Dropout
# from keras.models import Sequential
# from sklearn.metrics import accuracy_score, auc, roc_curve
# from sklearn.model_selection import train_test_split
# from sklearn.utils import shuffle

# try:
#     import matplotlib.pyplot as plt
# except ImportError:
#     import matplotlib
#     matplotlib.use("GtkAgg")
#     import matplotlib.pyplot as plt

# from ann_visualizer.visualize import ann_viz
# from keras_sequential_ascii import keras2ascii
# from keras.models import model_from_json


# test = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_GPS.csv", sep=",")
# columns = ['Route','LogMile', 'Latitude', 'Longitude', 'Thru_Lanes', 'ROW ', 'Num_Lns',
#  'Spd_Limit', 'Terrain', 'Land_Use', 'Illum', 'Operation', 'Acc_Ctrl','Sch Spd Limit' ,'Truck Spd Limit' ]
# print(test.columns.values)
# places = pandas.DataFrame(columns=columns)
# for i, info in enumerate(test.values):
#     print(i)
#     myindex = places.shape[0]+1 
#     print(myindex)
#     print(test.values[i])
#     # print(test.ID_NUMBER.values[i], test.ELM.values[i],test.ELM_Lat.values[i],test.ELM_Long.values[i] )
#     place = test.loc[i, ['ID_NUMBER','BLM', 'BLM_Lat','BLM_Long', 'Thru_Lanes', 'ROW ', 'Num_Lns',
#     'Spd_Limit', 'Terrain', 'Land_Use', 'Illum', 'Operation', 'Acc_Ctrl','Sch Spd Limit' ,'Truck Spd Limit']]
#     place = place.tolist()
#     # place = [test.ID_NUMBER.values[i], test.BLM.values[i],test.BLM_Lat.values[i],test.BLM_Long.values[i]]
#     places.at[myindex] = place
#     # places.at[myindex,'Route'] = test.ID_NUMBER.values[i]
#     # places.at[myindex,'LogMile'] = test.BLM.values[i]
#     # places.at[myindex,'Latitude'] = test.BLM_Lat.values[i]
#     # places.at[myindex,'Longitude'] = test.BLM_Long.values[i]
#     myindex = places.shape[0]+1 
#     # place1 = [test.ID_NUMBER.values[i], test.ELM.values[i],test.ELM_Lat.values[i],test.ELM_Long.values[i]]
#     place1 = test.loc[i, ['ID_NUMBER','ELM', 'ELM_Lat','ELM_Long', 'Thru_Lanes', 'ROW ', 'Num_Lns',
#     'Spd_Limit', 'Terrain', 'Land_Use', 'Illum', 'Operation', 'Acc_Ctrl','Sch Spd Limit' ,'Truck Spd Limit']]
#     place1 = place1.tolist()
#     places.at[myindex] = place1
#     print(myindex)
#     # places.at[myindex,'LogMile'] = test.ELM.values[i]
#     # places.at[myindex,'Latitude'] = test.ELM_Lat.values[i]
#     # places.at[myindex,'Longitude'] = test.ELM_Long.values[i]
#     places.to_csv("../Excel & CSV Sheets/ETRIMS/GPS_Locations.csv",sep=',')
# exit()
from datetime import datetime
from darksky import forecast

# places = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",")
# print(len(places))
# places = places[places['Latitude'].notnull()]
# print(len(places))
#
# places.Event = places.Event.astype(str)
# places.Conditions = places.Conditions.astype(str)
# places.Precipitation_Type = places.Precipitation_Type.astype(str)
# places.Precipitation_Intensity = places.Precipitation_Intensity.astype(float)
# places.Precip_Intensity_Max = places.Precip_Intensity_Max.astype(float)
# places.Temp_Max = places.Temp_Max.astype(float)
# places.Temp_Min = places.Temp_Min.astype(float)
# places.Precip_Intensity_Time = places.Precip_Intensity_Time.astype(str)
# places.Latitude = places.Latitude.astype(float)
# places.Longitude = places.Longitude.astype(float)
# places.EventBefore = places.EventBefore.astype(str)
# places.ConditionBefore = places.ConditionBefore.astype(str)
#
# month = 3
# day = 16
# year = 2019
def forecasting(places, month, day, year):
    thisdate = str(month)+'/'+str(day)+'/'+str(year)
    dt = datetime.strptime(thisdate, '%m/%d/%Y')
    print(thisdate, dt.weekday())
    places.Date = thisdate
    places.Weekday = dt.weekday()
    print(places.Date.values[0:5])
    print(places.Weekday.values[0:5])
    exit()
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    hoa = 0
    mioa = 0
    soa = 0
    yoa = year
    moa = month
    dayoa = day
    start = datetime.now()
    filename = "../Excel & CSV Sheets/ETRIMS/Forecast-for"+str(month)+"-"+str(day)+"-"+str(year)+"_"+str(start.date())+"_"+str(start.hour)+".csv"
    print(filename)
    for d, stuff in enumerate(places.values[0:(len(places.loc[places['Hour'] == 0]))]):
        print(d)
        lat = places.Latitude.values[d]
        long = places.Longitude.values[d]
        t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
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
        if d % 200 == 0:
            places.to_csv(filename,sep=",", index=False)
    places.to_csv(filename,sep=",", index=False)
    end = datetime.now()
    print("Duration:", end-start)

    
# segments = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv",sep=',')

# print(places.shape)
# places = places.drop_duplicates(subset ="Latitude")
# print(places.shape)
# places.to_csv("../Excel & CSV Sheets/ETRIMS/GPS_Locations.csv",sep=',')
# exit()


##Adds the segment data to the places file 

# for k,info in enumerate(places.values):
#     print(k)
#     for l, value in enumerate(segments.values):
#         if places.Route.values[k] == segments.ID_NUMBER.values[l]:
#             if segments.ELM.values[l] >= places.Log_Mile.values[k] >= segments.BLM.values[l]:
#                 places.Ad_Sys.values[k] = segments.Ad_Sys.values[l]
#                 places.Gov_Cont.values[k] = segments.Gov_Cont.values[l]
#                 places.Func_Class.values[k] = segments.Func_Class.values[l]
#                 break
#     places.to_csv("../Excel & CSV Sheets/ETRIMS/GPS_Locations2.csv",sep=',')
# exit()



##Gets the forecast data for every 4 hours. 

# fulldata = places.copy()
# for i in range(0,25,4):
#     name = ('places'+str(i))
#     print(name)
#     places.Hour= i
#     print(places.Hour[0:5])
#     fulldata = fulldata.append(places)
# fulldata = fulldata.drop_duplicates()
# print(fulldata.size)
# fulldata.to_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",", index=False)
# exit()
# places = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",")
# descriptions = pandas.read_csv(
#         "../Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON RAW.csv",
#         sep=",")

# for k,info in enumerate(places.values):
#     print(k)
#     if places.Hour.values[k] == 0:
#         for n, value in enumerate(descriptions.values):
#             if ((places.Route.values[k] == descriptions.ID_NUMBER.values[n]) and (descriptions.ELM.values[n] >= places.Log_Mile.values[k] >= descriptions.BLM.values[n]) 
#             and descriptions.Feature_Type[n] == 19):
#                 places.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
#                 places.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
#                 break
#     places.to_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4withPave.csv", sep=",", index=False)
# test = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_GPS.csv", sep=",")

# def generate_results(y_test, y_score):
#     fpr, tpr, _ = roc_curve(y_test, y_score)
#     roc_auc = auc(fpr, tpr)
#     font = {'family': 'serif',
#             'weight': 'bold',
#             'size': 16}

#     plt.rc('font', **font)
#     fig = plt.figure()
#     # plt.subplot(211)
#     plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
#     plt.plot([0, 1], [0, 1], 'k--')
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     # plt.title('Receiver operating characteristic curve')
#     print('AUC: %f' % roc_auc)
#     fig.savefig('roctest.png', bbox_inches='tight')
#     # plt.subplot(212)
#     print("This point reached. ")
#     fig = plt.figure()

#     plt.xticks(range(0, 20), range(1, 21))
#     plt.yticks(range(0, 2), ['No', 'Yes', ''])
#     plt.ylabel('Accident')
#     plt.xlabel('Record')
#     plt.grid(which='major', axis='x')
#     x= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
 
#     plt.scatter(x=x, y=predictions_round[0:20], s=100, c='blue', marker='x', linewidth=2)
#     plt.scatter(x=x, y=y_test[0:20], s=110,
#                 facecolors='none', edgecolors='r', linewidths=2)
#     fig.savefig('predtest.png', bbox_inches='tight')

#     print("Second point reached. ")
    # fig = plt.figure()
    # # plt.subplot(211)
    # plt.plot(hist.history['acc'])
    # plt.plot(hist.history['val_acc'])
    # plt.ylabel('Accuracy')
    # plt.xlabel('Epoch')
    # plt.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right')
    # # plt.show()
    # fig.savefig('acc.png', bbox_inches='tight')
    # print("Third point reached. ")
    # # summarize history for loss
    # # plt.subplot(212)
    # fig = plt.figure()
    # plt.plot(hist.history['loss'])
    # plt.plot(hist.history['val_loss'])
    # plt.ylabel('Loss')
    # plt.xlabel('Epoch')
    # plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    # # plt.show()
    # fig.savefig('loss.png', bbox_inches='tight')
    # print("End reached. ")

## The steps of creating a neural network or deep learning model ##
    # 1. Load Data
    # 2. Defining a neural network
    # 3. Compile a Keras model using an efficient numerical backend
    # 4. Train a model on some data.
    # 5. Evaluate that model on some data!


#           1. Load Data

# test = pandas.read_csv(
#     "../Excel & CSV Sheets/TestDay.csv", sep=",")
# test = shuffle(test)
# test = shuffle(test)

# X = test.ix[:, 1:(len(test.columns)+1)].values
# y = (test.ix[:, 0].values).reshape((138, 1))
# print("Size of X_Test:", X.shape, "Size of y_test:", y.shape)

# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
 
# # evaluate loaded model on test data
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, y, batch_size=500, verbose=1)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

# predictions = loaded_model.predict(X)
# print(y[0:5])
# print(predictions[0:5])

# # Then, let's round to either 0 or 1, since we have only two options.
# predictions_round = [abs(round(x[0])) for x in predictions]
# # print(rounded)
# accscore1 = accuracy_score(y, predictions_round)
# print("Rounded Test Accuracy:", accscore1*100)

# generate_results(y, predictions)

##This section is PCA stuff from Alnour. 


# import pandas as pd
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt
# import numpy as np
# data = pd.read_csv("../Excel & CSV Sheets/Full Data for Model.csv")
# # data = pd.read_csv("../Excel & CSV Sheets/Full Data.csv")
# pca = PCA(n_components=2)
# Y = data['Accident']
# X = data.drop('Accident', axis=1)
# X = X.values
# pca.fit(X)
# print(pca.explained_variance_ratio_)
# reduced_dimentions = pca.transform(X)
# reduced_dimentions = np.array(reduced_dimentions)
# X_true_accidents = reduced_dimentions[Y==1]
# X_non_accidents = reduced_dimentions[Y==0]
# X_true_accidents = X_true_accidents.reshape((X_true_accidents.shape[1], X_true_accidents.shape[0]))
# X_non_accidents = X_non_accidents.reshape((X_non_accidents.shape[1], X_non_accidents.shape[0]))
# # X_true_accidents = X_true_accidents.reshape((X_true_accidents.shape[1], X_true_accidents.shape[0]))
# print(X_true_accidents)
# fig = plt.figure()
# plt.subplot(211)
# plt.scatter(X_true_accidents[0], X_true_accidents[1])
# plt.subplot(212)
# plt.scatter(X_non_accidents[0], X_non_accidents[1])
# plt.show()




##This section is test commands for the time scheduler. 

# import schedule
# import time

# def job():
#     print("I'm working...")

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().minute.at(":15").do(job)
# schedule.every().monday.at("14:32").do(exit())

# while True:
#     schedule.run_pending()
#     time.sleep(1)



## This section creates the unix time column for the files. 

# from datetime import datetime
# import pandas

# data = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHour.csv", sep=",")

# for i,value in enumerate(data.values):
#     hoa = data.Hour.values[i]
#     mioa = 0
#     soa = 0
#     doa = data.Date.values[i]
#     # print(doa.split('/')[0], doa.split('/')[1], int(doa.split('/')[2])+2000)
#     yoa = int(doa.split('/')[2])+2000
#     moa = int(doa.split('/')[0])
#     dayoa = int(doa.split('/')[1])
#     date = datetime(yoa, moa, dayoa, hoa, mioa, soa)
#     unixtime = date.strftime('%s')
#     data.Unix.values[i] = unixtime
#     print(i, data.Unix.values[i])
# #     # print(unixtime)
# data.to_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourandUnix.csv", sep=",", index=False)



##This section finds the min and max of the route's log miles. 

routes = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/FullGPSforNSLoc.csv", sep=",")
roads = routes.Route.unique()
# print(len(roads))

df = pandas.DataFrame( columns=['BLM', 'ELM', 'Route'])

df.Route = roads

for i, info in enumerate(df.values):
    list = []
    print(i)
    for j, stuff in enumerate(routes.values):
        # min = routes.BLM.values[j]
        if routes.Route.values[j] == df.Route.values[i]:

            list.append(routes.Log_Mile.values[j])
            mini = min(list)
            df.BLM.values[i] = mini
            maxi = max(list)
            df.ELM.values[i] = maxi
            # print(mini,maxi)

df.to_csv('../Excel & CSV Sheets/ETRIMS/UniqueRoutes2.csv', sep=",")





##This section makes the data in a nice standardized format by minimum and maximum. 

# from sklearn import preprocessing
# import pandas
# # Get column names first
# df = pandas.read_csv("../Excel & CSV Sheets/Full Data for Model LatLong Unix.csv", sep=",")
# names = df.columns
# # Create the Scaler object
# scaler = preprocessing.MinMaxScaler()
# # Fit your data on the scaler object
# scaled_df = scaler.fit_transform(df)
# scaled_df = pandas.DataFrame(scaled_df, columns=names)
# scaled_df.to_csv("../Excel & CSV Sheets/Full Data Standardized MinMax.csv", sep=",", index=False)



#This section adds the etrims GPS location to the file based off of route and logmile. 


# from selenium import webdriver

# segments = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/SegmentEmpties.csv", sep=",")

# driver = webdriver.Chrome("/Users/pete/Documents/GitHub/SCAL_USIgnite-911/Code/chromedriver")

# driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

# usr = driver.find_element_by_id("UserName")
# pw = driver.find_element_by_id("Password")

# usr.send_keys("JJVPG56")
# pw.send_keys("Saturn71")  # updated 2/26/2019
# driver.find_element_by_class_name("btn").click()

# for i, info in enumerate(segments.values):
#     routeID = segments.ID_NUMBER.values[i]
#     logmile = segments.BLM.values[i]
#     siteRoute = 'https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/latlongforlrs?idnumber=' \
#                 + str(routeID) + '&logmile=' + str(logmile) + '&subroute='
#     if segments.BLM_Lat.values[i] == 0:
#         try:
#             driver.get(siteRoute)
#             raw = str(driver.page_source)
#             X = float(raw[raw.index("<X>") + len("<X>"): raw.index("</X>")])
#             Y = raw[raw.index("<Y>") + len("<Y>"): raw.index("</Y>")]
#             segments.BLM_Lat.values[i] = Y
#             segments.BLM_Long.values[i] = X
#         except: 
#             pass
#     logmile = segments.ELM.values[i]
#     siteRoute = 'https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/latlongforlrs?idnumber=' \
#                 + str(routeID) + '&logmile=' + str(logmile) + '&subroute='
#     if segments.ELM_Lat.values[i] == 0:
#         try:
#             driver.get(siteRoute)
#             raw = str(driver.page_source)
#             X = float(raw[raw.index("<X>") + len("<X>"): raw.index("</X>")])
#             Y = raw[raw.index("<Y>") + len("<Y>"): raw.index("</Y>")]
#             segments.ELM_Lat.values[i] = Y
#             segments.ELM_Long.values[i] = X
#         except: 
#             pass
#     segments.to_csv("../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_GPS_empties.csv", sep=",")


