from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas
from matplotlib import pyplot as plt


def easy_import_excel_file(file_name):
    data_file_name = pandas.read_excel(file_name)
    print('Import complete')
    return data_file_name


def main():
    # # Create Point objects
    # # Points could be specific accident lat and long coordinates
    # p1 = Point(24.952242, 60.1696017)
    # p2 = Point(24.976567, 60.1612500)
    #
    # # Create Polygon
    # # Polygon could represent a certain area perimeter for a county or weather station
    # coordinates = [(24.950899, 60.169158), (24.953492, 60.169158),
    #                (24.953510, 60.170104), (24.950958, 60.169990)]
    #
    # poly = Polygon(coordinates)
    #
    # print(p1)
    # print(p2)
    # print(poly)
    # # check center of polygon
    # print("Center of the polygon: ", poly.centroid)
    #
    # # check if p1 is within polygon
    # print("Is p1 inside polygon?", p1.within(poly))
    # # check if p2 is within polygon
    # print("Is p2 inside polygon?", p2.within(poly))
    #
    # # check if polygon contains a point
    # print("Does polygon contain p1?", poly.contains(p1))
    # print("Does polygon contain p2?", poly.contains(p2))


    weather_stations = easy_import_excel_file("somestations.xlsx")
    calldata = easy_import_excel_file("Agg_CallData2017.xlsx")
    # print(calldata.head())
    # Call Data Lat = 1, Long = 2
    # print(weather_stations.head())
    # Weather Stations Lat = 5, Long = 6

    # for i in enumerate(calldata.values):
    # print(i, value)
    # Lat and Long from calldata
    call_lat1 = (calldata.Latitude.values[0]) / 1000000
    call_long1 = (calldata.Longitude.values[0]) / -1000000
    # print("CallData Lat: ", lat1)
    # print("CallData Long: ", long1)

    # Lat and Long of weather station
    lat1 = weather_stations.ix[0, 5]
    long1 = weather_stations.ix[0, 6]
    # print("Lat1: ", call_lat1)
    # print("Long1: ", call_long1)

    # print("Altered Lat1: ", alter_lat1)
    # print("Altered Long1: ", alter_long1)
    # # Polygon (the weather station)
    station_coordinates = [(lat1, long1), (lat1, long1), (lat1, long1), (lat1, long1)]
    p1 = Point(call_lat1, call_long1)
    p2 = Point(lat1, long1)

    # Create the polygon
    poly = Polygon(station_coordinates)
    # Check if call_lat&long are in polygon coordinates
    print("Does the weather station cover the 911 call coordinates? ", poly.contains(p1))
    print("does the weather station cover the original somestations coordinates?", poly.contains(p2))



if __name__ == "__main__":
    main()
