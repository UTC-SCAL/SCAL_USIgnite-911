import os, sys
import pandas
import numpy
import threading
import math

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

geometrics = pandas.read_csv(folderpath + "Excel & CSV Sheets/Roadway_Geometrics.csv",sep=",",
                             dtype={'BLM': float,'ELM':float, 'ID_NUMBER':str, 'ROW':int, 'No. Lns':int, 'Spd_Limit':int,
                                    'Terrain':int, 'Land_Use':int, 'Illum':int, 'Operation':int, 'AccCtrl':int,
                                    'Sch Spd Limit':int, "Truck Spd Limit":int})

calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/Routes and Miles.xlsx")

# Number of threads = 4

num_threads = 16  # This is the number of threads to generate:
threads_working = {}


def process(calldata, geometrics, thr_num):
    global num_threads

    cd = calldata.copy()

    chunk_size = math.ceil(cd.shape[0] / num_threads)
    start = thr_num * chunk_size
    end = (thr_num + 1) * chunk_size

    cd = cd[start:end]
    for k, info in enumerate(cd.values):
        if k % 50==0:
            print(k)
        for i, value in enumerate(geometrics.values):
            try:
                if cd.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                    if geometrics.ELM.values[i] > cd.Log_Mile.values[k] > geometrics.BLM.values[i]:
                        cd.Terrain.values[k] = geometrics.Terrain.values[i]
                        cd.Land_Use.values[k] = geometrics.Land_Use.values[i]
                        cd.Access_Control.values[k] = geometrics.AccCtrl.values[i]
                        cd.Illumination.values[k] = geometrics.Illum.values[i]
                        cd.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
                        cd.Operation.values[k] = geometrics.Operation.values[i]
                        if geometrics.Sch_Spd_Limit[i] != -10:
                            cd.School_Zone[k] = 1
                        else:
                            cd.School_Zone[k] = 0
            except:
                pass
    cd.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(thr_num), sep=',', index=False)
    threads_working[thr_num] = False


for i in range(num_threads):
    thr = threading.Thread(target=process, args=(calldata, geometrics, i,))
    threads_working[i] = True
    thr.start()

# Wait for all threads to stop working...
while True:
    if True not in threads_working:
        break

frame = pandas.DataFrame()
list_=[]
for i in range(num_threads):
    df = pandas.read_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(i), sep=',')
    list_.append(df)
frame = pandas.concat(list_)
frame.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo.csv", sep=',', index=False)

for i in range(num_threads):
    os.remove(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(i))


#
#
#
# for k, info in enumerate(calldata.values[0:500]):
#     print(k)
#     for i, value in enumerate(geometrics.values):
#         try:
#             if calldata.Route.values[k] == geometrics.ID_NUMBER.values[i]:
#                 if geometrics.ELM.values[i] > calldata.Log_Mile.values[k] > geometrics.BLM.values[i]:
#                     calldata.Terrain.values[k] = geometrics.Terrain.values[i]
#                     calldata.Land_Use.values[k] = geometrics.Land_Use.values[i]
#                     calldata.Access_Control.values[k] = geometrics.AccCtrl.values[i]
#                     calldata.Illumination.values[k] = geometrics.Illum.values[i]
#                     calldata.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
#                     calldata.Operation.values[k] = geometrics.Operation.values[i]
#                     if geometrics.Sch_Spd_Limit[i] != -10:
#                         calldata.School_Zone[k] = 1
#                     else:
#                         calldata.School_Zone[k] = 0
#         except:
#             calldata.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo 1.csv", sep=',', index=False)
#
# calldata.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo 1.csv", sep=',', index=False)

# for i, value in enumerate(geometrics.values[0:10]):
#     print(route, logmile)
#     print(geometrics.Route.values[i], geometrics.BLM.values[i], geometrics.ELM.values[i])
#     if route is geometrics.Route.values[i]:
#         print("Found Route")
        # if  geometrics.ELM.values[i] > logmile > geometrics.BLM.values[i]:
        #     print("Found logmile at index:",i)
