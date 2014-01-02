

class RouteSpecs:
    """
    Data container for any specification sent by user.
    Currently only holds data, but may include
    functionality in the future.
    """

    def __init__(self, source_node, dist_min, dist_max, elev_min_a,elev_min_b, elev_max_a, elev_max_b):
        self.source_node = source_node
        self.dist_min = dist_min
        self.dist_max = dist_max
        self.elev_min_a = elev_min_a
        self.elev_min_b = elev_min_b
        self.elev_max_a = elev_max_a
        self.elev_max_b = elev_max_b