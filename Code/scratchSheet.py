# This file is kept empty for testing small chunks of code easily.
# Please clear this file when you are done working on the code, and put it into whatever file it needs to go in.
import pandas
import folium
from shapely.geometry import Point, Polygon


# Draw our hex grid on a folium map
def drawHexGrid(data):
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
    for j, _ in enumerate(data.values):
        folium.Marker(location=[float(data.Latitude.values[j]), float(data.Longitude.values[j])],
                      fill_color='#43d9de', radius=8).add_to(m)

    m.save('../Main Dir/Prediction Maps/ETRIMS Road Description.html')


# Match up accidents to their grid numbers
def matchAccidentToGridNum(hexShapeFile, accDataFile):
    # Iterate over our accidents
    for j, _ in enumerate(accDataFile.values):
        print(j, "/", len(accDataFile))
        # Our accident GPS coords as a Point object
        accPoint = Point(accDataFile.Longitude.values[j], accDataFile.Latitude.values[j])
        # Iterate over our grid hexes
        for i, _ in enumerate(hexShapeFile.values):
            latList = hexShapeFile.Latitudes.values[i].split(",")
            longList = hexShapeFile.Longitudes.values[i].split(",")
            longList = list(map(lambda x: float(x), longList))
            latList = list(map(lambda x: float(x), latList))
            # A polygon object made of the GPS coords of the hex shape
            gridHex = Polygon(zip(longList, latList))
            # Check if the accident point object is within the hex shape polygon
            if accPoint.within(gridHex):
                accDataFile.Grid_Num.values[j] = hexShapeFile.Grid_Num.values[i]
                break
    # Save the newly altered accident file that now should have grid nums
    accDataFile.to_csv("../road_desc with GridNum.csv", index=False)



