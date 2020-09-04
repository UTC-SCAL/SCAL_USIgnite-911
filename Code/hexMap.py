from shapely.geometry import Point
import pandas
from folium.plugins import HeatMap
import folium
from shapely.geometry import Polygon
import geopy.distance


def getLatLongColumns(gridCoords):
    """
    A method to convert a shape file's coords column into seperate lat and long columns
    """
    coordinateList = list(gridCoords.coords.values)
    longList = []  # a temporary list of longitude coords
    latList = []  # a temporary list of latitude coords
    longSaveList = []  # a list of longitude coords that will be grouped by 7 to be saved
    latSaveList = []  # a list of latitude coords that will be grouped by 7 to be saved
    for j, _ in enumerate(coordinateList):
        coordGroup = coordinateList[j]
        myList = coordGroup.replace(" ", "").split(",")
        # Longs are even values
        # Lats are odd values
        for i, _ in enumerate(myList):
            if i % 2 == 0:
                longList.append(myList[i])
                # Every 7 coordinates added to the list are considered grouped, since each hex polygon has 7 points
                if len(longList) > 6:
                    longSaveList.append(longList)
                    longList = []
            else:
                latList.append(myList[i])
                if len(latList) > 6:
                    latSaveList.append(latList)
                    latList = []
    # For the HexGrid, the length of these lists should be 694
    # print(len(longSaveList))
    # print(len(latSaveList))
    gridCoords['X'] = longSaveList
    gridCoords['Y'] = latSaveList
    gridCoords.to_csv("../Jeremy Thesis/HexGrid Shape Data_fill.csv")
    exit()


def accidentHeatmap(accidents):
    # Place map
    m = folium.Map(location=[35.14, -85.17], tiles='Stamen Terrain', zoom_start=13)
    m.add_child(folium.LatLngPopup())
    # Cut the accidents to include a certain variable value (for visualization sake)
    accidents = accidents[accidents['DayOfWeek'] == 6]
    accidents['count'] = 1
    # Make a heatmap of the accidents
    HeatMap(data=accidents[['Latitude', 'Longitude', 'count']].groupby(
        ['Latitude', 'Longitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)
    # This actually draws or "places" the map itself for viewing
    m.save("../")


def drawHexGrid(gridCoords):
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)
    for i, _ in enumerate(gridCoords.values):
        latList = gridCoords.Y.values[i].split(",")
        longList = gridCoords.X.values[i].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon_geom = Polygon(zip(longList, latList))
        polygon_geom2 = polygon_geom.convex_hull
        folium.GeoJson(polygon_geom).add_to(m)
        folium.GeoJson(polygon_geom2).add_to(m)
    # Use this for adding a pointer to a given location, it currently points to the center point of Grid Num 1
    # folium.Marker(location=[float(gridCoords.Center_Lat.values[0]), float(gridCoords.Center_Long.values[0])],
    #               fill_color='#43d9de', radius=8).add_to(m)

    m.save('../Jeremy Thesis/Hex Layout.html')


def drawSingleHex(gridCoords, grid_num):
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)
    latList = gridCoords.Y.values[grid_num].split(",")
    longList = gridCoords.X.values[grid_num].split(",")
    longList = list(map(lambda x: float(x), longList))
    latList = list(map(lambda x: float(x), latList))

    polygon_geom = Polygon(zip(longList, latList))
    polygon_geom2 = polygon_geom.convex_hull
    folium.GeoJson(polygon_geom).add_to(m)
    folium.GeoJson(polygon_geom2).add_to(m)
    # Use this for adding a pointer to a given location, it currently points to the center point of Grid Num 1
    # folium.Marker(location=[float(gridCoords.Center_Lat.values[grid_num]), float(gridCoords.Center_Long.values[grid_num])],
    #               fill_color='#43d9de', radius=8).add_to(m)

    m.save('../Jeremy Thesis/Single Hex.html')


def drawSingleGhostHex(gridCoords, grid_num):
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)
    latList = gridCoords.Y.values[grid_num].split(",")
    longList = gridCoords.X.values[grid_num].split(",")
    longList = list(map(lambda x: float(x), longList))
    latList = list(map(lambda x: float(x), latList))

    ghostLatList = []
    ghostLongList = []
    for i in range(0, 7):
        centerLat = gridCoords.Center_Lat.values[grid_num]
        centerLong = gridCoords.Center_Long.values[grid_num]
        # Some simple math to get the middle point between the current point and the center point
        # This middle point is then added to the original point to create the ghost point
        # I realize now this is far easier to show than explain
        ghost_lat, ghost_long = ((latList[i] - centerLat) / 2) + latList[i], \
                                ((longList[i] - centerLong) / 2) + longList[i]
        ghostLatList.append(ghost_lat)
        ghostLongList.append(ghost_long)

    polygon_geom = Polygon(zip(longList, latList))
    polygon_geom2 = polygon_geom.convex_hull
    folium.GeoJson(polygon_geom).add_to(m)
    folium.GeoJson(polygon_geom2).add_to(m)

    ghost_polygon_geom = Polygon(zip(ghostLongList, ghostLatList))
    ghost_polygon_geom2 = ghost_polygon_geom.convex_hull
    folium.GeoJson(ghost_polygon_geom).add_to(m)
    folium.GeoJson(ghost_polygon_geom2).add_to(m)

    # Use this for adding a pointer to a given location, it currently points to the center point of Grid Num 1
    # folium.Marker(location=[float(gridCoords.Center_Lat.values[0]), float(gridCoords.Center_Long.values[0])],
    #               fill_color='#43d9de', radius=8).add_to(m)

    m.save('../Jeremy Thesis/Ghost Hex.html')


def matchAccidentsWithGhost(predictions, accidents, date):
    # Read in the grid infor
    gridInfo = pandas.read_csv("../Jeremy Thesis/HexGrid Shape Data.csv")
    # Cut your predictions to only the accidents
    posPredictions = predictions[predictions["Prediction"] == 1]
    negPredictions = predictions[predictions["Prediction"] == 0]
    # Cut your accident file to only the date you want to look at
    accCut = accidents[accidents['Date'] == date]
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                        (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    # These for loops handle the straight forward DayFrame and Grid Num matching for accidents and predictions
    TP = 0
    FN = 0
    for i, _ in enumerate(accCut.values):
        accidentPoint = Point(accCut.Latitude.values[i], accCut.Longitude.values[i])
        for j, _ in enumerate(posPredictions.values):
            if (accCut.Grid_Num.values[i] == posPredictions.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posPredictions.DayFrame.values[j]):
                TP += 1
            else:
                predictionGrid = posPredictions.Grid_Num.values[j]  # Prediction Grid Num
                # List versions of the coordinates for the Hex shape of the Grid num
                latList = gridInfo.Y.values[predictionGrid].split(",")
                longList = gridInfo.X.values[predictionGrid].split(",")
                longList = list(map(lambda x: float(x), longList))
                latList = list(map(lambda x: float(x), latList))
                # Center point for the Grid Num
                centerLat = gridInfo.Center_Lat.values[predictionGrid]
                centerLong = gridInfo.Center_Long.values[predictionGrid]
                # Lists to hold the ghost coordinates for the hex shapes
                ghostLatList = []
                ghostLongList = []
                for k in range(0, 7):
                    # Some simple math to get the middle point between the current point and the center point
                    # This middle point is then added to the original point to create the ghost point
                    # I realize now this is far easier to show than explain
                    ghost_lat, ghost_long = ((latList[k] - centerLat) / 2) + latList[k], \
                                            ((longList[k] - centerLong) / 2) + longList[k]
                    ghostLatList.append(ghost_lat)
                    ghostLongList.append(ghost_long)

                ghostPoly = Polygon(zip(ghostLongList, ghostLatList))
                if ghostPoly.contains(accidentPoint) and accCut.DayFrame.values[i] == posPredictions.DayFrame.values[j]:
                    TP += 1
                    print("Ghost grid match")
        for n, _ in enumerate(negPredictions.values):
            if (accCut.Grid_Num.values[i] == negPredictions.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negPredictions.DayFrame.values[n]):
                FN += 1
    print("True Positives: ", TP)
    print("False Negatives: ", FN)


def matchAccidentsWithDistance(predictions, accidents, date):
    # Read in the grid info
    gridInfo = pandas.read_csv("../Jeremy Thesis/HexGrid Shape Data.csv")
    # Cut your predictions to only the accidents
    posPredictions = predictions[predictions["Prediction"] == 1]
    negPredictions = predictions[predictions["Prediction"] == 0]
    # Cut your accident file to only the date you want to look at
    accCut = accidents[accidents['Date'] == date]
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
                                        (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))

    # These for loops handle the straight forward DayFrame and Grid Num matching for accidents and predictions
    TP = 0
    FN = 0
    # distTP = 0
    for i, _ in enumerate(accCut.values):
        for j, _ in enumerate(posPredictions.values):
            if (accCut.Grid_Num.values[i] == posPredictions.Grid_Num.values[j] and accCut.DayFrame.values[i] ==
                    posPredictions.DayFrame.values[j]):
                TP += 1
            # else:
            #     accCoords = (float(accCut.Latitude.values[i]), float(accCut.Longitude.values[i]))
            #     predictionGrid = posPredictions.Grid_Num.values[j]  # Prediction Grid Num
            #     # Note: the predicitonGrid value needs to be reduced by 1 since the Grid_Num is being used as a row num
            #     # since python does counting like [0...max], we need to decrease our look up number by 1
            #     # The way the gridInfo file is set up, Grid_Num 1 has row 0, and Grid_Num 694 has row 693
            #     centerLat = gridInfo.Center_Lat.values[predictionGrid - 1]
            #     centerLong = gridInfo.Center_Long.values[predictionGrid - 1]
            #     predictionCoords = (float(centerLat), float(centerLong))
            #     distance = geopy.distance.vincenty(accCoords, predictionCoords).miles
            #     if distance <= 0.25 and accCut.DayFrame.values[i] == posPredictions.DayFrame.values[j]:
            #         TP += 1
        for n, _ in enumerate(negPredictions.values):
            if (accCut.Grid_Num.values[i] == negPredictions.Grid_Num.values[n] and accCut.DayFrame.values[i] ==
                    negPredictions.DayFrame.values[n]):
                FN += 1

    TN = len(negPredictions) - FN
    FP = len(posPredictions) - TP
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    print("\tTrue Positives: ", TP)
    # print("\tTrue Positives from Distance: ", distTP)
    print("\tFalse Negatives: ", FN)
    print("\tTrue Negatives: ", TN)
    print("\tFalse Positives: ", FP)
    try:
        print("\tRecall: ", recall)
    except:
        print("\tRecall Calc Error")
    try:
        print("\tSpecificity: ", TN / (FP + TN))
    except:
        print("\tSpecificity Calc Error")
    try:
        print("\tPrecision: ", precision)
    except:
        print("\tRecision Calc Error")
    try:
        print("\tF1 Score: ", 2 * ((recall * precision) / (recall + precision)))
    except:
        print("\tF1 Score Calc Error")


def makePredictionMap(predictions, accidents, date, dayFrameCut):
    gridCoords = pandas.read_csv("../Jeremy Thesis/HexGrid Shape Data.csv")
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)
    posPredictions = predictions[predictions['Prediction'] == 1]
    accCut = accidents[accidents['Date'] == date]
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    posPredictions = posPredictions[posPredictions['DayFrame'] == dayFrameCut]
    accCut = accCut[accCut['DayFrame'] == dayFrameCut]
    for i, _ in enumerate(posPredictions.values):
        predictionGrid = posPredictions.Grid_Num.values[i]
        latList = gridCoords.Y.values[predictionGrid].split(",")
        longList = gridCoords.X.values[predictionGrid].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon = Polygon(zip(longList, latList))
        folium.GeoJson(polygon, name=predictionGrid,
                       style_function=lambda x: {'fillColor': 'purple', 'color': 'black'}).add_to(m)

    for j, _ in enumerate(accCut.values):
        folium.Marker(location=[float(accCut.Latitude.values[j]), float(accCut.Longitude.values[j])],
                      fill_color='#43d9de', radius=8).add_to(m)

    saveName = '../Jeremy Thesis/Prediction Maps/Prediction for ' + date.replace("/", "-") + \
               ' DayFrame %d.html' % dayFrameCut
    m.save(saveName)

