__author__ = 'meirfischer'

from django.utils import unittest
import route_processing
import route_specification_data
import graph_algorithms

def get_test_adj_list():
    return  {0: {1: 82.38873277805163, 14: 266.6231251167132},
             1: {0: 82.38873277805163, 2: 85.74109988607606, 15: 268.29573005287796},
             2: {1: 85.74109988607606, 3: 82.75525945633603, 16: 274.61014215408494},
             3: {2: 82.75525945633603, 4: 78.79918085180745, 17: 271.2067618529445},
             4: {3: 78.79918085180745, 5: 79.39718110831093, 18: 279.16827264108787},
             5: {4: 79.39718110831093, 6: 80.71499814230314, 19: 278.8265914161268},
             6: {5: 80.71499814230314, 7: 79.24968891441974, 20: 273.8291663576184},
             7: {6: 79.24968891441974, 8: 78.36168529160078, 21: 276.8164035159303},
             8: {7: 78.36168529160078, 9: 80.81823674182382, 22: 274.80366528576184},
             9: {8: 80.81823674182382, 10: 84.85012947490316, 23: 279.09531381988296},
             10: {9: 84.85012947490316, 11: 87.59503589992097, 24: 277.4400274122313},
             11: {10: 87.59503589992097, 12: 78.36476695195711, 25: 277.95912889056444},
             12: {11: 78.36476695195711, 13: 79.91442656558584, 26: 273.92978777547904},
             13: {12: 79.91442656558584, 27: 270.2504590469046},
             14: {0: 266.6231251167132, 15: 83.55320018178702, 28: 275.7103771339167},
             15: {1: 268.29573005287796,
              14: 83.55320018178702,
              16: 82.33169765631645,
              29: 275.48273926152143},
             16: {2: 274.61014215408494,
              15: 82.33169765631645,
              17: 87.75707520549325,
              30: 275.0299911632324},
             17: {3: 271.2067618529445,
              16: 87.75707520549325,
              18: 76.7854550868973,
              31: 276.5681168710332},
             18: {4: 279.16827264108787,
              17: 76.7854550868973,
              19: 80.64013390170781,
              32: 269.2976240154057},
             19: {5: 278.8265914161268,
              18: 80.64013390170781,
              20: 77.23633249744631,
              33: 272.25074147391814},
             20: {6: 273.8291663576184,
              19: 77.23633249744631,
              21: 82.75989777614281,
              34: 273.1312011919567},
             21: {7: 276.8164035159303,
              20: 82.75989777614281,
              22: 78.4721789510152,
              35: 273.40357644332374},
             22: {8: 274.80366528576184,
              21: 78.4721789510152,
              23: 77.49117699669485,
              36: 281.1142489521684},
             23: {9: 279.09531381988296,
              22: 77.49117699669485,
              24: 83.73570041300154,
              37: 273.40874469166573},
             24: {10: 277.4400274122313,
              23: 83.73570041300154,
              25: 90.41507983919547,
              38: 276.7336570252085},
             25: {11: 277.95912889056444,
              24: 90.41507983919547,
              26: 78.63596570878565,
              39: 272.2665993723394},
             26: {12: 273.92978777547904,
              25: 78.63596570878565,
              27: 78.80740632786181,
              40: 275.51209531976326},
             27: {13: 270.2504590469046, 26: 78.80740632786181, 41: 275.95334862901336},
             28: {14: 275.7103771339167, 29: 88.80841172765727, 43: 314.19888224833},
             29: {15: 275.48273926152143,
              28: 88.80841172765727,
              30: 88.78645959194547,
              44: 316.3345177311764},
             30: {16: 275.0299911632324,
              29: 88.78645959194547,
              31: 77.5722447702176,
              46: 161.1917690486571},
             31: {17: 276.5681168710332,
              30: 77.5722447702176,
              32: 76.34539725943418,
              47: 163.13175206923376},
             32: {18: 269.2976240154057,
              31: 76.34539725943418,
              33: 84.06326774516971,
              48: 162.82099425881336},
             33: {19: 272.25074147391814,
              32: 84.06326774516971,
              34: 78.80356783729334,
              49: 159.8237206773173},
             34: {20: 273.1312011919567,
              33: 78.80356783729334,
              35: 79.52440775499953,
              50: 167.54023086665308},
             35: {21: 273.40357644332374,
              34: 79.52440775499953,
              36: 79.54562731356586,
              52: 309.8653538460924},
             36: {22: 281.1142489521684,
              35: 79.54562731356586,
              37: 76.62584635005591,
              53: 303.0323896040808},
             37: {23: 273.40874469166573,
              36: 76.62584635005591,
              38: 86.0021299090166,
              54: 307.73069095684565},
             38: {24: 276.7336570252085,
              37: 86.0021299090166,
              39: 89.77935386326072,
              55: 307.69951407418944},
             39: {25: 272.2665993723394,
              38: 89.77935386326072,
              40: 78.80810061035706,
              56: 310.5326852386043},
             40: {26: 275.51209531976326, 39: 78.80810061035706, 41: 79.59558353781954},
             41: {27: 275.95334862901336, 40: 79.59558353781954, 58: 81.95105637086372},
             43: {28: 314.19888224833, 44: 83.5418358774016},
             44: {29: 316.3345177311764, 43: 83.5418358774016, 45: 85.90254427471187},
             45: {44: 85.90254427471187, 46: 147.36323553899123},
             46: {30: 161.1917690486571, 45: 147.36323553899123, 47: 75.48730580374043},
             47: {31: 163.13175206923376, 46: 75.48730580374043, 48: 84.84930046977021},
             48: {32: 162.82099425881336, 47: 84.84930046977021, 49: 71.36256461251851},
             49: {33: 159.8237206773173, 48: 71.36256461251851, 50: 82.01010815831104},
             50: {34: 167.54023086665308, 49: 82.01010815831104, 51: 143.32016182543347},
             51: {50: 143.32016182543347, 52: 77.9328812137718},
             52: {35: 309.8653538460924, 51: 77.9328812137718, 53: 80.03723738301903},
             53: {36: 303.0323896040808, 52: 80.03723738301903, 54: 81.17478221142223},
             54: {37: 307.73069095684565, 53: 81.17478221142223, 55: 91.26043445163972},
             55: {38: 307.69951407418944, 54: 91.26043445163972, 56: 83.98753293744298},
             56: {39: 310.5326852386043, 55: 83.98753293744298, 57: 231.5157205933401},
             57: {56: 231.5157205933401, 58: 305.699490911616},
             58: {41: 81.95105637086372, 57: 305.699490911616}}

def get_test_elevs():
    return  [8.772932052612305,
             8.630032539367676,
             8.481337547302246,
             8.473003387451172,
             8.605457305908203,
             8.851371765136719,
             9.326964378356934,
             9.620454788208008,
             10.08272743225098,
             11.16177463531494,
             11.96563720703125,
             12.13568782806396,
             12.42085742950439,
             12.87494850158691,
             8.372590065002441,
             8.12594985961914,
             8.07753849029541,
             8.126249313354492,
             8.17297649383545,
             8.269344329833984,
             8.467561721801758,
             8.599291801452637,
             8.693227767944336,
             9.083831787109375,
             9.349800109863281,
             9.437838554382324,
             9.580528259277344,
             9.914894104003906,
             8.121710777282715,
             7.835072040557861,
             7.691619873046875,
             7.598601818084717,
             7.615684509277344,
             7.728802680969238,
             7.702752113342285,
             7.725890636444092,
             7.606010437011719,
             7.569760322570801,
             7.693739414215088,
             7.730432987213135,
             7.644207000732422,
             7.592205047607422,
             None,
             7.205403804779053,
             7.732362747192383,
             8.290694236755371,
             7.37311649323,
             7.17826652527,
             6.80265760422,
             6.78662490845,
             7.14887714386,
             8.43306159973,
             8.35956192017,
             8.1632232666,
             7.93828582764,
             7.62221002579,
             7.09258747101,
             5.68282175064,
             7.37508964539]

class TestRemovalOfNodesEdgeFromGraphOutOfRange(unittest.TestCase):

    def setUp(self):
        self.adj_list = get_test_adj_list()
        self.elevs = get_test_elevs()
        self.filtered_elevs = [elev for elev in self.elevs if elev is not None]

    def test_all_nodes_out_of_range(self):
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(self.adj_list, self.elevs, max(self.elevs)+1, max(self.elevs)+2)
        self.assertEquals(len(cleared_graph), 0)
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(self.adj_list, self.elevs, min(self.filtered_elevs)-2, min(self.filtered_elevs)-1)
        self.assertEquals(len(cleared_graph), 0)

    def test_all_nodes_in_range(self):
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(self.adj_list, self.elevs, min(self.filtered_elevs)-1, max(self.elevs)+1)
        self.assertEquals(cleared_graph, self.adj_list)

    def test_removal_of_nodes(self):
        a_l = {1:{2:2,3:3}, 8:{9:4}, 7:{8:4}, 12:{8:4} }
        els = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(a_l, els, min, max)
        self.assertEquals(cleared_graph, {8:{9:4}, 7:{8:4}})

    def test_removal_of_edges(self):
        a_l = { 8:{9:4}, 9:{2:4,11:6,7:6}}
        els = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(a_l, els, min, max)
        self.assertEquals(cleared_graph, {8:{9:4}, 9:{7:6}})

    def test_removal_nodes_and_edges(self):
        a_l = {8:{9:4}, 9:{2:4,11:6,7:6}, 3:{1:2,3:4}}
        els = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(a_l, els, min, max)
        self.assertEquals(cleared_graph, {8:{9:4}, 9:{7:6}})


class TestGetNodesInRange(unittest.TestCase):

    def test_no_nodes_in_range(self):
        a_l = {1:{}, 3:{},4:{}, 11:{},12:{}}
        els = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        nodes = route_processing.get_node_ids_in_range(a_l, els, min, max)
        self.assertEquals(nodes, [])

    def test_all_nodes_in_range(self):
        a_l = {5:{},6:{},7:{},8:{},9:{},10:{}}
        els = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        nodes = route_processing.get_node_ids_in_range(a_l, els, min, max)
        self.assertEquals(nodes, a_l.keys())

    def test_some_nodes_in_range(self):
        a_l = {4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{}}
        els = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        min = 5
        max = 10
        nodes = route_processing.get_node_ids_in_range(a_l, els, min, max)
        self.assertEquals(nodes, range(5,11))

class TestShortestDistancetoNodesinXY(unittest.TestCase):

    def test_no_nodes_in_either_X_Y_reachable(self):
        node_id = 0
        cleared_graph = {0:{10:4}, 10:{9:1}, 9:{10:1}}
        nodes_in_X = [1,2,3]
        nodes_in_Y = [4,5,6]
        (dist_2_X, dist_2_Y)=route_processing.get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y)
        self.assertEquals((dist_2_X, dist_2_Y),(None, None))

    def test_node_is_in_X_or_Y_so_dist_is_zero(self):
        node_id = 0
        cleared_graph = {0:{1:4}, 1:{0:1}}
        nodes_in_X = [0,1,2,3]
        nodes_in_Y = [4,5,6]
        (dist_2_X, dist_2_Y)=route_processing.get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y)
        self.assertEquals((dist_2_X, dist_2_Y),(0, None))
        node_id = 0
        cleared_graph = {0:{6:4}, 6:{0:1}}
        nodes_in_X = [1,2,3]
        nodes_in_Y = [0,4,5,6]
        (dist_2_X, dist_2_Y)=route_processing.get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y)
        self.assertEquals((dist_2_X, dist_2_Y),(None, 0))

    def test_node_in_X_reachable(self):
        node_id = 0
        cleared_graph = {0:{1:4}, 1:{0:1}}
        nodes_in_X = [1,2,3]
        nodes_in_Y = [4,5,6]
        (dist_2_X, dist_2_Y)=route_processing.get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y)
        self.assertEquals((dist_2_X, dist_2_Y),(4, None))

    def test_node_in_Y_reachable(self):
        node_id = 0
        cleared_graph = {0:{5:9}, 5:{0:8}}
        nodes_in_X = [1,2,3]
        nodes_in_Y = [4,5,6]
        (dist_2_X, dist_2_Y)=route_processing.get_shortest_distance_to_X_Y(node_id, cleared_graph, nodes_in_X, nodes_in_Y)
        self.assertEquals((dist_2_X, dist_2_Y),(None, 9))


class TestGatherAllClosestDistanceValues(unittest.TestCase):

    def test_values_for_all_nodes_equal_weighted_loop(self):
        cleared_graph = {0:{1:1,2:1}, 1:{2:1,0:1}, 2:{0:1,1:1}}
        elevs = [7, 15, 25]
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 5, 10, 20, 30)
        distances = route_processing.compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs)
        self.assertEquals(distances, {0:(0,1),1:(1,1),2:(1,0)})

    def test_values_for_all_nodes_unequal_weighted_loop(self):
        cleared_graph = {0:{1:1,2:2}, 1:{2:1,0:4}, 2:{0:2,1:1}}
        elevs = [7, 15, 25]
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 5, 10, 20, 30)
        distances = route_processing.compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs)
        self.assertEquals(distances, {0:(0,2),1:(3,1),2:(2,0)})

    def test_some_none_distances(self):
        cleared_graph = {0:{1:1,2:2}, 1:{2:1,0:4}, 2:{0:2,1:1}}
        elevs = [7, 15, 18]
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 5, 10, 20, 30)
        distances = route_processing.compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs)
        self.assertEquals(distances, {0:(0,None),1:(3,None),2:(2,None)})

    def test_all_none_distances(self):
        cleared_graph = {0:{1:1,2:2}, 1:{2:1,0:4}, 2:{0:2,1:1}}
        elevs = [12, 15, 18]
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 5, 10, 20, 30)
        distances = route_processing.compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs)
        self.assertEquals(distances, {0:(None,None),1:(None,None),2:(None,None)})

class TestNodeViability(unittest.TestCase):

    def test_criteria_a(self):
        node = 1
        running_distance= 10
        dist_max = 20
        path = [0]
        cleared_graph = {0:{1:20}}
        seen_X = False
        seen_Y = False
        closest_distances = {}
        viability =  graph_algorithms.is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances)
        self.assertEquals(viability, False)

    def test_criteria_b(self):
        node = 1
        running_distance= 10
        dist_max = 20
        path = [0]
        cleared_graph = {0:{1:5}}
        seen_X = False
        seen_Y = False
        closest_distances = {1:(None, None)}
        viability =  graph_algorithms.is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances)
        self.assertEquals(viability, False)

    def test_criteria_c(self):
        node = 1
        running_distance= 10
        dist_max = 20
        path = [1,0]
        cleared_graph = {0:{1:5}}
        seen_X = False
        seen_Y = False
        closest_distances = {1:(5, 5)}
        viability =  graph_algorithms.is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances)
        self.assertEquals(viability, False)

    def test_sat_all_criteria(self):
        node = 1
        running_distance= 10
        dist_max = 20
        path = [0]
        cleared_graph = {0:{1:5}}
        seen_X = False
        seen_Y = False
        closest_distances = {1:(5, 5)}
        viability =  graph_algorithms.is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances)
        self.assertEquals(viability, True)

class TestRandomWalk(unittest.TestCase):

    def test_no_path(self):
        cleared_graph = {0:{}}
        source_node = 0
        closest_distances = {0: (None, None)}
        dist_min = 10
        dist_max = 30
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(path, None)
        cleared_graph = {0:{1:5}, 1:{0:5}}
        source_node = 0
        closest_distances = {0: (5, 5), 1: (0,0)}
        dist_min = 10
        dist_max = 30
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(path, None)

    def test_path_length_one(self):
        cleared_graph = {0:{1:5}, 1:{0:5}}
        source_node = 0
        closest_distances = {0: (0, 0), 1: (0,0)}
        dist_min = 0
        dist_max = 3
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(len(path), 1)

    def test_path_length_few(self):
        cleared_graph = {0:{1:1}, 1:{2:1}, 2:{0:1}}
        source_node = 0
        closest_distances = {0: (2, 2), 1: (1, 1), 2:(0,0)}
        dist_min = 2
        dist_max = 2
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(len(path), 3)

if __name__ == "__main__":
    unittest.main()