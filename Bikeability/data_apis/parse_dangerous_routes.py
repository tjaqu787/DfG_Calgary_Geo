import geopandas as gpd
import folium
from shapely.ops import snap,split

def split_line_by_point(line, tolerance: float=1.0e-12):
    return split(snap(line, line.centroid, tolerance), line.centroid)


def remove_dangerous_routes(route_df, network_df):
    """
    :param route_df: CoC bike route geo dataframe
    :param network_df: CoC traffic flow volume geo dataframe
    :return: safe routes ,dangerous routes
    """
    route_df['geometry'] = route_df.geometry.apply(split_line_by_point)
    dangerous = gpd.sjoin(route_df, network_df)
    safe = route_df[~route_df['OBJECTID'].isin(dangerous['OBJECTID'])]
    return safe, dangerous


if __name__ == '__main__':
    route_data = gpd.read_file('../data_apis/data/w.json')
    # Using the traffic volume map - its routes are mostly perfect
    traffic_data = gpd.read_file('../data_apis/data/Traffic_Volumes_for_2019.csv')
    # my csv needs to be converted to a geometry the folling 3 lines do that
    traffic_data['geometry'] = gpd.GeoSeries.from_wkt(traffic_data['multilinestring'])
    traffic_data = traffic_data.drop(columns='multilinestring')
    traffic_data = traffic_data.explode(index_parts=False)
    traffic_data.crs = route_data.crs

    x, y = remove_dangerous_routes(route_data, traffic_data)
    print()
