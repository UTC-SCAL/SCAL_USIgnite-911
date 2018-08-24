import pandas
import os, sys
from datetime import datetime
import numpy as np
import gmplot
from geopy.geocoders import Nominatim
from string import digits
from math import sin, cos, sqrt, atan2, radians, asin


gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'
R = 6373.0  # Radius of the globe

start = datetime.now()

# MAIN Calldata 2018 + 2017 #
calldata = pandas.read_excel(folderpath + "Road Diet/Brainerd18.xlsx")


roadwaydata = pandas.read_excel(folderpath + "Excel & CSV Sheets/Roadways_with_Roadnames.xlsx")


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


#          Mapping the Calls and their AADT Stations           #

# for i, value in enumerate(calldata.values[0:1000]):
#     lat = calldata.Latitude.values[i]
#     long = calldata.Longitude.values[i]
#     gmap.marker(lat, long, '#FF0000', title=calldata.index.values[i])  # Places a red marker for call

#     roadlat = calldata.Road_Lat.values[i]
#     roadlong = calldata.Road_Long.values[i]
#     gmap.marker(roadlat, roadlong, 'b', title=calldata.index.values[i])


calldata["Road_Station"] = pandas.Series(index=calldata.index)
calldata["AADT"] = pandas.Series(index=calldata.index)
calldata["Road_Lat"] = pandas.Series(index=calldata.index)
calldata["Road_Long"] = pandas.Series(index=calldata.index)
calldata.Road_Station = calldata.Road_Station.astype(str)
calldata.AADT = calldata.AADT.astype(float)
calldata.Road_Lat = calldata.Road_Lat.astype(float)
calldata.Road_Long = calldata.Road_Long.astype(float)


def get_AADT_no_road(j):
    matchlist = []
    minilist = []
    print(j)
    for p,value in enumerate(roadwaydata.values):
        matchlist.append(roadwaydata.StationNumber.values[p])
        lat1 = radians(roadwaydata.Latitude.values[p])
        lon1 = radians(roadwaydata.Longitude.values[p])
        lat2 = radians(calldata.Latitude.values[j])
        lon2 = radians(calldata.Longitude.values[j])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        minilist.append(round(distance,2))

    minindex = minilist.index(min(minilist))

    match = matchlist[minindex]
    calldata.Road_Station.values[j] = match
    calldata.AADT.values[j] = \
    roadwaydata.loc[roadwaydata['StationNumber'] == match, 'AADT_10_Year_Average'].iloc[0]
    calldata.Road_Lat.values[j] = \
        roadwaydata.loc[roadwaydata['StationNumber'] == match, 'Latitude'].iloc[0]
    calldata.Road_Long.values[j] = \
        roadwaydata.loc[roadwaydata['StationNumber'] == match, 'Longitude'].iloc[0]


def get_AADT(j):
    calldata.Address = calldata.Address.astype(str)
    matchlist = []
    latcoords = []
    longcoords = []
    minilist = []
    road = calldata.Address.values[j]
    # print("Call Road",road)
    road = road.lstrip(digits)
    road = road.split("/")[0]
    lat = calldata.Latitude.values[j]
    long = calldata.Longitude.values[j]
    index = 0
    try:
        print(j)
        for i, value in enumerate(roadwaydata.values):
            aadtroad = roadwaydata.Road.values[i]
            aadtroad = aadtroad.lstrip(digits)
            if road in aadtroad:
                print("AADT Road",aadtroad)
                print("Match found!",road, ":", aadtroad)
                # print("Match")
                matchlist.append(roadwaydata.StationNumber.values[i])
                latcoords.append(roadwaydata.Latitude.values[i])
                longcoords.append(roadwaydata.Longitude.values[i])
                print(matchlist)

        for p in range(0, len(matchlist)):
            lat1 = radians(latcoords[p])
            lon1 = radians(longcoords[p])
            lat2 = radians(lat)
            lon2 = radians(long)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            minilist.append(distance)

        minindex = minilist.index(min(minilist))
        match = matchlist[minindex]
        calldata.Road_Station.values[j] = match
        calldata.AADT.values[j] = \
        roadwaydata.loc[roadwaydata['StationNumber'] == match, 'AADT_10_Year_Average'].iloc[0]
        calldata.Road_Lat.values[j] = \
            roadwaydata.loc[roadwaydata['StationNumber'] == match, 'Latitude'].iloc[0]
        calldata.Road_Long.values[j] = \
            roadwaydata.loc[roadwaydata['StationNumber'] == match, 'Longitude'].iloc[0]

    except:
        get_AADT_no_road(j)


# #Finding addresses for the AADT stations.
def find_address(i):
    calldata.Address = calldata.Address.astype(str)
    # empty_test = pandas.isnull(calldata.Address.values[i])
    # if empty_test is True:
    latlong = calldata.Latitude.values[i], calldata.Longitude.values[i]
    print(i)
    try:
        geolocator = Nominatim()
        location = geolocator.reverse(latlong)
        location = str(location).split(",")
        road = str(location[0:2])
        calldata.Address.values[i] = road
    except:
        calldata.Address.values[i] = "Address not found"
    else:
        pass

for k, info in enumerate(calldata.values):
    if calldata.Latitude.values[k] > 40:
        calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
        calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)
for i, info in enumerate(calldata.values):
    find_address(i)

save_excel_file(folderpath + "Road Diet/Brainerd18.xlsx", "Brainerd18", calldata)
