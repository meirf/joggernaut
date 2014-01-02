import sys
import math
from collections import defaultdict

from jogger.models import Node
import db_graph_2_mem
import graph_algorithms


def is_inherent_specs_consitent(route_specs):
    """
    Check elevation ranges are intrinsically logical
    """
    if int(route_specs.elev_min_b) > int(route_specs.elev_max_b):
        return False
    return True


def is_node_exists_in_elev_ranges(min, max):
    """
    Determines if there is a node in the with elevation in
    the specified range.
    """
    if len(Node.objects.filter(elevation__gte=min).filter(elevation__lte=max))==0:
        return False
    return True


def is_source_node_set(route_specs):
    """
    The default value for source node is -1
    Here we check whether that value is not as
    default.
    """
    if route_specs.source_node == -1:
        return False
    return True


def clear_out_range(adj_list, elevs, min, max):
    """
    Before we find for each node
    the shortest path distance to node in X
    and shortest path distance to node in Y
    we must ensure that these paths use only
    nodes for which X.a<=node.elev<=Y.b
    This method returns a copy of the graph
    with removal of all nodes whose elevation
    is out of this range and all edges
    that touch these nodes.
    """
    graph_copy = adj_list.copy()
    for node_id, edges in graph_copy.items():
        if elevs[node_id]>max or elevs[node_id]<min:
            del graph_copy[node_id]
        else:
            for neighbor in edges.keys():
                if elevs[neighbor]>max or elevs[neighbor]<min:
                    del graph_copy[node_id][neighbor]
    return graph_copy


def get_node_ids_in_range(adj_list, elevs, min, max):
    """
    Returns nodes with elevations in specified range
    """
    return [node for node in adj_list if min<=elevs[node]<=max]


def get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y):
    """
    Given a node, n, cleared graph, G,
    and nodes in X and nodes in Y,
    find shortest distance from n
    to any node in X and any node in Y
    both via G.
    We return a tuple of these two distance
    values. If n has no path to a node in
    X or Y, we return None for that value.
    """
    (D,P) = graph_algorithms.Dijkstra(cleared_graph,node_id)
    shortest_to_X = sys.maxint
    for node in nodes_in_X:
        if node in D and D[node]<shortest_to_X:
            shortest_to_X = D[node]
    shortest_to_Y = sys.maxint
    for node in nodes_in_Y:
        if node in D and D[node]<shortest_to_Y:
            shortest_to_Y = D[node]
    return (None if shortest_to_X==sys.maxint else shortest_to_X,
            None if shortest_to_Y==sys.maxint else shortest_to_Y)


def compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs):
    """
    Given G', and route specs, R
    We compute a dictionary of tuples:
        node_id -> (closest distance to node in X, closest distance to node in Y)
    """
    closest_distances = defaultdict(tuple)
    nodes_in_X = get_node_ids_in_range(cleared_graph, elevs, route_specs.elev_min_a, route_specs.elev_min_b)
    nodes_in_Y = get_node_ids_in_range(cleared_graph, elevs, route_specs.elev_max_a, route_specs.elev_max_b)
    for node in cleared_graph:
        closest_distances[node] = get_shortest_distance_to_X_Y(node,cleared_graph,nodes_in_X, nodes_in_Y)
    return closest_distances


def get_min(l):
    none_clear = [val for val in l if val is not None]
    if len(none_clear)>0:
        return min(none_clear)
    return -1


def get_max(l):
    if len(l)>0:
        return max(l)
    return -1


def hav_dist(lat1, lon1, lat2, lon2):
    """
    http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
    """
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d * 1000


def main_route_calculator(route_specs):
    response = {"warning" : "okay"}
    elevs = db_graph_2_mem.get_elevs()
    adj_list = db_graph_2_mem.get_adjacency_list()
    coords = db_graph_2_mem.get_coords()

    if is_inherent_specs_consitent(route_specs) is False:
        response["warning"] = "Fix elevation ranges: " \
                              +str(route_specs.elev_min_b) + " is greater than " + str(route_specs.elev_max_b)
        return response

    if is_node_exists_in_elev_ranges(route_specs.elev_min_a, route_specs.elev_min_b) is False:
        response["warning"] = "No node exists with " \
                              "elevation in range: " + str(route_specs.elev_min_a)+" - "+str(route_specs.elev_min_b)
        return response

    if is_node_exists_in_elev_ranges(route_specs.elev_max_a, route_specs.elev_max_b) is False:
        response["warning"] = "No node exists with " \
                              "elevation in range: " + str(route_specs.elev_max_a)+" - "+str(route_specs.elev_max_b)
        return response

    if is_source_node_set(route_specs) is False:
        response["warning"] = "Please choose a coordinate from the drop down list"
        return response

    # THIS REACHABILITY IS BADLY SPECIFIED SINCE DIJKSTRA
    # MAY INCLUDE IN ITS DISTANCE/PARENTS NODES WITH ELEVATIONS
    # OUT OF [X.a,Y.b]
    (D,P) = graph_algorithms.Dijkstra(adj_list, route_specs.source_node)
    nodes_in_dist = [node for node, dist in D.iteritems() if dist<=route_specs.dist_max]
    node_in_X = [node for node in nodes_in_dist if route_specs.elev_min_a<=elevs[node]<=route_specs.elev_min_b]
    node_in_Y = [node for node in nodes_in_dist if route_specs.elev_max_a<=elevs[node]<=route_specs.elev_max_b]
    if len(node_in_X)==0 or len(node_in_Y)==0:
        elevs_within_D1 = [elevs[node] for node in nodes_in_dist]
        response["warning"] = "Elevation ranges can't be reached. " \
                              "Min elevation/Max elevation within distance " + str(route_specs.dist_max) + \
                              "{0:.2f}".format(min(elevs_within_D1)) +"/"+ "{0:.2f}".format(max(elevs_within_D1))
        return response

    route_data = graph_algorithms.random_walk_wrapper(adj_list, route_specs.source_node, elevs, route_specs,
                                                      num_of_ranges=20, paths_per_range=50, coords=coords)
    response['route_data'] = route_data
    return response