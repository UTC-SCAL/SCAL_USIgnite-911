##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.

import pandas
import numpy
import time
import math
import geopy.distance


# points = pandas.read_csv("Excel & CSV Sheets/Accidents/Coords.csv")


# means = []
# for i, _ in enumerate(points.values):
#     if i!=(len(points.values)-1):
#         j = i+1
#         dist = geopy.distance.distance(points.Coords[i], points.Coords[j]).miles
#         means.append(dist)
#         print(i,j,dist)
# print(sum(means)/len(means))


accidents = pandas.read_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents Old Style.csv")

print(accidents.Route[0])

accidents['Road'] = accidents.apply(lambda x :x.Route[2:-3], axis=1)

accidents['Unix'] = accidents.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Time).zfill(2), "%m/%d/%y %H:%M:%S"), axis=1)
accidents['Unix'] = accidents.apply(lambda x : x.Unix.strftime('%s'), axis=1)

accidents['Unix'] = accidents['Unix'].astype(str).astype(int)
accidents['Coords'] = accidents['Latitude'].astype(str) + " , " +accidents['Longitude'].astype(str)

start = time.time()
drops = list()
for i, _ in enumerate(accidents.values):
    if i % 2000 == 0: 
        print(i, round(((time.time()-start)/60),2), len(drops))
    timematches = accidents.loc[(accidents['Unix'].between((int(accidents.Unix[i]) - 900),(int(accidents.Unix[i]) + 900)))].index.tolist()
    if len(timematches) > 1:
        for j in timematches:
            dist = geopy.distance.distance(accidents.Coords[i], accidents.Coords[j]).miles
            if dist < .25 and (int(i) != int(j)) and j not in drops and (accidents.Road[i] == accidents.Road[j]):
                drops.append(j)

keeps = accidents.drop(drops)
end = time.time()
print("Time taken:",round(((end-start)/60),2))
print("Total Accidents Begin", len(accidents.values))
print("Total Accidents End", len(keeps.values))
print("Difference of:", int(len(accidents.values)-len(keeps.values)), "and percent of:",\
     round(100*len(keeps.values)/len(accidents.values),2))
keeps.to_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents No Dups Test.csv")