"""
Author: Jeremy Roland
Purpose: A collection of methods I used to create maps to map out our accidents and predictions
"""

from shapely.geometry import Polygon
import pandas
from folium.plugins import HeatMap
import folium
import geopy.distance


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

    m.save('../Main Dir/Prediction Maps/Hex Layout.html')


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
    # Cut our predictions down to just the values with a probability above some threshold
    if dayFrameCut == 1:
        posPredictions = posPredictions[posPredictions['Probability'] >= .80]
    elif dayFrameCut == 2:
        posPredictions = posPredictions[posPredictions['Probability'] >= .75]
    elif dayFrameCut == 3:
        posPredictions = posPredictions[posPredictions['Probability'] >= .50]
    elif dayFrameCut == 4:
        posPredictions = posPredictions[posPredictions['Probability'] >= .60]
    else:
        print("You entered the wrong dayFrame, fool")
        exit()

    # These lists are for finding neighboring grids to map a different color
    predictionGrids = posPredictions.Grid_Num.unique()  # Our list of grids that have predictions for accidents
    # Get a list of accident grids that are not in our list of prediction grids
    accNoMatchGrids = [i for i in accCut.Grid_Num.values if i not in predictionGrids]
    # Save this list for appending matched neighboring grids
    neighborMatchGrids = []
    # Get neighboring grids
    for accGrid in accNoMatchGrids:
        # Iterate through our list of accident grids and get the center point for the grid num
        # Note: the grid value needs to be reduced by 1 since the Grid_Num is being used as a row num
        # since python does counting like [0...max], we need to decrease our look up number by 1
        # The way the gridCoords file is set up, Grid_Num 1 has row 0, and Grid_Num 694 has row 693
        accCenterLat = gridCoords.Center_Lat.values[accGrid - 1]
        accCenterLong = gridCoords.Center_Long.values[accGrid - 1]
        accCoords = (float(accCenterLat), float(accCenterLong))

        for predGrid in predictionGrids:
            # Iterate through our list of prediction grids and get the center point for the grid num
            predCenterLat = gridCoords.Center_Lat.values[predGrid - 1]
            predCenterLong = gridCoords.Center_Long.values[predGrid - 1]
            predCoords = (float(predCenterLat), float(predCenterLong))
            # Get the distance in miles between the center point of our hotspot and the actual accident
            # The distance used can be altered accordingly
            # The distance between each hexagon in our grid is 0.509... miles, so round it up to 0.51 to find out if
            # the grids are neighbors
            distance = geopy.distance.vincenty(accCoords, predCoords).miles
            if distance <= 0.51:
                neighborMatchGrids.append(accGrid)

    # Place our predicted grids on the map
    for i, _ in enumerate(posPredictions.values):
        predictionGrid = posPredictions.Grid_Num.values[i] - 1
        latList = gridCoords.Latitudes.values[predictionGrid].split(",")
        longList = gridCoords.Longitudes.values[predictionGrid].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon = Polygon(zip(longList, latList))
        folium.GeoJson(polygon, name=predictionGrid,
                       style_function=lambda x: {'fillColor': 'purple', 'color': 'black'}).add_to(m)

    # Place markers on our map for the actual accidents
    # Split the Join Count variable into chunks, and based on the grid num of the accident we're mapping, we'll
    # select the color and icon to use based on that join count
    histMax = gridCoords.Join_Count.max()  # highest join count value
    histMin = gridCoords.Join_Count.min()  # lowest join count value
    histFirstThird = int(histMax * .33)  # first quarter join count value
    histLastThird = int(histMax * .66)  # last quarter join count value
    for j, _ in enumerate(accCut.values):
        # Get the row number of the corresponding grid number for our accident in our grid data file
        info_row_num = gridCoords.loc[gridCoords["Grid_Num"] == accCut.Grid_Num.values[j]].index[0]
        # Get the associated join count for our accident record, then base the color and icon of the map marker based
        # on it
        accHistoricRisk = gridCoords.Join_Count.values[info_row_num]
        if histMin <= accHistoricRisk <= histFirstThird:
            colorSelect = 'blue'
            iconSelect = 'arrow-down'
        elif histFirstThird < accHistoricRisk <= histLastThird:
            colorSelect = 'purple'
            iconSelect = 'minus'
        elif histLastThird < accHistoricRisk <= histMax:
            colorSelect = 'red'
            iconSelect = 'arrow-up'
        else:
            print("error in assigning colorSelect for accident points")
            exit()
        # Place a marker on the map for the current accident record we're looking at
        folium.Marker(location=[float(accCut.Latitude.values[j]), float(accCut.Longitude.values[j])],
                      icon=folium.Icon(color=colorSelect, icon=iconSelect)).add_to(m)
    # Place the matched neighboring grids on our map, with a different color to distinguish them
    for grid in neighborMatchGrids:
        latList = gridCoords.Latitudes.values[grid - 1].split(",")
        longList = gridCoords.Longitudes.values[grid - 1].split(",")
        longList = list(map(lambda x: float(x), longList))
        latList = list(map(lambda x: float(x), latList))

        polygon = Polygon(zip(longList, latList))
        folium.GeoJson(polygon, name=grid,
                       style_function=lambda x: {'fillColor': 'yellow', 'color': 'black'}).add_to(m)

    saveName = '../Main Dir/Prediction Maps/Prediction for %s DayFrame %d.html' % (date.replace("/", "-"), dayFrameCut)
    m.save(saveName)


################################################ Make a Prediction Map #################################################
# predictions is a forecast file that has the accident predictions performed for a given day
predictionPath = 'Main Dir/Logistic Regression Tests/LogReg_SS 5050_Forecast_2021-01-01.csv'
predictions = pandas.read_csv("../%s" % predictionPath)
# accidents is the file that has our accidents fetched through the email code
accidents = pandas.read_csv("../Main Dir/Accident Data/EmailAccidentData_2021-02-08.csv")
# date is the date that the prediction file has predictions for. Make sure its format matches the date format of the
# accidents file
date = predictionPath.split("_")[3].split(".")[0]
# dayFramecut is the aggregated hour you want the prediction map to cover (1, 2, 3, 4)
dayFrameCut = 4

makePredictionMap(predictions, accidents, date, dayFrameCut)
########################################################################################################################

################################################ Create a Heatmap ######################################################
# accidents is the file that has our accidents fetched through the email code
# accidents = pandas.read_csv("../")
# Use this or a new statement to cut your data that you want to create a heat map of
# accCut = accidents[accidents['Date'].str.contains('2020')]
# accidentHeatmap(accidents)
########################################################################################################################
