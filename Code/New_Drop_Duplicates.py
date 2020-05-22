import pandas
import numpy
import time
import math
import geopy.distance
import swifter
from datetime import datetime


accidents = pandas.read_csv("Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData.csv")

cleaned = pandas.read_csv("Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_DropDups.csv")

lastcleaned = pandas.Timestamp(cleaned['Response Date'].values[-1]).date()

accidents['Date'] = accidents.apply(lambda x : pandas.Timestamp(x['Response Date']).date(), axis=1)
accidents['Hour'] = accidents.apply(lambda x : pandas.Timestamp(x['Response Date']).hour, axis=1)
accidents['Coords'] = accidents['Latitude'].astype(str) + " , " +accidents['Longitude'].astype(str)

start = time.time()
drops = list()
for i, _ in enumerate(accidents.values):
    if accidents.Date.values[i] >= lastcleaned:
        if i % 2000 == 0: 
            print(i, round(((time.time()-start)/60),2), len(drops))
        timematches = accidents.loc[(accidents['Unix'].between((int(accidents.Unix[i]) - 900),(int(accidents.Unix[i]) + 900)))].index.tolist()
        if len(timematches) > 1:
            for j in timematches:
                dist = geopy.distance.distance(accidents.Coords[i], accidents.Coords[j]).miles
                if dist < .25 and (int(i) != int(j)) and j not in drops and (j>i):
                    drops.append(j)
keeps = accidents.drop(drops)
end = time.time()
keeps = keeps.drop(['Coords', 'OK'], axis=1)

##Getting the hour/date combo of the unix time here to avoid any missed duplicates. 
keeps['Unix'] = keeps.apply(lambda x : pandas.datetime.strptime(str(x.Date) + " " + str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
keeps['Unix'] = keeps.apply(lambda x : x.Unix.strftime('%s'), axis=1)

print("Time taken:",round(((end-start)/60),2))
print("Total Accidents Begin", len(accidents.values))
print("Total Accidents End", len(keeps.values))
print("Difference of:", int(len(accidents.values)-len(keeps.values)), "and percent of:",\
     round(100*len(keeps.values)/len(accidents.values),2))


keeps.to_csv("Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_DropDupsTest.csv", index=False)