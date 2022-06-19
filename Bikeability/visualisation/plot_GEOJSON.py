import geopandas as gpd
import folium


# for folium plot docs  https://geopandas.org/en/stable/gallery/plotting_with_folium.html
#                       https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps

def plot_geo_paths(df, map=None):
    if map == None:
        map = folium.Map(location=[51.0719, -114.048], tiles="Stamen Terrain", zoom_start=12)
    folium.Choropleth(df.geometry).add_to(map)
    return map
    # Iterate through list and add a marker for each volcano, color-coded by its type.


if __name__ == '__main__':
    data = gpd.read_file('../data_apis/data/z.json')
    plotted_map = plot_geo_paths(data)
    plotted_map.save('map.html')
