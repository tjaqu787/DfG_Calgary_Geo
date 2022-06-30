import osmnx as ox
import folium
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pickle as pkl

from data_apis import City_Of_Calgary_ARCGIS_Rest_API as cgy

# create map centered in Calgary
map = folium.Map(location=[51.0719, -114.048], zoom_start=12)

# gathering the data
lanes = {}
lanes['red'] = cgy.get_protected_bike_lanes()
lanes['green'] = cgy.get_bike_routes()
lanes['blue'] = cgy.get_painted_bike_lanes()
lanes['magenta'] = cgy.get_regional_pathways()
cgy_path_conn = gpd.read_file('cgy-pathways-connectors-20220622.shp')
lanes['purple'] = cgy_path_conn['geometry']
cgy_bikeways = gpd.read_file('geo_export_a12e575d-0408-4516-8fd8-e9bf368796d5.shp')
lanes['black'] = cgy_bikeways['geometry']

# creating the GeoDataFrame to store all the data
graph = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326')
for k,v in lanes.items():
    df_v = gpd.GeoDataFrame(data=v.geometry, columns=['geometry'])
    graph = pd.concat([graph, df_v], axis=0)
    print(k, ':', v.shape)

# Cleaning
graph.drop_duplicates(inplace=True)
# TODO Remove short lines

# Getting the initial and final point coordinates of each LineString
graph_bounds = graph.geometry.bounds

# all the paths together
print('Final graph:', graph.shape)

with open('data_clean.pkl', 'wb') as f:
    pkl.dump([graph, graph_bounds], f)



folium.Choropleth(graph, line_weight=2, line_color='red').add_to(map)

# show the map in a jupyter notebook
map

# https://stackoverflow.com/questions/55054731/geopandas-connect-points

#tags = {'cycleway':'lane'}
#place = ox.geometries_from_place('calgary', tags)
#place.explore()
