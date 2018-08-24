import gmplot
import pandas
import os, sys
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from geopy.geocoders import Nominatim


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Place map
gmap = gmplot.GoogleMapPlotter(35.042776, -85.299202, 11)

# MAIN: Call Data for 2018 #
calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2016_to_2018.xlsx")

for k, info in enumerate(calldata.values):
    if calldata.Latitude.values[k] > 40:
        calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
        calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)

calldata.Date = calldata.Date.astype(str)




# Drawing an Octagon covering ~ 6.5 - 7 miles
MLK_lats, MLK_longs = zip(*[(35.046390, -85.308698), (35.039291, -85.288772),(35.038121, -85.289353), (35.045041, -85.309021), (35.046390, -85.308698)])
Brainerd_lats, Brainerd_longs = zip(*[(35.028186,-85.256347),(35.027001,-85.254598), (35.026027,-85.252059),
                                      (35.025325, -85.248724), (35.023579,-85.246749),(35.021950,-85.242888),
                                      (35.018193, -85.240276),(35.014987, -85.235511), (35.008983,-85.220120),
                                      (35.011233, -85.212743),(35.018433, -85.203724), (35.019733,-85.204358),
                                      (35.016494,-85.210095), (35.012780,-85.214325), (35.010836, -85.220210),
                                      (35.019077, -85.238424), (35.023033,-85.241630), (35.025494,-85.246492),
                                      (35.026529,-85.249583), (35.028791,-85.255689), (35.028186,-85.256347)])
    # Placing the previously drawn octagon on the map (just a visual assistant)
# gmap.plot(MLK_lats, MLK_longs, 'cornflowerblue', edge_width=10)
# gmap.plot(Brainerd_lats, Brainerd_longs, 'cornflowerblue', edge_width=10)
# Making the actual polygon using the coordinates above
MLKpoly_coords = ((35.046390, -85.308698), (35.039291, -85.288772),(35.038121, -85.289353), (35.045041, -85.309021), (35.046390, -85.308698))
MLKpoly = Polygon(MLKpoly_coords)
MLKcount16 = 0
MLKcount17 = 0
MLKcount18 = 0
MLK16 = pandas.DataFrame(columns=calldata.columns.values)
MLK17 = pandas.DataFrame(columns=calldata.columns.values)
MLK18 = pandas.DataFrame(columns=calldata.columns.values)


Brainerdpoly_coords = ((35.028186,-85.256347),(35.027001,-85.254598), (35.026027,-85.252059),
                                      (35.025325, -85.248724), (35.023579,-85.246749),(35.021950,-85.242888),
                                      (35.018193, -85.240276),(35.014987, -85.235511), (35.008983,-85.220120),
                                      (35.011233, -85.212743),(35.018433, -85.203724), (35.019733,-85.204358),
                                      (35.016494,-85.210095), (35.012780,-85.214325), (35.010836, -85.220210),
                                      (35.019077, -85.238424), (35.023033,-85.241630), (35.025494,-85.246492),
                                      (35.026529,-85.249583), (35.028791,-85.255689), (35.028186,-85.256347))
Brainerdpoly = Polygon(Brainerdpoly_coords)
Brainerdcount16 = 0
Brainerdcount17 = 0
Brainerdcount18 = 0
Brainerd16 = pandas.DataFrame(columns=calldata.columns.values)
Brainerd17 = pandas.DataFrame(columns=calldata.columns.values)
Brainerd18 = pandas.DataFrame(columns=calldata.columns.values)

for i, value in enumerate(calldata.values[0:-1]):
#     # All variables are blank-of-accident, thus year is yoa.
    doa = calldata.Date.values[i]
    yoa = int(doa.split('-')[0])
    moa = int(doa.split('-')[1])
    # take in the 911 incident lat and long one at a time
    lat = calldata.Latitude.values[i]
    long = calldata.Longitude.values[i]
    call_incident = Point(lat, long)
    # See if the 911 incident is in the current polygon (representing a weather station)
    if MLKpoly.contains(call_incident):
        # if yoa == 2016:
        #     MLKcount16 += 1
        #     gmap.marker(lat, long, 'cyan', title=i)
        if yoa == 2017 and 3 < moa < 8 :

            MLKcount17 += 1
            MLK17.loc[MLKcount17] = calldata.values[i]
                # (-85.308259 < long < -85.289341)
            gmap.marker(lat, long, 'green', title=i)
        elif yoa == 2018 and 3 < moa < 8:
            MLKcount18 += 1
            MLK18.loc[MLKcount18] = calldata.values[i]
            gmap.marker(lat, long, 'orange', title=i)
        else:
            pass
    if Brainerdpoly.contains(call_incident):
        # if yoa == 2016:
        #     Brainerdcount16 += 1
        #     gmap.marker(lat, long, 'cyan', title=i)
        if yoa == 2017 and moa < 8:
            Brainerdcount17 += 1
            Brainerd17.loc[Brainerdcount17]= calldata.values[i]
                # (-85.308259 < long < -85.289341)
            gmap.marker(lat, long, 'green', title=i)
        elif yoa == 2018 and moa < 8:
            Brainerdcount18 += 1
            Brainerd18.loc[Brainerdcount18]= calldata.values[i]
            gmap.marker(lat, long, 'orange', title=i)
        else:
            pass






# for i, value in enumerate(calldata.values[0:-1]):
#     # All variables are blank-of-accident, thus year is yoa.
#     doa = calldata.Date.values[i]
#     yoa = int(doa.split('-')[0])
#     # print(i)
#     # exit()
#     # print(type(calldata.Date.values[i]))
#     # yoa = calldata.Date.values[i]
#     lat = calldata.Latitude.values[i]
#     address = calldata.Address.values[i]
#     print(lat)
#     long = calldata.Longitude.values[i]
#     if yoa == 2016:
#         gmap.marker(lat, long, 'cyan', title=i)
#     elif yoa == 2017:
#             # (-85.308259 < long < -85.289341)
#         gmap.marker(lat, long, 'green', title=i)
#     elif yoa == 2018:
#         gmap.marker(lat, long, 'orange', title=i)

# gmap.marker(35.042776, -85.299202, "red", title="SimCenter")
# print("2016 Brainerd:", Brainerdcount16 )
print("2017 Brainerd:", Brainerdcount17 )
print("2018 Brainerd:", Brainerdcount18 )
def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()

# print("2016 MLK:", MLKcount16 )
print("2017 MLK:", MLKcount17 )
print("2018 MLK:", MLKcount18 )
print("MLK 2017:",MLK17[0:5])
save_excel_file(folderpath + "Road Diet/MLK17.xlsx", "MLK17", MLK17)
print("MLK 2018:",MLK18[0:5])
save_excel_file(folderpath + "Road Diet/MLK18.xlsx", "MLK18", MLK18)
print("Brainerd 2017",Brainerd17[0:5])
save_excel_file(folderpath + "Road Diet/Brainerd17.xlsx", "Brainerd17", Brainerd17)
print("Brainerd 2018:",Brainerd18[0:5])
save_excel_file(folderpath + "Road Diet/Brainerd18.xlsx", "Brainerd18", Brainerd18)

gmap.draw("Accidents Map for Khashi.html")


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

