import osmnx as ox
import folium
import pandas as pd
import matplotlib.pyplot as plt

from data_apis import City_Of_Calgary_ARCGIS_Rest_API as cgy

map = folium.Map(location=[51.0719, -114.048], zoom_start=12)

lanes = {}
lanes['red'] = cgy.get_protected_bike_lanes()
lanes['green'] = cgy.get_bike_routes()
lanes['blue'] = cgy.get_painted_bike_lanes()
lanes['magenta'] = cgy.get_regional_pathways()

graph = pd.DataFrame()
for k,v in lanes.items():
    graph = pd.concat([graph, v], axis=0)
    print(v.shape)
    folium.Choropleth(v, line_weight=3, line_color=k).add_to(map)


print(graph.shape)


# show the map in a jupyter notebook
map

# https://stackoverflow.com/questions/55054731/geopandas-connect-points

#tags = {'cycleway':'lane'}
#place = ox.geometries_from_place('calgary', tags)
#place.explore()
