import numpy as np
import pandas
import os, sys
import time

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

calldata = pandas.read_csv(folderpath + "Excel & CSV Sheets/Added Addresses.csv", sep=",")
old_reports = pandas.read_csv(folderpath + "Excel & CSV Sheets/Accident Report - 4-29-2015 - 4-29-2018.csv", sep=",")
road_seg = pandas.read_csv(folderpath + "Excel & CSV Sheets/Road_Segment_County_HAMILTON.csv", sep=",")


# for k, info in enumerate(old_reports.values):
#     if old_reports.Latitude.values[k] > 40:
#         old_reports.Latitude.values[k] = (old_reports.Latitude.values[k] / 1000000)
#         old_reports.Longitude.values[k] = (old_reports.Longitude.values[k] / -1000000)

# t0 = time.time()
# for i, info in enumerate(calldata.values[0:34724]):
#     print(i)
#     for j, stuff in enumerate(old_reports.values):
#         if calldata.Latitude.values[i] == old_reports.Latitude.values[j]:
#             calldata.Address.values[i] = old_reports.Address.values[j]
# calldata.to_csv(folderpath + "Excel & CSV Sheets/Added Addresses.csv", sep=',', index=False)
# t1 = time.time()
# total = t1-t0
# # print("This fucking code took a whopping ", total)

calldata.Route = calldata.Route.astype(str)
road_seg.Road_Name = road_seg.Road_Name.astype(str)
calldata.Address = calldata.Address.astype(str)

for i, info in enumerate(calldata.values):
    print(i)
    for k, stuff in enumerate(road_seg.values):
        if road_seg.Road_Name.values[k].lower() in calldata.Address.values[i].lower():
            calldata.Route.values[i] = str(road_seg.Route.values[k])

calldata.to_csv(folderpath + "Excel & CSV Sheets/Added Addresses with Routes.csv", sep=',', index=False)