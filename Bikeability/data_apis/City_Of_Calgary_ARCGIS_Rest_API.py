import esri2gpd
import geopandas as gpd


def get_roads():
    roads = gpd.GeoDataFrame(esri2gpd.get(
        'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/RoadClassification/MapServer/0'))
    return roads


def get_regional_pathways():
    regional_pathways = esri2gpd.get(
        f'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/13')
    return regional_pathways


def get_protected_bike_lanes():
    protected_bike_lanes = esri2gpd.get(
        'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/15')
    return protected_bike_lanes


def get_painted_bike_lanes():
    painted_bike_lanes = esri2gpd.get(
        'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/16')
    return painted_bike_lanes


def get_bike_routes():
    bike_routes = esri2gpd.get(
        'https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/ParksPathwayBikeWay/MapServer/17')
    return bike_routes


if __name__ == '__main__':
    x = get_protected_bike_lanes()
    y = get_regional_pathways()
    z = get_bike_routes()
    w = get_painted_bike_lanes()

    x.to_file("x.json", driver="GeoJSON")
    y.to_file("y.json", driver="GeoJSON")
    z.to_file("z.json", driver="GeoJSON")
    w.to_file("w.json", driver="GeoJSON")
    print()
