import os, sys
import pandas
import numpy
import threading
import math

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


# geometrics = pandas.read_csv(folderpath + "Excel & CSV Sheets/Roadway_Geometrics.csv",sep=",",
#                              dtype={'BLM': float,'ELM':float, 'ID_NUMBER':str, 'ROW':int, 'No. Lns':int, 'Spd_Limit':int,
#                                     'Terrain':int, 'Land_Use':int, 'Illum':int, 'Operation':int, 'AccCtrl':int,
#                                     'Sch Spd Limit':int, "Truck Spd Limit":int})



# # Number of threads = 4
# 
# num_threads = 16  # This is the number of threads to generate:
# threads_working = {}
# 
# 
# def process(calldata, geometrics, thr_num):
#     global num_threads
# 
#     cd = calldata.copy()
# 
#     chunk_size = math.ceil(cd.shape[0] / num_threads)
#     start = thr_num * chunk_size
#     end = (thr_num + 1) * chunk_size
# 
#     cd = cd[start:end]
#     for k, info in enumerate(cd.values):
#         if k % 50==0:
#             print(k)
#         for i, value in enumerate(geometrics.values):
#             try:
#                 if cd.Route.values[k] == geometrics.ID_NUMBER.values[i]:
#                     if geometrics.ELM.values[i] > cd.Log_Mile.values[k] > geometrics.BLM.values[i]:
#                         cd.Terrain.values[k] = geometrics.Terrain.values[i]
#                         cd.Land_Use.values[k] = geometrics.Land_Use.values[i]
#                         cd.Access_Control.values[k] = geometrics.AccCtrl.values[i]
#                         cd.Illumination.values[k] = geometrics.Illum.values[i]
#                         cd.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
#                         cd.Operation.values[k] = geometrics.Operation.values[i]
#                         if geometrics.Sch_Spd_Limit[i] != -10:
#                             cd.School_Zone[k] = 1
#                         else:
#                             cd.School_Zone[k] = 0
#             except:
#                 pass
#     cd.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(thr_num), sep=',', index=False)
#     threads_working[thr_num] = False
# 
# 
# for i in range(num_threads):
#     thr = threading.Thread(target=process, args=(calldata, geometrics, i,))
#     threads_working[i] = True
#     thr.start()
# 
# # Wait for all threads to stop working...
# while True:
#     if True not in threads_working:
#         break
# 
# frame = pandas.DataFrame()
# list_=[]
# for i in range(num_threads):
#     df = pandas.read_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(i), sep=',')
#     list_.append(df)
# frame = pandas.concat(list_)
# frame.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo.csv", sep=',', index=False)
# 
# for i in range(num_threads):
#     os.remove(folderpath + "Excel & CSV Sheets/Routes and Miles Adding Geo_{}.csv".format(i))
# 


# calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/Routes_and_Miles_Complete.xlsx")
# hours = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Accident Data NS (Hour).xlsx")
# 
# for k, info in enumerate(hours.values):
#     print(k)
#     for i, value in enumerate(calldata.values):
#         try:
#             if calldata.Latitude.values[i] == hours.Latitude.values[k] and \
#                             calldata.Longitude.values[i] == hours.Longitude.values[k]:
#                     hours.Terrain.values[k] = calldata.Terrain.values[i]
#                     hours.Land_Use.values[k] = calldata.Land_Use.values[i]
#                     hours.Access_Control.values[k] = calldata.Access_Control.values[i]
#                     hours.Illumination.values[k] = calldata.Illumination.values[i]
#                     hours.Speed_Limit.values[k] = calldata.Speed_Limit.values[i]
#                     hours.Operation.values[k] = calldata.Operation.values[i]
#                     # if calldata.Sch_Spd_Limit[i] != -10:
#                     #     hours.School_Zone[k] = 1
#                     # else:
#                     #     hours.School_Zone[k] = 0
#         except:
#             pass
# 
# save_excel_file(folderpath + "Excel & CSV Sheets/AD Hours.xlsx", "Data That Actually Worked", hours)
calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/Routes_and_Miles_Complete.xlsx")
dates = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Accident Data NS (Date).xlsx")

for k, info in enumerate(dates.values):
    print(k)
    for i, value in enumerate(calldata.values):
        try:
            if calldata.Latitude.values[i] == dates.Latitude.values[k] and \
                            calldata.Longitude.values[i] == dates.Longitude.values[k]:
                    dates.Terrain.values[k] = calldata.Terrain.values[i]
                    dates.Land_Use.values[k] = calldata.Land_Use.values[i]
                    dates.Access_Control.values[k] = calldata.Access_Control.values[i]
                    dates.Illumination.values[k] = calldata.Illumination.values[i]
                    dates.Speed_Limit.values[k] = calldata.Speed_Limit.values[i]
                    dates.Operation.values[k] = calldata.Operation.values[i]
                    # if calldata.Sch_Spd_Limit[i] != -10:
                    #     dates.School_Zone[k] = 1
                    # else:
                    #     dates.School_Zone[k] = 0
        except:
            pass

save_excel_file(folderpath + "Excel & CSV Sheets/AD Dates.xlsx", "Data That Actually Worked", dates)

# for i, value in enumerate(geometrics.values[0:10]):
#     print(route, logmile)
#     print(geometrics.Route.values[i], geometrics.BLM.values[i], geometrics.ELM.values[i])
#     if route is geometrics.Route.values[i]:
#         print("Found Route")
        # if  geometrics.ELM.values[i] > logmile > geometrics.BLM.values[i]:
        #     print("Found logmile at index:",i)
