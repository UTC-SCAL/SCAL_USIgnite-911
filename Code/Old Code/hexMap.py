"""
Author: Jeremy Roland
Purpose: A collection of methods I used to create maps to map out our accidents and predictions
"""

from shapely.geometry import Point, Polygon
import pandas
from folium.plugins import HeatMap
import folium
import geopy.distance


def getLatLongColumns(gridCoords):
    """
    A method to convert a shape file's coords column into seperate lat and long columns
    You shouldn't need to mess with this, or use it, unless we change our grid layout
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
    gridCoords.to_csv("../")


# Create a folium heatmap of the accidents in our accident file
def accidentHeatmap(accidents):
    # Place map
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    m.add_child(folium.LatLngPopup())
    # Cut the accidents to include a certain variable value (for visualization sake)
    # accidents = accidents[accidents['DayOfWeek'] == 6]
    accidents['count'] = 1
    # Make a heatmap of the accidents
    HeatMap(data=accidents[['Latitude', 'Longitude', 'count']].groupby(
        ['Latitude', 'Longitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)
    # This actually draws or "places" the map itself for viewing
    m.save("../Main Dir/Prediction Maps/Accident Heatmap.html")


# Draw our hex grid on a folium map
def drawHexGrid():
    # Set our map
    gridCoords = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)

    # Iterate through our grid coordinate file, and set polygon objects down on our map
    for i, _ in enumerate(gridCoords.values):
        latList = gridCoords.Latitudes.values[i].split(",")
        longList = gridCoords.Longitudes.values[i].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon_geom = Polygon(zip(longList, latList))
        polygon_geom2 = polygon_geom.convex_hull
        folium.GeoJson(polygon_geom).add_to(m)
        folium.GeoJson(polygon_geom2).add_to(m)

    # Use this for adding a pointer to a given location, it currently points to the center point of Grid Num 1
    # folium.Marker(location=[float(gridCoords.Center_Lat.values[0]), float(gridCoords.Center_Long.values[0])],
    #               fill_color='#43d9de', radius=8).add_to(m)

    m.save('../Main Dir/Prediction Maps/Hex Layout.html')


# A testing method that draws only a single hex from our hex grid
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

    m.save('../Main Dir/Prediction Maps/Single Hex.html')


# Create a folium map that shows the predictions for a given dayframe of a day
def makePredictionMap(predictions, accidents, date, dayFrameCut):
    # Our file that has our grid layout information
    gridCoords = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    # Set our map
    m = folium.Map([35.0899, -85.2505], zoom_start=12, tiles='Stamen Terrain')
    folium.LatLngPopup().add_to(m)
    # Get our positive predictions (our accident predictions)
    posPredictions = predictions[predictions['Prediction'] == 1]
    # Cut our actual accidents down to the date we want to look at
    accCut = accidents[accidents['Date'] == date]
    # Add DayFrame to our actual accidents
    accCut['DayFrame'] = 0
    accCut.DayFrame = accCut.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23 else
    (2 if 5 <= x <= 9 else (3 if 10 <= x <= 13 else 4)))
    # Cut our predictions down to the dayframe we want to show
    posPredictions = posPredictions[posPredictions['DayFrame'] == dayFrameCut]
    accCut = accCut[accCut['DayFrame'] == dayFrameCut]

    # Iterate through our predictions, and layout our grid
    # Essentially, if a grid num has a corresponding prediction, it's colored in and the transparency of the color
    # reflects the probability tied to the prediction
    for i, _ in enumerate(posPredictions.values):
        predictionGrid = posPredictions.Grid_Num.values[i]
        latList = gridCoords.Y.values[predictionGrid].split(",")
        longList = gridCoords.X.values[predictionGrid].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon = Polygon(zip(longList, latList))
        folium.GeoJson(polygon, name=predictionGrid,
                       style_function=lambda x: {'fillColor': 'purple', 'color': 'black'}).add_to(m)
    # Place markers on our map for the actual accidents
    for j, _ in enumerate(accCut.values):
        folium.Marker(location=[float(accCut.Latitude.values[j]), float(accCut.Longitude.values[j])],
                      fill_color='#43d9de', radius=8).add_to(m)

    saveName = '../Main Dir/Prediction Maps/Prediction for %s DayFrame %d.html' % (date.replace("/", "-"), dayFrameCut)
    m.save(saveName)


