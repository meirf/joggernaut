__author__ = 'meirfischer'

from collections import defaultdict
from polls.models import Node, Edge

def get_elevs():
    elevs = [None] * (len(Node.objects.all()) + 1)
    for node in Node.objects.all():
        elevs[node.node_id] = node.elevation
    return elevs

"""Not identical to original adjacency list
   use in graph_input_2_db.py, which was
        dictionary mapping each node id to a list,
            each element of which was a 2-tuple
                composed of node id neighbor and distance to that neighbor

   THIS graph representation is as follows:
        dictionary mapping each node id to a dict,
            each key of this sub-dict is a neighbor node id
            the value at each key is the distance to that neighbor

    """
def get_adjacency_list():
    adj_list = defaultdict(dict)
    for edge in Edge.objects.all():
        adj_list[edge.node_a.node_id][edge.node_b.node_id] = edge.distance
    return adj_list

def get_coords():
    elevs = [None] * (len(Node.objects.all()) + 1)
    for node in Node.objects.all():
        elevs[node.node_id] = (node.latit, node.longit)
    return elevs