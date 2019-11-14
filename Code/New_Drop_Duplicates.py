import pandas
import numpy
import time
import math
import geopy.distance

# accidents = pandas.read_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents Old Style.csv", parse_dates=["Date_Time"])
# accidents['Coords'] = accidents['Latitude'].astype(str) + " , " +accidents['Longitude'].astype(str)
# print("Total Accidents Begin", len(accidents.values))
# start = time.time()
# remove = pandas.DataFrame(columns= accidents.columns)
# for i, _ in enumerate(accidents.values):
#     if i % 100 == 0: 
#         print(i)
#     if i!=(len(accidents.values)-1):
#         j = i+1
#         dist = geopy.distance.distance(accidents.Coords[i], accidents.Coords[j]).miles
#         if (((accidents.Date_Time[j]-accidents.Date_Time[i]).seconds % 3600 / 60.0) < 30) and dist < .3:
#             remove = remove.append(accidents.iloc[[j]], ignore_index=False)
# end = time.time()

# print("Time:",end-start)
# listing = list(remove.index.values)
# accidents.drop(accidents.index[listing], inplace=True)
# print("Total Accidents End", len(accidents.values))
# accidents.to_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents No Dups.csv")
# exit()


accidents = pandas.read_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents Old Style.csv")

accidents['Unix'] = accidents.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Time).zfill(2), "%m/%d/%y %H:%M:%S"), axis=1)
accidents['Unix'] = accidents.apply(lambda x : x.Unix.strftime('%s'), axis=1)

accidents['Unix'] = accidents['Unix'].astype(str).astype(int)
accidents['Coords'] = accidents['Latitude'].astype(str) + " , " +accidents['Longitude'].astype(str)

start = time.time()
drops = list()
for i, _ in enumerate(accidents.values):
    if i % 2000 == 0: 
        print(i, round(((time.time()-start)/60),2), len(drops))
    timematches = accidents.loc[(accidents['Unix'].between((int(accidents.Unix[i]) - 3600),(int(accidents.Unix[i]) + 3600)))].index.tolist()
    if len(timematches) > 1:
        for j in timematches:
            dist = geopy.distance.distance(accidents.Coords[i], accidents.Coords[j]).miles
            if dist < .25 and (int(i) != int(j)) and j not in drops:
                drops.append(j)

keeps = accidents.drop(drops)
end = time.time()
print("Time taken:",round((end-start/60),2))
print("Total Accidents Begin", len(accidents.values))
print("Total Accidents End", len(keeps.values))
print("Difference of:", int(len(accidents.values)-len(keeps.values)), "and percent of:",\
     len(keeps.values)/len(accidents.values))
keeps.to_csv("Excel & CSV Sheets/Accidents/2017-2019 Accidents No Dups Take 5 - 2 hour window.csv")
