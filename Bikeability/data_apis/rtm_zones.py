import geopandas as gpd
from sodapy import Socrata
from shapely import geometry

def get_rtm_zones():
    #get data and assign to geodataframe
    client = Socrata('data.calgary.ca', None)
    data = client.get('izjs-4mru', limit=2000)
    gdf = gpd.GeoDataFrame(data)
    
    #build shapely polygons from coordinates
    gdf['geometry'] = [geometry.Polygon(gdf['polygon'][i]['coordinates'][0]) for i in range(len(gdf['polygon']))]
    gdf.drop(columns='polygon', inplace=True)
    
    #set coordiante reference system
    gdf.set_crs(epsg=4326, inplace=True)
    
    return gdf