import os
import datetime 
import pandas 
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

##Login to GIS
gis = GIS()
safegraphid = "6ac3ff66afb54f35b66cbad9f41f127c"

test = gis.content.get(safegraphid)
layer = FeatureLayerCollection(test.url)

##Pulls the individual layer out of the collection
layer = layer.layers
print(layer)
layer = layer[0]
# print(layer)
# exit()
query_result = layer.query()
print(query_result)
exit()
##Converts the query results into a dataframe. 
frame = query_result.sdf
# frame = layer.sdf
# print(frame[0])
exit()
frame = frame.loc[frame['State'] == 'TN']

print(frame[0])