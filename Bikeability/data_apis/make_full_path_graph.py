from sodapy import Socrata
import os.path
import esri2gpd
import geopandas as gpd
from shapely import geometry
from pandas import concat
import connect_paths

"""
Author Tyrell Jaques 2022-08-08
pulls and saves all data for the calgary bike network
Labels for pathways= regional_pathways,trails,bike_routes,protected_bike_lanes,painted_bike_lanes,bike_routes
"""

def meta_data():
    """
    :return: epsg, max_min
    """
    epsg = 4326

    max_min = {}
    return epsg, max_min

def get_socrata(file_name, endpoint, host_url='data.calgary.ca'):
    if not os.path.exists(file_name):
        print(f'{file_name} does not exist. Downloading new data...')
        client = Socrata(host_url, None)
        results = gpd.GeoDataFrame(client.get(endpoint))
        print(f'Data downloaded. Saving to {file_name}...')
        results.to_file(file_name, driver="GeoJSON")
    else:
        print(f'{file_name} exists. Loading data from disk...')
        results = gpd.read_file(file_name)
    return results


def get_arcgis(file_name, url):
    if not os.path.exists(file_name):
        print(f'{file_name} does not exist. Downloading new data...')
        results = gpd.GeoDataFrame(esri2gpd.get(url))
        print(f'Data downloaded. Saving to {file_name}...')
        results.to_file(file_name, driver="GeoJSON")
        print(f'Data downloaded. Saving to {file_name}...')
    else:
        print(f'{file_name} exists. Loading data from disk...')
        results = gpd.read_file(file_name)
    return results


def get_traffic_flow():
    """
    Returns a dataframe of traffic flow data from the Calgary Traffic Flow API
    2019 traffic flow map
    :return: dataframe of labels and line-strings
    """
    file_name = "data/traffic_flow.json"
    url = 'qeqv-tb2c'
    traffic_flow = get_socrata(file_name, url)
    return traffic_flow[['label', 'geometry']]


def get_rtm_zones():
    epsg = 4326
    file_name = "data/pathways.json"
    url = '4c3g-8je3'
    rtm_zones = get_socrata(file_name, url)

    # build shapely polygons from coordinates
    rtm_zones['geometry'] = [geometry.Polygon(rtm_zones['the_geom'][i]['coordinates'][0]) for i in
                             range(len(rtm_zones['the_geom']))]
    rtm_zones.drop(columns='the_geom', inplace=True)

    # set coordinate reference system
    rtm_zones.set_crs(epsg=epsg, inplace=True)

    # return filtered values, City of Calgary only
    return rtm_zones[rtm_zones['region'] == '0']


def get_connectors():
    url = '6eun-p5zf'
    file_name = "data/pathways.json"
    connectors = get_socrata(file_name, url)
    connectors['label'] = 'regional_pathways'
    return connectors[['label', 'geometry']]


def get_roads():
    file_name = "data/roads.json"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/RoadClassification/MapServer/0'
    routes = get_arcgis(file_name, url)
    routes['label'] = routes['ROAD_CLASS']
    return routes[['label', 'geometry']]


def get_trails():
    file_name = "data/trails.json"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/9'
    trails = get_arcgis(file_name, url)
    trails['label'] = 'trails'
    return trails[['label', 'geometry']]


def get_regional_pathways():
    file_name = "data/regional_paths.json"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/13'
    routes = get_arcgis(file_name, url)
    routes['label'] = 'regional_pathways'
    return routes[['label', 'geometry']]


def get_protected_bike_lanes():
    file_name = "data/protected_bike_lanes.json"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/15'
    protected_bike_lanes = get_arcgis(file_name, url)
    protected_bike_lanes['label'] = 'protected_bike_lanes'
    return protected_bike_lanes[['label', 'geometry']]


def get_painted_bike_lanes():
    file_name = "data/painted_bike_lanes"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/16'
    painted_bike_lanes = get_arcgis(file_name, url)
    painted_bike_lanes['label'] = 'painted_bike_lanes'
    return painted_bike_lanes[['label', 'geometry']]


def get_bike_routes():
    file_name = "data/bike_routes"
    url = 'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/17'
    bike_routes = get_arcgis(file_name, url)
    bike_routes['label'] = 'bike_routes'
    return bike_routes[['label', 'geometry']]


def load_all_parts():
    file_name = "data/all_parts.json"
    if not os.path.exists(file_name):
        df = gpd.GeoDataFrame(
            concat([get_connectors(), get_regional_pathways(), get_protected_bike_lanes(),
                    get_painted_bike_lanes(), get_bike_routes()], ignore_index=True), crs=get_connectors().crs)
        df = df.simplify(0.001, preserve_topology=True)
        df = connect_paths.connect_paths(df)
        df = df.simplify(0.0001, preserve_topology=True)

        df.to_file(file_name, driver="GeoJSON")

    else:
        df = gpd.read_file(file_name)
    return df


if __name__ == '__main__':
    map_data = load_all_parts()
    '''
    if map == None:
        map = folium.Map(location=[51.0719, -114.048], tiles="Stamen Terrain", zoom_start=12)
        print('map')
    folium.Choropleth(map_data.geometry).add_to(map)
    map.save('unweighted_path_network.html')
    '''
