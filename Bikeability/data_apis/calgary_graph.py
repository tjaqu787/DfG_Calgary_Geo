import osmnx as ox

def calgary_graph():
    city = 'Calgary, Alberta, Canada'
    return ox.graph_from_place(city, network_type='drive')