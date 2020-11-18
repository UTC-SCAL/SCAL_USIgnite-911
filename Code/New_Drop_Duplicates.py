"""
Author: Pete Way
Editor: Jeremy Roland
Purpose: Clean newly fetched accident files of potentially duplicate call records
"""
import pandas
import time
import geopy.distance

# The file containing the newly fetched accident records
fetchedAccidents = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_NewFetch.csv")
# The file containing our cleaned list of raw accident records
cleanedAccidents = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData.csv")
# Gets the date of the last record in our raw accident data
lastcleaned = pandas.Timestamp(cleanedAccidents['Response Date'].values[-1]).date()

fetchedAccidents['Date'] = fetchedAccidents.apply(lambda x : pandas.Timestamp(x['Response Date']).date(), axis=1)
fetchedAccidents['Hour'] = fetchedAccidents.apply(lambda x : pandas.Timestamp(x['Response Date']).hour, axis=1)
fetchedAccidents['Coords'] = fetchedAccidents['Latitude'].astype(str) + " , " + fetchedAccidents['Longitude'].astype(str)

drops = list()
for i, _ in enumerate(fetchedAccidents.values):
    if fetchedAccidents.Date.values[i] >= lastcleaned:
        # if i % 2000 == 0:
        #     print(i, round(((time.time()-start)/60),2), len(drops))
        timematches = fetchedAccidents.loc[(fetchedAccidents['Unix'].between((int(fetchedAccidents.Unix[i]) - 900),
                                                                (int(fetchedAccidents.Unix[i]) + 900)))].index.tolist()
        if len(timematches) > 1:
            for j in timematches:
                dist = geopy.distance.distance(fetchedAccidents.Coords[i], fetchedAccidents.Coords[j]).miles
                if dist < .25 and (int(i) != int(j)) and j not in drops and (j > i):
                    drops.append(j)
keeps = fetchedAccidents.drop(drops)
keeps = keeps.drop(['Coords', 'OK'], axis=1)

# Getting the hour/date combo of the unix time here to avoid any missed duplicates.
keeps['Unix'] = keeps.apply(lambda x: pandas.datetime.strptime(str(x.Date) + " " +
                                                               str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
# Depending on your OS, choose one of the following lines
# keeps['Unix'] = keeps.apply(lambda x: x.Unix.strftime('%s'), axis=1)  # For Unix or Mac
keeps['Unix'] = keeps.apply(lambda x: x.Unix.timestamp(), axis=1)  # For Windows

print("Duplicates Removed:", int(len(fetchedAccidents.values) - len(keeps.values)))
# Save the dropped duplicates version
keeps.to_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_DropDupsTest.csv", index=False)
