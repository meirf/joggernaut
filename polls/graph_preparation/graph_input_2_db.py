__author__ = 'meirfischer'

from parse_kml_ids_with_coords import get_adj_list, get_all_elevations, get_coordinates
from polls.models import Node, Edge

def create_nodes(coords, elevs):
    for i in xrange(len(coords)):
        if coords[i] is not None:
            n = Node(node_id=i, latit=coords[i][1], longit=coords[i][0], elevation=elevs[i])
            n.save()

def create_edges(adj_list):
    for k,v in adj_list.items():
        for edge_dist in v:
            e = Edge(node_id_a=k, node_id_b=edge_dist[0], distance=edge_dist[1])
            e.save()

def load_into_db():
    coords = get_coordinates()
    elevs = get_all_elevations()
    create_nodes(coords, elevs)

    adj_list = get_adj_list()
    create_edges(adj_list)

if __name__ == "__main__":
    load_into_db()