import connectors
import connect_paths
import parse_dangerous_routes
import City_Of_Calgary_ARCGIS_Rest_API




def unweighted_path_network():
    '''

    :return: City of calgary pathway network merged unweighted.
    '''
    # get data from City of Calgary
    x = City_Of_Calgary_ARCGIS_Rest_API.get_protected_bike_lanes()
    y = City_Of_Calgary_ARCGIS_Rest_API.get_regional_pathways()
    z = City_Of_Calgary_ARCGIS_Rest_API.get_bike_routes()
    w = City_Of_Calgary_ARCGIS_Rest_API.get_painted_bike_lanes()
    v = connectors.get_connectors()

    #merge data
    paths = x.overlay(y, how='union').overlay(z, how='union').overlay(w, how='union').overlay(v, how='union')
    # simplify geometry
    paths = paths.simplify(tolerance=0.003)
    paths = connect_paths.connect_paths(paths)
    return paths


if __name__ == '__main__':
    map_data = unweighted_path_network()
    if map == None:
        map = folium.Map(location=[51.0719, -114.048], tiles="Stamen Terrain", zoom_start=12)
        print('map')
    folium.Choropleth(df.geometry,fill_color=colour,line_color=colour).add_to(map)
    return map