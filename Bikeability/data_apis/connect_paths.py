import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import LineString
import folium
import make_full_path_graph


def coords(geom):
    return list(geom.coords)


def lines_to_coordinates(gdf):
    coordinates = gdf.apply(lambda row: coords(row.geometry), axis=1)
    coordinates = list_of_tuple_to_list_of_list(coordinates)
    return coordinates


def list_of_tuple_to_list_of_list(list_of_tuples):
    coordinates = [x for xs in list_of_tuples for x in xs]
    coordinates = [[x[0], x[1]] for x in coordinates]
    return coordinates


def find_linestring_endpoints(line):
    """
    :param line: shapely.geometry.LineString
    :return: list of endpoints
    """
    return [line.coords[0], line.coords[-1]]


def connect_paths(df):
    """
    :param df: dataframe with geometry linestring and label columns
    :return: dataframe with connected paths
    """
    df = df.explode(index_parts=False)
    endpoints = list_of_tuple_to_list_of_list(df.geometry.apply(find_linestring_endpoints))
    new_df = tree_nearest(endpoints, df.crs)
    new_df = df.merge(new_df, on=['label', 'geometry'], how='outer')
    print('dissolving')
    #new_df = new_df.dissolve(by='label')
    return new_df


def tree_nearest(ends, crs, radius=.02):
    endpoints = np.array(ends)
    kd_tree1 = cKDTree(endpoints)
    indexes = kd_tree1.query_pairs(r=radius)
    # vectorization? What dat?
    print('making lines')
    lines = []
    for i in indexes:
        if (((endpoints[i[0], 0] - endpoints[i[1], 0]) ** 2 + (
                endpoints[i[0], 1] - endpoints[i[1], 1]) ** 2) ** .5) != 0:
            lines.append(
                LineString([(endpoints[i[0], 0], endpoints[i[0], 1]), (endpoints[i[1], 0], endpoints[i[1], 1])]))
    df = gpd.GeoDataFrame({'geometry': lines, 'label': np.zeros(len(lines))}, crs=crs)
    df['label'] = 'Connectors'
    print('dissolving')
    out_df = gpd.GeoDataFrame(df.head(1))
    out_df['label'] = '0'
    parts = 40
    for i in range(parts):
        print(f"Part {i}")
        out_df = out_df.merge(df.iloc[i::parts].dissolve(by='label'), on=['label', 'geometry'], how='outer')
        print(len(out_df))

    out_df = out_df[out_df['label'] != '0']
    return out_df


if __name__ == '__main__':
    trails = make_full_path_graph.get_trails()
    paths = connect_paths(trails)
    paths.crs = trails.crs
    map = folium.Map(location=[51.0719, -114.048], tiles="Stamen Terrain", zoom_start=12)
    # add the points to the map
    print('plotting')
    folium.Choropleth(paths.geometry, fill_color='green', line_color='green').add_to(map)
    folium.Choropleth(trails.geometry, fill_color='red', line_color='red').add_to(map)

    map.save('map.html')
