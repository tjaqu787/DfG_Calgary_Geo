# Takes as arguments:
# graph dataset, origin & target points (shapely.Point format), field to use as weight
# finds nearest nodes to target & origin points, calculates shortest distance
# requires scipy and scikit-learn to be installed in environment (no need to import)

import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, Point

def route_from_points(graph, origin_point, target_point, weight_field):

    # define gdf for graph's nodes
    nodes = ox.graph_to_gdfs(graph, nodes=True, edges=False)

    # assign xy values for origin and target points to tuples
    origin_xy = (origin_point.x, origin_point.y)
    target_xy = (target_point.x, target_point.y)

    # identify nearest nodes
    origin_node = ox.distance.nearest_nodes(graph, origin_xy[0], origin_xy[1])
    target_node = ox.distance.nearest_nodes(graph, target_xy[0], target_xy[1])

    # returns list of nodes along shortest path between input points
    route_ids = nx.shortest_path(G=graph, source=origin_node, target=target_node, weight=weight_field)

    route_gdf = nodes.loc[route_ids]

    return LineString(list(route_gdf.geometry.values)) #return route LineString
