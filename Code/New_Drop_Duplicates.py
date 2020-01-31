import pandas
import numpy
import time
import math
import geopy.distance
import swifter

# accidents = pandas.read_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents Old Style.csv")

accidents = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/RawAccidentData.csv")

# print(len([i for i in accidents.Latitude if i > 36]) )
# exit()

cleaned = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/RawAccidentData_DropDups.csv")

lastcleaned = pandas.Timestamp(cleaned['Response Date'].values[-1]).date()
accidents['Date'] = accidents.apply(lambda x : pandas.Timestamp(x['Response Date']).date(), axis=1)

# print(type(lastcleaned))
# print(type(accidents['Response Date'].values[0]))
# exit()
# accidents['Unix'] = accidents.swifter.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Time).zfill(2), "%m/%d/%y %H:%M:%S"), axis=1)
# accidents['Unix'] = accidents.swifter.apply(lambda x : x.Unix.strftime('%s'), axis=1)

# accidents['Unix'] = accidents.swifter.apply(lambda x : pandas.datetime.strptime(x.Response_Date, "%m/%d/%y %H:%M"), axis=1)
# accidents['Unix'] = accidents.swifter.apply(lambda x : x.Unix.strftime('%s'), axis=1)

# accidents['Unix'] = accidents['Unix'].astype(str).astype(int)
accidents['Coords'] = accidents['Latitude'].astype(str) + " , " +accidents['Longitude'].astype(str)
# print(accidents.tail())

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
print("Time taken:",round(((end-start)/60),2))
print("Total Accidents Begin", len(accidents.values))
print("Total Accidents End", len(keeps.values))
print("Difference of:", int(len(accidents.values)-len(keeps.values)), "and percent of:",\
     round(100*len(keeps.values)/len(accidents.values),2))
keeps.to_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/RawAccidentData_DropDupsTest.csv")