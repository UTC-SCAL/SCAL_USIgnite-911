import gmplot
import pandas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import radians, cos, sin, asin, sqrt

# Place map
gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)

weather_stations = data_file_name = pandas.read_excel(("Updated_Weather_Stations.xlsx"))
calldata = data_file_name = pandas.read_excel(("Agg_CallData2017.xlsx"))
# print(calldata.head())
# Call Data Lat = 1, Long = 2
# print(weather_stations.head())
# Weather Stations Lat = 5, Long = 6

# for i in enumerate(calldata.values):
# print(i, value)
# Mapping a single 911 incident
call_lat1 = (calldata.Latitude.values[0]) / 1000000
call_long1 = (calldata.Longitude.values[0]) / -1000000

call_lat2 = (calldata.Latitude.values[20]) / 1000000
call_long2 = (calldata.Longitude.values[20]) / -1000000
# print("CallData Lat: ", lat1)
# print("CallData Long: ", long1)
latcoords = []
longcoords = []
coords = []
# for i, value in weather_stations.values[0]:
#     lat1 = weather_stations.ix[i, 5]
#     long1 = weather_stations.ix[i, 6]
#     coords = coords.append(lat1+','+long1)
# lat1 = weather_stations.ix[0, 5]
# long1 = weather_stations.ix[0, 6]
for i, value in enumerate(weather_stations.values):
    coords.append(str(str(value[4]) + "," + str(value[5])))
    latcoords.append((value[4]))
    longcoords.append((value[5]))


# print(coords[0])
# print(longcoords)

# Polygon
poly_lat1 = latcoords[32]
poly_long1 = longcoords[32]
## Diamond ##
# KCHA_lats, KCHA_lons = zip(*[(poly_lat1 + 0.05, poly_long1), (poly_lat1, poly_long1 + 0.05),
#                              (poly_lat1 - 0.05, poly_long1), (poly_lat1, poly_long1 - 0.05), (poly_lat1 + 0.05, poly_long1)])

## Octagon ##
# KCHA_lats, KCHA_lons = zip(*[(poly_lat1 + 0.05, poly_long1), (poly_lat1 + 0.04, poly_long1 + 0.055), (poly_lat1, poly_long1 + 0.065), (poly_lat1 - 0.04, poly_long1 + 0.055),
#                              (poly_lat1 - 0.05, poly_long1), (poly_lat1 - 0.04, poly_long1 - 0.055), (poly_lat1, poly_long1 - 0.065),
#                              (poly_lat1 + 0.04, poly_long1 - 0.055), (poly_lat1 + 0.05, poly_long1)])

## Octagon covering ~ 5 miles ##
KCHA_lats, KCHA_lons = zip(*[(poly_lat1 + 0.08, poly_long1), (poly_lat1 + 0.07, poly_long1 + 0.085), (poly_lat1, poly_long1 + 0.095), (poly_lat1 - 0.07, poly_long1 + 0.085),
                             (poly_lat1 - 0.08, poly_long1), (poly_lat1 - 0.07, poly_long1 - 0.085), (poly_lat1, poly_long1 - 0.095),
                             (poly_lat1 + 0.07, poly_long1 - 0.085), (poly_lat1 + 0.08, poly_long1)])
## How the formula works:
    # Diamond: [(A), (B), (C), (D), (E)]
    # Octagon: [(A), point, (B), point, (C), point, (D), point, (E)]
# Put the polygon on the map
gmap.plot(KCHA_lats, KCHA_lons, 'cornflowerblue', edge_width=10)

# Scatter points
# call_lats, call_lons = zip(*[(call_lat1, call_long1)])
# stationlats = zip(*[latcoords])
# stationlongs = zip(*[longcoords])
# print(type(latcoords[0]))
c_lats, c_lons = zip(*[(call_lat1, call_long1)])
c_lats2, c_lons2 = zip(*[(call_lat2, call_long2)])


stations = []
for i, value in enumerate(weather_stations.values):
    stations.append(value[0])
# gmap.scatter(call_lats, call_lons, '#3B0B39', size=40, marker=False)

# Mapping the weather stations #
# for i,value in enumerate(latcoords[0:len(latcoords)]):
#     # print(latcoords[i])
#     # lat, lon = zip(*[latcoords[i], longcoords[i]])
#     gmap.marker(latcoords[i], longcoords[i], 'c', title= stations[i])

# Station KTNCHATT87
gmap.marker(latcoords[32], longcoords[32], 'c', title=stations[32])

# Mapping the 911 incidents
# for i ,value in enumerate(calldata.values[0:1000]):
#     lat = (value[1] / 1000000)
#     long = (value[2] / -1000000)
#     # lat,lon = zip(*[lat, long])
#     gmap.marker(lat, long, 'k')

# Individual 911 incidents
gmap.scatter(c_lats, c_lons, 'k', size=60, marker=True)
gmap.scatter(c_lats2, c_lons2, 'k', size=60, marker=True)

poly_coords = ((poly_lat1 + 0.08, poly_long1), (poly_lat1 + 0.07, poly_long1 + 0.085), (poly_lat1, poly_long1 + 0.095), (poly_lat1 - 0.07, poly_long1 + 0.085),
                             (poly_lat1 - 0.08, poly_long1), (poly_lat1 - 0.07, poly_long1 - 0.085), (poly_lat1, poly_long1 - 0.095),
                             (poly_lat1 + 0.07, poly_long1 - 0.085), (poly_lat1 + 0.08, poly_long1))
poly = Polygon(poly_coords)
p1 = Point(call_lat1, call_long1)
p2 = Point(call_lat2, call_long2)

print("Does the polygon contain the 911 incident? ", poly.contains(p1))
print("Does the polygon contain the random point? ", poly.contains(p2))

# # Marker
# hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
# gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# # Draw
gmap.draw("Chattanooga Polygons Testing.html")

## Haversine Formula ##
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
print("Distance: Center, A: ", haversine(poly_long1, poly_lat1, poly_long1, poly_lat1 + 0.10))
print("Distance: Center, B: ", haversine(poly_long1, poly_lat1, poly_long1 + 0.115, poly_lat1))
print("Distance: Center, C: ", haversine(poly_long1, poly_lat1, poly_long1, poly_lat1 - 0.10))
print("Distance: Center, D: ", haversine(poly_long1, poly_lat1, poly_long1 - 0.115, poly_lat1))
print("Distance: Center, E: ", haversine(poly_long1, poly_lat1, poly_long1, poly_lat1 + 0.10))

