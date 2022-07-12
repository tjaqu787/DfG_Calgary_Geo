import osmnx as ox
import folium
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pickle as pkl
from shapely.geometry import Point

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

# Cleaning
graph.drop_duplicates(inplace=True)
graph.reset_index(inplace=True)

# Getting the initial and final point coordinates of each LineString
graph = pd.concat([graph, graph.geometry.bounds], axis=1)
graph.drop('index', axis=1, inplace=True)

# all the paths together
print('Final graph:', graph.shape)

graph.to_pickle('data_clean.pkl')

# maybe use buffer??
# https://gis.stackexchange.com/questions/365998/how-buffering-works-in-geopandas
# https://www.codegrepper.com/code-examples/python/find+the+last+point+of+line+geopanda
buff = graph.buffer(0.2, resolution=1)
folium.Choropleth(buff, line_weight=2, line_color='red').add_to(map)
map


#%% Calculating Distances Manually
for i1,v1 in graph.iterrows():
    # matrix of distances between point v1 and v2
    mtx_dist = []
    for i2,v2 in graph.iterrows():
        if i1 == i2:
            continue
        # https://stackoverflow.com/a/63725180
        pt1 = Point(v1.maxx, v1.maxy)
        pt2 = Point(v2.maxx, v2.maxy)
        df1 = gpd.GeoDataFrame({'geometry': [pt1]})#, crs='EPSG:4326')
        df2 = gpd.GeoDataFrame({'geometry': [pt2]})
        
        # need this?
        # https://stackoverflow.com/questions/63722124/get-distance-between-two-points-in-geopandas
        # https://geobgu.xyz/py/geopandas2.html
        #pts_df2 = pts_df.shift() #We shift the dataframe by 1 to align pnt1 with pnt2
        dist = df1.distance(df2)
        print('i1:', i1, 'i2:', i2, 'dist:', dist[0])

    # TODO sort to gest the smallest distance

    # TODO consider a threshold: sometimes the 'closest' is very far





# TODO Remove short lines
# remove after connecting because some of the small parts might be useful connectors




folium.Choropleth(graph, line_weight=2, line_color='red').add_to(map)

# show the map in a jupyter notebook
map

# https://stackoverflow.com/questions/55054731/geopandas-connect-points

#tags = {'cycleway':'lane'}
#place = ox.geometries_from_place('calgary', tags)
#place.explore()
