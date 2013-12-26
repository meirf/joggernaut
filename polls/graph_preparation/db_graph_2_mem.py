__author__ = 'meirfischer'

from collections import defaultdict
from polls.models import Node, Edge

import pdb

def get_elevs():
    elevs = [None] * (len(Node.objects.all()) + 1)
    for node in Node.objects.all():
        elevs[node.node_id] = node.elevation
    return elevs

def get_adjacency_list():
    adj_list = defaultdict(list)
    for edge in Edge.objects.all():
        adj_list[edge.node_a.node_id].append((edge.node_b.node_id, edge.distance))
    return adj_list

if __name__ == "__main__":
    print get_elevs()
    print get_adjacency_list()