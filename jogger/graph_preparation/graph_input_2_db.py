__author__ = 'meirfischer'

from parse_kml_ids_with_coords import get_adj_list, get_all_elevations, get_coordinates
from jogger.models import Node, Edge

def create_graph(coords, elevs, adj_list):
    #create_nodes
    nodes = []
    for i in xrange(len(coords)):
        if coords[i] is not None:
            n = Node(node_id=i, latit=coords[i][1], longit=coords[i][0], elevation=elevs[i])
            nodes.append(n)
            n.save()
        else:
            nodes.append(None)
    #create_edges
    for k,v in adj_list.items():
        for edge_dist in v:
            e = Edge(node_a=nodes[k], node_b=nodes[edge_dist[0]], distance=edge_dist[1])
            e.save()

def load_into_db():
    coords = get_coordinates()
    elevs = get_all_elevations()
    adj_list = get_adj_list()
    create_graph(coords, elevs, adj_list)

if __name__ == "__main__":
    load_into_db()