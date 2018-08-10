import gmplot
import pandas

# Place map
gmap = gmplot.GoogleMapPlotter(35.042776, -85.299202, 11)

# MAIN: Call Data for 2018 #
calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/MLK Data for Khashi.xlsx")

for k, info in enumerate(calldata.values):
    if calldata.Latitude.values[k] > 40:
        calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
        calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)

calldata.Date = calldata.Date.astype(str)

for i, value in enumerate(calldata.values):
    # All variables are blank-of-accident, thus year is yoa.
    doa = calldata.Date.values[i]
    yoa = int(doa.split('-')[0])

    lat = calldata.Latitude.values[i]
    long = calldata.Longitude.values[i]
    if yoa == 2016:
        gmap.marker(lat, long, 'cyan', title=i)
    elif yoa == 2017:
        gmap.marker(lat, long, 'green', title=i)
    elif yoa == 2018:
        gmap.marker(lat, long, 'orange', title=i)

gmap.marker(35.042776, -85.299202, "red", title="SimCenter")

gmap.draw("Accidents Map for Khashi.html")
