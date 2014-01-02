__author__ = 'meirfischer'

from django.utils import unittest
from graph_preparation import route_processing
from graph_preparation import route_specification_data
from graph_preparation import graph_algorithms

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

def get_test_coords():
    return  [(40.81085348983534, -73.95069122314453),
             (40.81020385883746, -73.95116329193115),
             (40.80953798046392, -73.95167827606201),
             (40.80888021599794, -73.95213961601257),
             (40.808263048347875, -73.95260095596313),
             (40.80765399544973, -73.95309448504122),
             (40.80700433337586, -73.95352363586426),
             (40.806387148279185, -73.95399570465088),
             (40.80576995744257, -73.95444631576538),
             (40.80513651877329, -73.954918384552),
             (40.80447058967455, -73.95541191101074),
             (40.803772168734845, -73.95589470863342),
             (40.80315495364101, -73.95634531974792),
             (40.80251336864485, -73.95677447384514),
             (40.80968414921198, -73.94792318344116),
             (40.809018265623074, -73.94838452339172),
             (40.808352375352044, -73.9488136768341),
             (40.80767023692629, -73.94933938980103),
             (40.80703681651909, -73.94970417022705),
             (40.80641963184845, -73.95020842552185),
             (40.80581868324361, -73.95066976547241),
             (40.80516088191082, -73.95113110542297),
             (40.804551800789206, -73.9516031742096),
             (40.80392647167342, -73.95201086997986),
             (40.803276772860904, -73.95251512527466),
             (40.802553975474005, -73.95300865238823),
             (40.80195299186528, -73.95350217884697),
             (40.80133575979199, -73.95396351879754),
             (40.80852290911068, -73.94502639770508),
             (40.80781641053205, -73.94551992416382),
             (40.807101783377405, -73.94599199295044),
             (40.8064927198211, -73.94644260406494),
             (40.80589177187812, -73.94688248634338),
             (40.805233971269786, -73.94737601280212),
             (40.80461676967753, -73.94783735406236),
             (40.803983320038206, -73.9482772363408),
             (40.80333362165247, -73.94867420196533),
             (40.80274888815603, -73.94915699958801),
             (40.80206669188431, -73.94963979786553),
             (40.80136824583369, -73.95017623966851),
             (40.80075100832267, -73.95063757961907),
             (40.80012564341188, -73.95109891956963),
             None,
             (40.807101783129575, -73.94179701805115),
             (40.806427752738266, -73.94223690032959),
             (40.80576995744257, -73.94277334213257),
             (40.80639526917302, -73.94431829583482),
             (40.805794320347566, -73.94473672044114),
             (40.80512839772544, -73.94523024689988),
             (40.80458428500896, -73.94568085801438),
             (40.80391022929611, -73.94607782494859),
             (40.80324428776881, -73.94461870193481),
             (40.80262706770392, -73.94505858421326),
             (40.802001720468716, -73.94553065299988),
             (40.801360124324766, -73.94599199295044),
             (40.800637307041264, -73.9465069770813),
             (40.799971332674865, -73.94697904586792),
             (40.7981520505767, -73.9483201510302),
             (40.79945966391186, -73.95151734417595)]

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

    """
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
        """

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

    """
    def test_no_path(self):
        cleared_graph = {0:{}}
        source_node = 0
        closest_distances = {0: (None, None)}
        dist_min = 10
        dist_max = 30
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(path, (None, None))
        cleared_graph = {0:{1:5}, 1:{0:5}}
        source_node = 0
        closest_distances = {0: (5, 5), 1: (0,0)}
        dist_min = 10
        dist_max = 30
        path = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(path, (None, None))
    """

    def test_path_length_one(self):
        cleared_graph = {0:{1:5}, 1:{0:5}}
        source_node = 0
        closest_distances = {0: (0, 0), 1: (0,0)}
        dist_min = 0
        dist_max = 3
        (path, dist) = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(len(path), 1)

    def test_path_length_few(self):
        cleared_graph = {0:{1:1}, 1:{2:1}, 2:{0:1}}
        source_node = 0
        closest_distances = {0: (2, 2), 1: (1, 1), 2:(0,0)}
        dist_min = 2
        dist_max = 2
        (path, dist) = graph_algorithms.random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max)
        self.assertEquals(len(path), 3)

class TestRanges(unittest.TestCase):

    def test_ranges(self):
        min_dist = 1
        max_dist = 10
        ranges = graph_algorithms.get_ranges(min_dist, max_dist)
        self.assertEquals(ranges, [{"min":1, "max":10,'paths':[], 'distances':[]}])
        min_dist = 2
        max_dist = 10
        ranges = graph_algorithms.get_ranges(min_dist, max_dist, 5)
        self.assertEquals(ranges, [{"min":2, "max":4, 'paths':[], 'distances':[]},{"min":4, "max":6, 'paths':[], 'distances':[]},{"min":6, "max":8, 'paths':[], 'distances':[]},{"min":8, "max":10, 'paths':[], 'distances':[]}])

class TestRandomWalkWithRangesMultiplicity(unittest.TestCase):

    def test_using_multiplepaths(self):
        source_node = 0
        dist_min = 3
        dist_max = 3
        elev_min_a = 20
        elev_min_b = 30
        elev_max_a = 50
        elev_max_b = 60
        un_cleared_graph = {0:{1:1}, 1:{2:1}, 2:{3:1}, 3:{0:1}}
        elevs = [40, 40, 25, 55]
        route_specs = route_specification_data.RouteSpecs(source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b)
        route_data = graph_algorithms.random_walk_wrapper(un_cleared_graph, source_node, elevs, route_specs, 2, 2)
        expected = [  {   'min': 3,
                          'max': 3,
                          'paths': [
                                     [0, 1, 2, 3]
                                    ],
                          'distances': [3]
                        }
                      ]
        self.assertEquals(route_data, expected)
        source_node = 0
        dist_min = 2
        dist_max = 4
        elev_min_a = 20
        elev_min_b = 30
        elev_max_a = 50
        elev_max_b = 60
        un_cleared_graph = {0:{1:1}, 1:{2:1}, 2:{3:1}, 3:{0:1}}
        elevs = [40, 40, 25, 55]
        route_specs = route_specification_data.RouteSpecs(source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b)
        route_data = graph_algorithms.random_walk_wrapper(un_cleared_graph, source_node, elevs, route_specs, 3, 1)
        expected = [  {   'min': 2,
                          'max': 3,
                          'paths': [
                                     [0, 1, 2, 3]
                                    ],
                          'distances': [3]
                      },
                      {   'min': 3,
                          'max': 4,
                          'paths': [
                                     [0, 1, 2, 3, 0]
                                    ],
                          'distances': [4]
                      }
                   ]
        self.assertEquals(route_data, expected)

    def test_getting_coords_not_node_ids(self):
        self.maxDiff = None
        coords = [(1,2),(3,4),(5,6),(7,8)]
        source_node = 0
        dist_min = 2
        dist_max = 4
        elev_min_a = 20
        elev_min_b = 30
        elev_max_a = 50
        elev_max_b = 60
        un_cleared_graph = {0:{1:1}, 1:{2:1}, 2:{3:1}, 3:{0:1}}
        elevs = [40, 40, 25, 55]
        route_specs = route_specification_data.RouteSpecs(source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b)
        route_data = graph_algorithms.random_walk_wrapper(un_cleared_graph, source_node, elevs, route_specs, 3, 1, coords)
        expected = [  {   'min': 2,
                          'max': 3,
                          'paths': [
                                     [{'lat': 1, 'long': 2, 'node_id':0}, {'lat': 3, 'long': 4, 'node_id':1}, {'lat': 5, 'long': 6, 'node_id':2},{'lat': 7, 'long': 8, 'node_id':3}]
                                    ],
                          'distances': [3]
                        },
                        { 'min': 3,
                          'max': 4,
                          'paths': [
                                     [{'lat': 1, 'long': 2, 'node_id':0}, {'lat': 3, 'long': 4, 'node_id':1}, {'lat': 5, 'long': 6, 'node_id':2},{'lat': 7, 'long': 8, 'node_id':3}, {'lat': 1, 'long': 2, 'node_id':0}]
                                    ],
                          'distances': [4]
                        }
                      ]
        self.assertEquals(route_data, expected)


class TestAllRouteSpecsSatAFTER(unittest.TestCase):

    def setUp(self):
        self.adj_list = get_test_adj_list()
        self.coords = get_test_coords()
        self.elevs = get_test_elevs()

    def test_distance_correct(self):
        """
        In the response data, calculate that
        every path's coords add up to
        the distance value for that path
        """
        source_node = 0
        dist_min = 1200
        dist_max = 2000
        elev_min_a = 7
        elev_min_b = 15
        elev_max_a = 12
        elev_max_b = 17
        route_specs = route_specification_data.RouteSpecs(source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b)
        route_data = graph_algorithms.random_walk_wrapper(self.adj_list, route_specs.source_node, self.elevs, route_specs, number_of_ranges=20, paths_per_range=50, coords=self.coords)
        for r in route_data:
            for i,path in enumerate(r['paths']):
                path_dist = 0
                for coord_pair_ind in range(0,len(path)-1):
                    pair_a = path[coord_pair_ind]
                    pair_b = path[coord_pair_ind+1]
                    path_dist+=route_processing.hav_dist(pair_a['lat'],pair_a['long'],pair_b['lat'],pair_b['long'])
                self.assertTrue(abs(path_dist-r['distances'][i])<10)

    def test_elevation_sat(self):
        """
        For every path in response,
        test that there is >=1 node in X
        and  that there is >=1 node in Y
        """
        source_node = 0
        dist_min = 1200
        dist_max = 2000
        elev_min_a = 7
        elev_min_b = 25
        elev_max_a = 10
        elev_max_b = 50
        route_specs = route_specification_data.RouteSpecs(source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b)
        route_data = graph_algorithms.random_walk_wrapper(self.adj_list, route_specs.source_node, self.elevs, route_specs, number_of_ranges=20, paths_per_range=50, coords=self.coords)
        for r in route_data:
            for path in r['paths']:
                x_count = 0
                y_count = 0
                for node in path:
                    x_count += 1 if route_specs.elev_min_a<=self.elevs[node['node_id']]<=route_specs.elev_min_b else 0
                    y_count += 1 if route_specs.elev_max_a<=self.elevs[node['node_id']]<=route_specs.elev_max_b else 0
                self.assertTrue(x_count>0)
                self.assertTrue(y_count>0)


class TestSatCriteriaC(unittest.TestCase):

    def test_one_node_in_path(self):
        path = [0]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, True)

    def test_two_nodes_in_path(self):
        path = [0, 1]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, True)

    def test_many_nodes_in_path(self):
        path = [0, 1, 2, 0, 4]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, True)
        path = [0, 1, 2, 0, 2]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, False)
        path = [0, 1, 2, 0, 4]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, True)
        path = [0, 2, 0]
        sat = graph_algorithms.satisfies_criteria_c(path)
        self.assertEquals(sat, False)


class TestMinPriorMax(unittest.TestCase):

    def test_node_in_x_before_node_in_y(self):
        path  = [2,7]
        elevs = [6,7,8,9,10,11,12,13,14]
               # 0 1 2 3  4  5  6  7  8
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 7, 10, 12, 15)
        sat = graph_algorithms.has_x_before_y(path, elevs, route_specs)
        self.assertEquals(sat, True)

    def test_no_node_in_x(self):
        path  = [0,7]
        elevs = [6,7,8,9,10,11,12,13,14]
               # 0 1 2 3  4  5  6  7  8
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 7, 10, 12, 15)
        sat = graph_algorithms.has_x_before_y(path, elevs, route_specs)
        self.assertEquals(sat, False)

    def test_no_node_in_y(self):
        path  = [1,4]
        elevs = [6,7,8,9,10,11,12,13,14]
               # 0 1 2 3  4  5  6  7  8
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 7, 10, 12, 15)
        sat = graph_algorithms.has_x_before_y(path, elevs, route_specs)
        self.assertEquals(sat, False)

    def test_y_before_x(self):
        path  = [7,3]
        elevs = [6,7,8,9,10,11,12,13,14]
               # 0 1 2 3  4  5  6  7  8
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 7, 10, 12, 15)
        sat = graph_algorithms.has_x_before_y(path, elevs, route_specs)
        self.assertEquals(sat, False)

    def test_y_same_as_x(self):
        path  = [6]
        elevs = [6,7,8,9,10,11,12,13,14]
               # 0 1 2 3  4  5  6  7  8
        route_specs = route_specification_data.RouteSpecs(0, 100, 200, 7, 12, 12, 15)
        sat = graph_algorithms.has_x_before_y(path, elevs, route_specs)
        self.assertEquals(sat, True)

if __name__ == "__main__":
    unittest.main()

















