import gmplot
import pandas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os, sys


def midpoint(x1, x2, y1, y2):
    mid_lat = (x1 + x2) / 2
    mid_long = (y1 + y2) / 2
    return mid_lat, mid_long


# Creating and plotting the ghost point
# Lat_list and long_list hold the latitudes and longitudes for the current grid block's 5 points
def find_ghost(lat_list, long_list, center_lat, center_long):
    # These two lists hold the "ghost" latitude and longitudes
    # By "ghost", we mean they are superficial extensions to a grid block
    # This more or less acts as an overlapping mechanism for blocks in the grid for prediction purposes
    ghost_lats = []
    ghost_longs = []

    for i in range(0, 5):
        # Some simple math to get the middle point between the current point and the center point
        # This middle point is then added to the original point to create the ghost point
        # I realize now this is far easier to show than explain
        ghost_lat, ghost_long = ((lat_list[i] - center_lat)/2) + lat_list[i], \
                                ((long_list[i] - center_long)/2) + long_list[i]
        ghost_lats.append(ghost_lat)
        ghost_longs.append(ghost_long)

    # Now we actually make ghost polygon with the newly calculated ghost points
    # I used set numbers here since each of the grid blocks only have 5 points, as each grid block is a square
    grid_ghost_lats, grid_ghost_longs = zip(*[(ghost_lats[0], ghost_longs[0]),
                                              (ghost_lats[1], ghost_longs[1]),
                                              (ghost_lats[2], ghost_longs[2]),
                                              (ghost_lats[3], ghost_longs[3]),
                                              (ghost_lats[4], ghost_longs[4])])
    gmap.plot(grid_ghost_lats, grid_ghost_longs, 'white', edge_width=2)
    return grid_ghost_lats, grid_ghost_longs


path = os.path.dirname(sys.argv[0])
# Place map
gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)

# This file contains the coordinates for the grid blocks
gridCoords = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Vertices Oriented Layout.csv", sep=",")
# print(gridCoords.head())

# This will hold the polygon versions of our grid blocks
# The final length of this should be 1100, since we have 1100 blocks
gridLayout_Coords = []
ghostLayout_Coords = []

# Places the first 5 coordinates in the file as pins, represents the first grid block seen in Connor's diagram
# for i, value in enumerate(gridCoords.values[0:5]):
#     lat = gridCoords.Y.values[i]
#     long = gridCoords.X.values[i]
#     gmap.marker(lat, long, '#FF0000', title=i)

# Drawing the grid blocks on a gmap
for i, value in enumerate(gridCoords.values):
    if i % 5 == 0:
        # Drawing the block grid, all this does is place the grid on the map #
        # We only draw on each 5th iteration, since each grid block's coordinates are grouped by 5
        grid_lats, grid_longs = zip(*[(gridCoords.Y.values[i], gridCoords.X.values[i]),
                                      (gridCoords.Y.values[i+1], gridCoords.X.values[i+1]),
                                      (gridCoords.Y.values[i+2], gridCoords.X.values[i+2]),
                                      (gridCoords.Y.values[i+3], gridCoords.X.values[i+3]),
                                      (gridCoords.Y.values[i+4], gridCoords.X.values[i+4])])
        gmap.plot(grid_lats, grid_longs, 'cornflowerblue', edge_width=5)
        # Making the actual polygon using the coordinates above for calculations and manipulation #
        # poly_coords are the current polygon's coordinates (lat & long)
        # poly_coords = ((gridCoords.Y.values[i], gridCoords.X.values[i]),
        #                (gridCoords.Y.values[i+1], gridCoords.X.values[i+1]),
        #                (gridCoords.Y.values[i+2], gridCoords.X.values[i+2]),
        #                (gridCoords.Y.values[i+3], gridCoords.X.values[i+3]),
        #                (gridCoords.Y.values[i+4], gridCoords.X.values[i+4]))
        # # Append the poly_coords to a list for later use
        # gridLayout_Coords.append(poly_coords)

        # # Getting the center points for the polygons and assigning them accordingly to the grid blocks
        # poly = Polygon(poly_coords)
        # center = poly.centroid.coords
        # # The center coordinates for the current grid block
        # center_lat = center[0][0]  # Latitude
        # center_long = center[0][1]  # Longitude
        # gridCoords.Center_Lat.values[i] = center_lat
        # gridCoords.Center_Long.values[i] = center_long

        # Drawing the ghost grid blocks #
        # ghost_lats, ghost_longs = zip(*[(gridCoords.Ghost_Lat.values[i], gridCoords.Ghost_Long.values[i]),
        #                                 (gridCoords.Ghost_Lat.values[i+1], gridCoords.Ghost_Long.values[i+1]),
        #                                 (gridCoords.Ghost_Lat.values[i+2], gridCoords.Ghost_Long.values[i+2]),
        #                                 (gridCoords.Ghost_Lat.values[i+3], gridCoords.Ghost_Long.values[i+3]),
        #                                 (gridCoords.Ghost_Lat.values[i+4], gridCoords.Ghost_Long.values[i+4])])
        # gmap.plot(ghost_lats, ghost_longs, 'white', edge_width=2)
        # # Making the actual ghost polygons using the ghost coordinates above for calculations and manipulations #
        # ghost_coords = ((gridCoords.Ghost_Lat.values[i], gridCoords.Ghost_Long.values[i]),
        #                 (gridCoords.Ghost_Lat.values[i+1], gridCoords.Ghost_Long.values[i+1]),
        #                 (gridCoords.Ghost_Lat.values[i+2], gridCoords.Ghost_Long.values[i+2]),
        #                 (gridCoords.Ghost_Lat.values[i+3], gridCoords.Ghost_Long.values[i+3]),
        #                 (gridCoords.Ghost_Lat.values[i+4], gridCoords.Ghost_Long.values[i+4]))
        # # Append the poly_coords to a list for later use #
        # ghostLayout_Coords.append(ghost_coords)
# This is for saving any changes to the grid coordiantes file
# gridCoords.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Vertices OS Layout.csv")

# This code was used for initially finding the coordinates for the ghost grid blocks #
        # Finding the ghost coordinates for the ghost grid
        # Get the center coordinates for the current grid block's polygon
#         poly = Polygon(poly_coords)
#         center = poly.centroid.coords
#         # The center coordinates for the current grid block
#         center_lat = center[0][0]  # Latitude
#         center_long = center[0][1]  # Longitude
#         # Place a marker on the map for each center point (helps with visualizing ghost grid)
#         gmap.marker(center_lat, center_long, '#FF0000', title=i)
#         ghost_grid_lats, ghost_grid_longs = find_ghost(grid_lats, grid_longs, center_lat, center_long)
#         # Append the newly made ghost coordinates to the main vertices points file for future use
#         # I know this isn't the prettiest code, but forget your opinion 'cause it works
#         gridCoords.Ghost_Lat.values[i], gridCoords.Ghost_Long.values[i] = ghost_grid_lats[0], ghost_grid_longs[0]
#         gridCoords.Ghost_Lat.values[i+1], gridCoords.Ghost_Long.values[i+1] = ghost_grid_lats[1], ghost_grid_longs[1]
#         gridCoords.Ghost_Lat.values[i+2], gridCoords.Ghost_Long.values[i+2] = ghost_grid_lats[2], ghost_grid_longs[2]
#         gridCoords.Ghost_Lat.values[i+3], gridCoords.Ghost_Long.values[i+3] = ghost_grid_lats[3], ghost_grid_longs[3]
#         gridCoords.Ghost_Lat.values[i+4], gridCoords.Ghost_Long.values[i+4] = ghost_grid_lats[4], ghost_grid_longs[4]
# gridCoords.to_csv("../")
        

# Checking to see what calldata records each grid block has #
# calldata = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Data 2017+2018.csv", sep=",")
# for j in range(1, len(gridLayout_Coords)):
#     poly = Polygon(gridLayout_Coords[j])  # This is the grid block for the current iteration
#     print(j)
#     # take in the 911 incident lat and long one at a time
#     for o, value2 in enumerate(calldata.values):
#         call_lat = calldata.Latitude.values[o]
#         call_long = calldata.Longitude.values[o]
#         call_incident = Point(call_lat, call_long)
#         # See if the 911 incident is in the current grid block polygon
#         if poly.contains(call_incident):
#             calldata.Grid_Block.values[o] = j
#         else:
#             pass
# calldata.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Data 2017+2018.csv")

# Getting the center coordinate of each grid block #
# These will be our weather points for each grid block
# for j in range(0, len(gridLayout_Coords)):
#     poly = Polygon(gridLayout_Coords[j])  # This is the grid block for the current iteration
#     center = poly.centroid.coords
#     # The center coordinates for the current grid block
#     center_lat = center[0][0]  # Latitude
#     center_long = center[0][1]  # Longitude
#     # This places a point marker at the center of each grid block
#     gmap.marker(center_lat, center_long, '#FF0000', title=j)

# Placing markers for predicted accidents
predictions = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Forecast-for6-10-2019_2019-06-11_11.csv")
for p, values in enumerate(predictions.values):
    if predictions.Probability.values[p] >= .80 and 19 <= predictions.Hour.values[p] <= 23:
        gmap.marker(predictions.Latitude.values[p], predictions.Longitude.values[p], '#FF0000', title=p)


# This actually draws or "places" the map itself for viewing #
gmap.draw("Chattanooga Polygons.html")