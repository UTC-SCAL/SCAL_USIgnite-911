import osmnx as ox
import geopandas
import matplotlib.pyplot as plt
# G = ox.graph_from_place('Chattanooga, Tennessee, USA', network_type='drive')
# ox.plot_graph(G)
# import fiona
# shape = fiona.open("/Users/peteway/Downloads/Chattanooga_Roads_City_Limits/Roads_Chat_City_Limits.shp")
shape = geopandas.read_file("/Users/peteway/Downloads/Chattanooga_Roads_City_Limits/Roads_Chat_City_Limits.shp")
print(shape.head())
print(shape.columns.values)
print(type(shape))

fig, ax = plt.subplots(figsize = (10,10))
shape.plot(ax=ax)
plt.show()

# G2 = ox.graph_from_place('Isle of Wight, UK', network_type='drive')
# # ox.plot_graph(G2)

# basic_stats = ox.basic_stats(G2)
# print(basic_stats)
# # print(basic_stats['circuity_avg'])

# extended_stats = ox.extended_stats(G2)
# print(extended_stats)
