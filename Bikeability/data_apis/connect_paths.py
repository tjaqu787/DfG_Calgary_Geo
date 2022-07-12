import geopandas as gpd
import numpy as np
import pandas as pd
import folium
from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString


def coords(geom):
    return list(geom.coords)


def lines_to_coordinates(gdf):
    coordinates = gdf.apply(lambda row: coords(row.geometry), axis=1)
    coordinates = [x for xs in coordinates for x in xs]
    coordinates = [[x[1], x[0]] for x in coordinates]
    return coordinates


def find_linestring_endpoints(line):
    """
    :param line: shapely.geometry.LineString
    :return: list of endpoints
    """
    return [line.coords[0], line.coords[-1]]


def connect_paths(df):
    """
    :param df: dataframe with geometry linestring column
    :return: dataframe with connected paths
    """
    df = df.explode(index_parts=False)
    points = lines_to_coordinates(df)
    endpoints = df.geometry.apply(find_linestring_endpoints)
    new_df = tree_nearest(endpoints, points)
    new_df.crs = df.crs
    new_df = df.append(new_df)
    new_df = new_df.geometry.simplify(0.0002)
    return new_df


def tree_nearest(ends, points):
    coordinates = [x for xs in ends for x in xs]
    coordinates = [[x[1], x[0]] for x in coordinates]
    endpoints = np.array(coordinates)
    line_points = np.array(points)
    kd_tree1 = cKDTree(endpoints)
    kd_tree2 = cKDTree(points)
    indexes = kd_tree1.query_ball_tree(kd_tree2, r=0.002)
    # vectorization? Whats that?
    lines = []
    for i in range(len(indexes)):
        for j in indexes[i]:
            lines.append(LineString([(endpoints[i, 0], line_points[j, 0]),(endpoints[i, 1], line_points[j, 1])]))
    df = pd.DataFrame({'geometry': lines})
    return df


if __name__ == '__main__':
    regional_paths = gpd.read_file('../data_apis/data/y.json')
    paths = connect_paths(regional_paths)
    paths.crs = regional_paths.crs
    map = folium.Map(location=[51.0719, -114.048], tiles="Stamen Terrain", zoom_start=12)
    folium.Choropleth(regional_paths.geometry,fill_color='red',line_color='red').add_to(map)
    folium.Choropleth(paths.geometry,fill_color='green',line_color='green').add_to(map)

    map.save('map.html')
