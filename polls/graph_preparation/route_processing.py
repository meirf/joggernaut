__author__ = 'meirfischer'

from polls.models import Node, Edge
import db_graph_2_mem
import graph_algorithms

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
   """
def check_nodes_in_ranges_reachable_within_distance(route_specs):
    ensure_set_graph_from_db()
    (D,P) = graph_algorithms.Dijkstra(adj_list, route_specs.source_node)
    return D
    # node within distance with elev in X
    # node_ids = filter(lambda x, D.values())
    # node within distance with elev in Y
    # len(filter(,D.values()))>0

#check elev ranges are allowable
def check_inherent_specs(route_specs):
    if route_specs.elev_min_b > route_specs.elev_max_b:
        raise Exception(str(route_specs.elev_min_b) + " is greater than " + str(route_specs.elev_max_b))


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

def main_route_calculator(route_specs):
    response = {};
    try:
        check_inherent_specs(route_specs)
        check_node_exists_in_elev_ranges(route_specs)
        check_source_node_set(route_specs)
    except Exception, e:
        response["input_status"] = "BadInput"
        response["response_data"] = e.message
        return response
    response["input_status"] = "ActionableInput"
    response["response_data"] = str(check_nodes_in_ranges_reachable_within_distance(route_specs))
    return response