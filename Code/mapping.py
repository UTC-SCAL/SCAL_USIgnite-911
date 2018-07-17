import gmplot
import pandas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import radians, cos, sin, asin, sqrt
from descartes.patch import PolygonPatch
import numpy
import math


# Haversine Formula #
def haversine(long1, lat1, long2, lat2):
    # convert decimal degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # the radius of the earth in miles
    return c * r


def fill_blanks(calldata, column_to_fill):
    for i, value in enumerate(calldata[column_to_fill].values):
        if pandas.isnull(calldata.loc[i, column_to_fill]) == True or calldata.loc[i, column_to_fill] == None:
            calldata.ix[i, column_to_fill] = 0

# Place map
gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)
# Read in the weather stations and the 911 data

<<<<<<< HEAD
# All Weather Stations Reduced to Stations that actually have useful info #
# weather_stations = data_file_name = \
#     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/All_Weather_Stations_Reduced.xlsx")

# MAIN: Weather Stations for 2017 #
# weather_stations = data_file_name = \
#     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Stations_Covering_2017_Reduced.xlsx")

# MAIN: Weather Stations for 2018 #
weather_stations = data_file_name = \
    pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/2018 Weather Stations.xlsx")

# MAIN: Call Data for 2017 #
# calldata = data_file_name = \
#     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Call_Data_2017_NewStations_NoBlanks.xlsx")

# MAIN: Call Data for 2018 #
calldata = data_file_name = \
    pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData_2018_Stations_Sorted.xlsx")

# Call Data for Khashayar's Project #
# calldata = data_file_name = \
#     pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Agg_CallData.xlsx"))

=======
# All Weather Stations #
# weather_stations = data_file_name = \
#     pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Updated_Weather_Stations.xlsx"))

# Currently Used Weather Stations #
# weather_stations = data_file_name = \
#     pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Current Weather Stations.xlsx"))

# Weather Stations That Cover 2017 #
# weather_stations = data_file_name = \
#     pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Stations_Covering_2017.xlsx"))

# Weather Stations That Cover 2017 Reduced #
weather_stations = data_file_name = \
    pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Stations_Covering_2017_Reduced.xlsx"))

# Currently used weather stations and NOAA stations #
# weather_stations = data_file_name = \
#     pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/NOAA Station Finder.xlsx"))

# Call Data #
calldata = data_file_name = \
    pandas.read_excel(("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Agg_CallData2017_NoBlanks.xlsx"))
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040
calldata["Station"] = ""

# print(calldata.head())
# Call Data Lat = 1, Long = 2
# print(weather_stations.head())
<<<<<<< HEAD
# Weather Stations Lat = 4, Long = 5
=======
# Weather Stations Lat = 4, Long = 5, Station name = 1
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040

# Storing the 911 incidents
# for i in enumerate(calldata.values):
#     # print(i, value)
#     call_lat = (calldata.Latitude.values[i]) / 1000000
#     call_long = (calldata.Longitude.values[i]) / -1000000

latcoords = []  # Weather station latitudes
longcoords = []  # Weather station longitudes
coords = []  # Weather station coordinates
# Dataframe containing the 9 weather stations used
station_matches = pandas.DataFrame(index=range(len(calldata)), columns=weather_stations.Station.values)
# print(station_matches.head())


# Placing the weather station coordinates into lists
for i, value in enumerate(weather_stations.values):
    coords.append(str(str(value[4]) + "," + str(value[5])))
    latcoords.append((value[4]))
    longcoords.append((value[5]))

# Placing the weather station identifiers into a list
# Doing this allows us to hover our mouse over a weather station and see which one it is
stations = []
for i, value in enumerate(weather_stations.values):
    stations.append(value[1])

# Placing all the weather station pins on the map, marked by cyan pin
for i, value in enumerate(latcoords[0:len(latcoords)]):
    # The 3 lines are commented out, they display the additional NOAA weather station locations #
    # Use these lines only when using the NOAA stations finder xlsx file #
    # if weather_stations.ID[i] >= 7:
    # gmap.marker(latcoords[i], longcoords[i], 'g', title=stations[i])
    # else:
    gmap.marker(latcoords[i], longcoords[i], 'c', title=stations[i])

# Placing all of the 911 incident pins on the map, marked by gray and red pins
<<<<<<< HEAD
for i, value in enumerate(calldata.values):
    lat = (value[1] / 1000000)
    long = (value[2] / -1000000)
    if value[0] == 0:
        gmap.marker(lat, long, '#DCDCDC', title=i) # Places a gray marker if no injury
    elif value[0] == 1:
        gmap.marker(lat, long, '#FF0000', title=i) # Places a red marker if injury

# MLK Testing Purposes for Khashayar's tests #
# for i, value in enumerate(calldata.values):
#     lat = (value[1] / 1000000)
#     long = (value[2] / -1000000)
#     date = value[3].strftime('%Y-%m-%d')
#     year = date[0:4]
#     year = int(year)
#     if (calldata.Month.values[i] == 3 or calldata.Month.values[i] == 4) and year == 2018:
#         gmap.marker(lat, long, 'g', title=i)
#     elif (calldata.Month.values[i] == 3 or calldata.Month.values[i] == 4) and year == 2017:
#         gmap.marker(lat, long, 'b', title=i)


=======
# for i, value in enumerate(calldata.values):
#     lat = (value[1] / 1000000)
#     long = (value[2] / -1000000)
#     if value[0] == 0:
#         gmap.marker(lat, long, '#DCDCDC', title=i) # Places a gray marker if no injury
#     elif value[0] == 1:
#         gmap.marker(lat, long, '#FF0000', title=i) # Places a red marker if injury

# print(weather_stations.head())
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040
for i in range(0, len(latcoords)):
    # Center for the polygon (the weather station)
    poly_lat = latcoords[i]
    poly_long = longcoords[i]
    # Coordinates for the polygon's edges
    # The A_lat, A_long, B_lat...represent the cardinal points of the octagon (which alone represent a diamond)
    # Think of them like north, south, east, west points
    # The P1_lat, P1_long, P2_lat...represent the points in between the cardinal points in the octagon
    A_lat, A_long = poly_lat + 0.10, poly_long
    P1_lat, P1_long = poly_lat + 0.09, poly_long + 0.105
    B_lat, B_long = poly_lat, poly_long + 0.115
    P2_lat, P2_long = poly_lat - 0.09, poly_long + 0.105
    C_lat, C_long = poly_lat - 0.10, poly_long
    P3_lat, P3_long = poly_lat - 0.09, poly_long - 0.105
    D_lat, D_long = poly_lat, poly_long - 0.115
    P4_lat, P4_long = poly_lat + 0.09, poly_long - 0.105
    E_lat, E_long = poly_lat + 0.10, poly_long

    # Drawing an Octagon covering ~ 6.5 - 7 miles
    station_lats, station_longs = zip(*[(A_lat, A_long), (P1_lat, P1_long), (B_lat, B_long), (P2_lat, P2_long),
                                        (C_lat, C_long), (P3_lat, P3_long), (D_lat, D_long), (P4_lat, P4_long),
                                        (E_lat, E_long)])
<<<<<<< HEAD
    # Placing the previously drawn octagon on the map (just a visual assistant)
    gmap.plot(station_lats, station_longs, 'cornflowerblue', edge_width=10)

    # Making the actual polygon using the coordinates above
=======
#     # Placing the previously drawn octagon on the map (just a visual assistant)
    gmap.plot(station_lats, station_longs, 'cornflowerblue', edge_width=10)
#
#     # Making the actual polygon using the coordinates above
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040
#     poly_coords = ((A_lat, A_long), (P1_lat, P1_long), (B_lat, B_long), (P2_lat, P2_long), (C_lat, C_long),
#                    (P3_lat, P3_long), (D_lat, D_long), (P4_lat, P4_long), (E_lat, E_long))
#     poly = Polygon(poly_coords)
#     for j, value in enumerate(calldata.values):
#         # take in the 911 incident lat and long one at a time
#         call_lat = (value[1] / 1000000)
#         call_long = (value[2] / -1000000)
#         call_incident = Point(call_lat, call_long)
#         # See if the 911 incident is in the current polygon (representing a weather station)
#         if poly.contains(call_incident):
#             station_matches.loc[j, str(stations[i])] = stations[i]
#         else:
#             station_matches.loc[j, str(stations[i])] = 0
# #
# #
# # print(station_matches.head())
<<<<<<< HEAD
# writer = pandas.ExcelWriter("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Weather Station Matches 2018 Only.xlsx",
#                             engine='xlsxwriter')
# station_matches.to_excel(writer)
# workbook = writer.book
# writer.save()

# Taking out the 0's in weather station matches
# my_dwindling_sanity = []
# match_list = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Weather Station Matches 2018 Only.xlsx")
=======
# writer = pandas.ExcelWriter("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Weather Station Matches.xlsx", engine='xlsxwriter')
# station_matches.to_excel(writer)
# workbook = writer.book
# writer.save()
#
# # Taking out the 0's in weather station matches
# my_dwindling_sanity = []
# match_list = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Weather Station Matches.xlsx")
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040
# for i, value in enumerate(match_list.values):
#     call_lat = (calldata.Latitude.values[i]) / 1000000
#     call_long = (calldata.Longitude.values[i]) / -1000000
#     call_stations = []
#     # removes 0 values from match_list
#     for station in value:
#         call_stations = [x for x in value if x != 0]
#         # print(call_stations)
#     # Gets the weather station that has the lowest haversine value (the smallest distance to the 911 incident)
#     if len(call_stations) == 1:
#         value = value[value != 0]
#         my_dwindling_sanity.append(value[0])
#     elif len(call_stations) == 0:
#         my_dwindling_sanity.append("Out of Range")
#     else:
#         min_list = []
#         for j in range(0, len(call_stations)):
#             index = 0
#             mini = haversine(call_long, call_lat, longcoords[j], latcoords[j])
#             if j+1 != len(call_stations) and haversine(call_long, call_lat, longcoords[j+1], latcoords[j+1]) < mini:
#                 try:
#                     mini = haversine(call_long, call_lat, longcoords[j+1], latcoords[j+1])
#                     index = j+1
#                 except:
#                     pass
#             my_dwindling_sanity.append(call_stations[index])
#             break
#
# # for o in enumerate(my_dwindling_sanity):
# #     print(o)
# # print(len(my_dwindling_sanity))
# calldata["Station"] = my_dwindling_sanity
<<<<<<< HEAD
# writer = pandas.ExcelWriter("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/Agg_CallData2018_Stations.xlsx", engine='xlsxwriter')
=======
# writer = pandas.ExcelWriter("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Agg_CallData2017_Stations.xlsx", engine='xlsxwriter')
>>>>>>> 3602d32382d95fc62485b59d217c34f707050040
# calldata.to_excel(writer)
# workbook = writer.book
# writer.save()


gmap.draw("Chattanooga Polygons.html")
