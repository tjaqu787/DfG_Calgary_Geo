import geopandas as gpd
from sodapy import Socrata
from shapely import geometry



def get_rtm_zones():
    epsg = 4326
    endpoint = '4c3g-8je3'
    #get data and assign to geodataframe
    client = Socrata('data.calgary.ca', None)
    data = client.get(endpoint, limit=2000)
    rtm_zones = gpd.GeoDataFrame(data)
    
    #build shapely polygons from coordinates
    rtm_zones['geometry'] = [geometry.Polygon(rtm_zones['the_geom'][i]['coordinates'][0]) for i in range(len(rtm_zones['the_geom']))]
    rtm_zones.drop(columns='the_geom', inplace=True)
    
    #set coordiante reference system
    rtm_zones.set_crs(epsg=epsg, inplace=True)
    
    #return filtered values, City of Calgary only
    return rtm_zones[rtm_zones['region']=='0']


