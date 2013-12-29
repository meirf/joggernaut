__author__ = 'meirfischer'

from polls.models import Node, Edge
import db_graph_2_mem
import graph_algorithms
import sys

elevs = None
adj_list = None

def ensure_set_graph_from_db():
    global elevs, adj_list
    if elevs is None and adj_list is None:
        elevs = db_graph_2_mem.get_elevs()
        adj_list = db_graph_2_mem.get_adjacency_list()

"""If there is no node within distance D1 from A that has
   an elevation in range X or if there is no node within
   distance D1 from A that has an elevation in range Y,
   the user will be notified and told what the max and min
   elevations are within D1 distance from A.
   THIS REACHABILITY IS BADLY SPECIFIED SINCE DIJKSTRA
   MAY INCLUDE IN ITS DISTANCE/PARENTS NODES WITH ELEVATIONS
   OUT OF [X.a,Y.b]
   """
def check_nodes_in_ranges_reachable_within_distance(route_specs):
    ensure_set_graph_from_db()
    (D,P) = graph_algorithms.Dijkstra(adj_list, route_specs.source_node)
    nodes_within_max_distance = [node for node, dist in D.iteritems() if dist<=route_specs.dist_max]
    node_in_X = [node for node in nodes_within_max_distance if route_specs.elev_min_a<=elevs[node]<=route_specs.elev_min_b]
    node_in_Y = [node for node in nodes_within_max_distance if route_specs.elev_max_a<=elevs[node]<=route_specs.elev_max_b]
    if len(node_in_X)==0 or len(node_in_Y)==0:
        elevs_within_D1 = [elevs[node] for node in nodes_within_max_distance]
        raise Exception("Elevation ranges can't be reached. Min elevation/Max elevation within distance "
                        + str(route_specs.dist_max) +" is " + "{0:.2f}".format(min(elevs_within_D1)) +"/"+ "{0:.2f}".format(max(elevs_within_D1)))

#check elev ranges are allowable
def check_inherent_specs(route_specs):
    if route_specs.elev_min_b > route_specs.elev_max_b:
        raise Exception("Fix elevation ranges: " +str(route_specs.elev_min_b) + " is greater than " + str(route_specs.elev_max_b))


"""If there is no node in the pre-computed subsection
   with elevation in range X or there is no node in the
   pre-computed subsection with elevation in range Y,
   the user will be told what the upper limit elevation
   is or what the lower limit elevation is.
   """
def check_node_exists_in_elev_ranges(route_specs):
    elevs = [n.elevation for n in Node.objects.all()]
    elev_message = "\nLowest/Highest elevation in graph: " + "{0:.2f}".format(min(elevs)) +"/"+ "{0:.2f}".format(max(elevs))
    if len(Node.objects.filter(elevation__gte=route_specs.elev_min_a).filter(elevation__lte=route_specs.elev_min_b))==0:
        raise Exception("No node exists with elevation in range: "+
                        str(route_specs.elev_min_a)+" - "+str(route_specs.elev_min_b) + elev_message)
    if len(Node.objects.filter(elevation__gte=route_specs.elev_max_a).filter(elevation__lte=route_specs.elev_max_b))==0:
        raise Exception("No node exists with elevation in range: "+
                        str(route_specs.elev_max_a)+" - "+str(route_specs.elev_max_b) + elev_message)


"""The default value for source node is -1
   Here we check that that value is not as
   default since further algorithms depend
   on it.
   """
def check_source_node_set(route_specs):
    if route_specs.source_node == -1:
        raise Exception("Please choose a starting coordinate from the drop down list")


""" Before we find for each node
    the shortest path distance to node in X
    and shortest path distance to node in Y
    we must ensure that these paths use only
    nodes for which X.a<=node.elev<=Y.b
    This method returns a copy of the graph
    with removal of all nodes whose elevation
    is out of this range and all edges
    that touch these nodes.
    """
def clear_graph_of_nodes_out_of_elev_range(adj_list, elevs, min, max):
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
    nodes_in_range = []
    for node in adj_list:
        if min<=elevs[node]<=max:
            nodes_in_range.append(node)
    return nodes_in_range

""" Given a node, n, cleared graph, G,
    and nodes in X and nodes in Y,
    find shortest distance from n
    to any node in X and any node in Y
    both via G.
    We return a tuple of these two distance
    values. If n has no path to a node in
    X or Y, we return None for that value.
    """
def get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y):
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



def main_route_calculator(route_specs):
    response = {}
    try:
        check_inherent_specs(route_specs)
        check_node_exists_in_elev_ranges(route_specs)
        check_source_node_set(route_specs)
        check_nodes_in_ranges_reachable_within_distance(route_specs)
    except Exception, e:
        response["input_status"] = "BadInput"
        response["response_data"] = e.message
        return response
    ensure_set_graph_from_db()
    response["input_status"] = "???"
    response["response_data"] = "Past checks"
    return response