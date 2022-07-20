# By Richard 2022-07-19
# finds nearest nodes to target & origin points, calculates shortest distance between them
import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, Point


def route_from_points(graph, origin_point, target_point, weight_field=None):
    """
    Finds the shortest path between two points in a graph.
    :param graph: Graph of linestrings
    :param origin_point: Start point in shapely.geometry.Point format
    :param target_point: Finish point in shapely.geometry.Point format
    :param weight_field: How to weight each linestring
    :return: return route LineString
    """
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

    return LineString(list(route_gdf.geometry.values))  # return route LineString
