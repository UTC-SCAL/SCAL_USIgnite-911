import gmplot
import pandas


# Place map
gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)


# MAIN: Call Data for 2017 #
# calldata = data_file_name = \
#     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017 Data/2017 CallData Agg.xlsx")

# MAIN: Call Data for 2018 #
# calldata = data_file_name = \
#     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/2018 Accident Report List Agg Options.xlsx")

# MAIN: Call Data for 2018 + 2017  #
calldata = data_file_name = \
    pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Accident Report List Agg Options.xlsx")


# print(calldata.head())
# Call Data Columns:
# Lat = 1, Long = 2
# Event = 8, Conditions = 9
# Clear = 16, Rain = 17, Snow = 18, Cloudy = 19, Foggy = 20

# Placing all of the 911 incident pins on the map, marked by gray and red pins
for i, value in enumerate(calldata.values):
    lat = calldata.Latitude.values[i]
    long = calldata.Longitude.values[i]
    if calldata.Y.values[i] == 0 and calldata.Cloudy.values[i] == 1:
        gmap.marker(lat, long, '#DCDCDC', title=i)  # Places a gray marker if no injury
    elif calldata.Y.values[i] == 1 and calldata.Cloudy.values[i] == 1:
        gmap.marker(lat, long, '#FF0000', title=i)  # Places a red marker if injury

# Map showing all 911 incidents #
# gmap.draw("2018+2017 Map.html")
# Map showing 911 incidents w/ foggy #
# gmap.draw("2017+2018 Foggy Map.html")
# Map showing 911 incidents w/ rain #
# gmap.draw("2017+2018 Rain Map.html")
# Map showing 911 incidents w/ snow #
# gmap.draw("2017+2018 Snow Map.html")
# Map showing 911 incidents w/ cloudy #
# gmap.draw("2017+2018 Cloudy Map.html")

