import osmnx as ox
import folium
import pandas as pd

from data_apis import City_Of_Calgary_ARCGIS_Rest_API as cgy

map = folium.Map(location=[51.0719, -114.048], zoom_start=12)


bike_lane = cgy.get_painted_bike_lanes()
print(bike_lane.shape)

reg_path = cgy.get_regional_pathways()
print(reg_path.shape)

graph = reg_path
graph = pd.concat([bike_lane, reg_path], axis=0)
print(graph.shape)

folium.Choropleth(reg_path, line_weight=3, line_color='red').add_to(map)
folium.Choropleth(bike_lane, line_weight=3, line_color='blue').add_to(map)

# show the map in a jupyter notebook
map

# https://stackoverflow.com/questions/55054731/geopandas-connect-points

#tags = {'cycleway':'lane'}
#place = ox.geometries_from_place('calgary', tags)
#place.explore()
