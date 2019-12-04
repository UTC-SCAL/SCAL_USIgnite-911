import osmnx as ox
# G = ox.graph_from_place('Chattanooga, Tennessee, USA', network_type='drive')
# ox.plot_graph(G)


G2 = ox.graph_from_place('Isle of Wight, UK', network_type='drive')
# ox.plot_graph(G2)

basic_stats = ox.basic_stats(G2)
print(basic_stats)
# print(basic_stats['circuity_avg'])

extended_stats = ox.extended_stats(G2)
print(extended_stats)
