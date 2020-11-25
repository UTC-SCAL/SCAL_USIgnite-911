"""
Author: Jeremy Roland
Purpose: I made this way back in the day for matching nearby weather stations to our accident. This was before we
    started to use DarkSky. It doesn't serve a purpose really, other than to be a template for working with polygons
    and point objects in python
"""

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# Create Point objects
# Points could be specific accident lat and long coordinates
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

# Create Polygon
# Polygon could represent a certain area perimeter for a county or weather station
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158),
               (24.953510, 60.170104), (24.950958, 60.169990)]

poly = Polygon(coordinates)

print(p1)
print(p2)
print(poly)
# check center of polygon
print("Center of the polygon: ", poly.centroid)

# check if p1 is within polygon
print("Is p1 inside polygon?", p1.within(poly))
# check if p2 is within polygon
print("Is p2 inside polygon?", p2.within(poly))

# check if polygon contains a point
print("Does polygon contain p1?", poly.contains(p1))
print("Does polygon contain p2?", poly.contains(p2))
