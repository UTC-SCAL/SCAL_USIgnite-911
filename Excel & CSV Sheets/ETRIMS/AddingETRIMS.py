import pandas
import os, sys, platform
from datetime import datetime

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'
sep = "\\" if platform.system() is "Windows" else "/"

start = datetime.now()

dataset = pandas.read_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/GeoTest.csv",
                          sep=",", dtype={'Accident': int, 'Latitude': float, 'Longitude':float, 'Date':str,
                                          'Time':str,'Address':str, 'Route':str, 'Log_Mile': float,
                                          'City':str, 'Hour':int, 'Temperature':float, 'Temp_Min':float, 'Temp_Max':float,
                                          'Daily_Avg_Temp':float, 'Monthly_avg_Temp':float, 'Relative_Temp':float,
                                          'Dewpoint':float, 'Humidity':float, 'Month':int, 'Visibility':float, 'Cloud_Coverage':float,
                                          'Precipitation_Intensity':float, 'Precip_Intensity_Max':float, 'Precip_Intensity_Time':str,
                                          'Clear':int, 'Cloudy':int, 'Rain':int, 'Fog':int, 'Snow':int, 'RainBefore':int,
                                          'Terrain':float, 'Land_Use':float, 'Access_Control':float, 'Illumination':float,
                                          'Operation':float, 'Speed_Limit':float, 'Thru_Lanes':int, 'Num_Lanes':int, 'Weekday':int },
                                           parse_dates = True)
geometrics = pandas.read_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_New.csv",sep=",")
segments = pandas.read_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv",sep=",")
descriptions = pandas.read_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON.csv",sep=",")
# features = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Route_Feature_County_HAMILTON.csv".replace("/", sep),sep=",")
traffic = pandas.read_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",sep=",")

for k, info in enumerate(dataset.values):
    print(k)
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
            if segments.ELM.values[n] > dataset.Log_Mile.values[k] > descriptions.BLM.values[n]:
                if descriptions.Feature_Type.value[n] == 'PAVEMENT':
                    dataset.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
                    dataset.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
                if descriptions.Feature_Type.value[n] == 'ACCELERATION/DECELERATION LANE':
                    dataset.Turn_Lane.values[k] = 1
            else:
                print("Not found")

dataset.to_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/GeoTest.csv")
