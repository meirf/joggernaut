from __future__ import generators

import random
import route_processing
import numpy
from collections import defaultdict

""" Clears graph of nodes outside of [X.a, Y.b]
    Gets closest distances for all nodes to nodes in X and Y
    Calls random walk with this data:
        Splits up [X.a,Y.b] into R ranges.
        For each range in R, gets up to P paths.
            If get None as a result advance an iteration and
            don't include that in the result.

    We return a list of ranges
        where each range is a tuple of the form (min_dist, max_dist)
    and a dictionary
        where each key is tuple range and each value
        is a set of tuples, each of which is a tupled list of nodes
        (Note: to convert this dict's values to coords, use "get_coords_version_of_path"
        and tuple the result)
    """
def random_walk_wrapper(un_cleared_graph, source_node, elevs, route_specs, number_of_ranges=2, paths_per_range=1, coords=None):
    cleared_graph = route_processing.clear_graph_of_nodes_out_of_elev_range(un_cleared_graph, elevs, route_specs.elev_min_a, route_specs.elev_max_b)
    closest_distances = route_processing.compute_closest_distance_values_at_each_node(cleared_graph, elevs, route_specs)
    ranges = get_ranges(route_specs.dist_min, route_specs.dist_max, number_of_ranges)
    routes = defaultdict(set)
    distances = defaultdict(int)
    for r in ranges:
        for count in range(paths_per_range):#iterate paths_per_range times
            (path,running_distance) = random_walk(cleared_graph, source_node, closest_distances, r[0], r[1])
            if path is not None:
                if coords is None:
                    routes[r].add(tuple(path))
                    distances[tuple(path)] = running_distance
                else:
                    routes[r].add(tuple([coords[node] for node in path]))
                    distances[tuple([coords[node] for node in path])] = running_distance
    return (ranges, routes, distances)

def get_ranges(min_dist, max_dist, number_of_ranges=2):
    line_points = numpy.linspace(min_dist, max_dist, number_of_ranges)
    ranges = []
    for i in range(0, len(line_points)-1):
         ranges.append((line_points[i],line_points[i+1]))
    return ranges

""" Accumulate path of nodes, P, s.t.
    a. dist_min <= Sum(path) <= dist_max
    b. P contains at least a node in X
       and a node in Y.
    c. For any node sequence in the path
       node_i, node_j, node_k
       node_k != node_i
    d. No node in P is outside of [X.a, Y.b]
       Note: we assume that the graph given
       contains no such node since it was cleared
       of these nodes by a prior method.
    e. If at any point there are >1 viable
       nodes to choose from, the next node
       is choosen pseudorandomly.

    Elaboration on a.,b.,c.:
        The candidate of next nodes starts as
        any of that node's neighbors, but is
        progressively filtered.
        As we traverse, we may come to a point
        where not all criteria can be met.
        If we get to such a point:
        if running_distance < dist_min, else we"ll return
        running_path.
        Specifically,
        a. We will filter from the candidate set of next
           viable nodes any node whose addition
           will put us over the dist_max
        b. We will filter out any node which
           does not have a distance (is None) to
           node in X or Y depending on whether we've
           seen such nodes yet. Once we've
           seen a node in X or Y, we don't care about this.
        c. We will filter out any node that is equal to the node
           2 nodes prior if the path length so far is >1.
    """
def random_walk(cleared_graph, source_node, closest_distances, dist_min, dist_max):
    running_distance = 0
    path = [source_node]
    seen_X = True if closest_distances[source_node][0]==0 else False
    seen_Y = True if closest_distances[source_node][1]==0 else False
    while True:
        candidate_nodes = cleared_graph[path[-1]].keys()
        candidate_nodes[:] = [node for node in candidate_nodes if is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances)]
        if len(candidate_nodes) > 0:
            new_node = random.choice(candidate_nodes)
            running_distance += cleared_graph[path[-1]][new_node]
            seen_X = True if closest_distances[new_node][0]==0 else False
            seen_Y = True if closest_distances[new_node][1]==0 else False
            path.append(new_node)
        else:
            break

    if dist_min <= running_distance <= dist_max:
        return (path,running_distance)
    else:
        return (None,None)

""" Filter based on false see above method description
    a. We will filter from the candidate set of next
       viable nodes any node whose addition
       will put us over the dist_max
    b. We will filter out any node which
       does not have a distance (is None) to
       node in X or Y depending on whether we've
       seen such nodes yet. Once we've
       seen a node in X or Y, we don't care about this.
    c. We will filter out any node that is equal to the node
       2 nodes prior if the path length so far is >1.
    """
def is_viable(node, running_distance, dist_max, path, cleared_graph, seen_X, seen_Y, closest_distances):
    prev_node = path[-1]
    next_dist = cleared_graph[prev_node][node]
    if running_distance + next_dist > dist_max:#criteria a
        return False
    if (not seen_X) and closest_distances[node][0] is None:#criteria b
        return False
    if (not seen_Y) and closest_distances[node][1] is None:#criteria b
        return False
    if len(path)>1 and path[-2]==node:#criteria c
        return False
    return True

# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002
def Dijkstra(G, start, end=None):
	"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation:
	a. A vertex can be any object that can
	be used as an index into a dictionary.
	b. G is a dictionary, indexed by vertices.
	c. For any vertex v, G[v] is itself a dictionary,
	indexed by the neighbors of v. For any edge v->w, G[v][w] is the length of
	the edge.

	This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.

	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.

	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
 	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0

	for v in Q:
		D[v] = Q[v]
		if v == end: break

		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v

	return (D,P)

def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path



# Priority dictionary using binary heaps
# David Eppstein, UC Irvine, 8 Mar 2002


class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap
of pairs (value,key).  Note that changing or removing a dict entry will
not remove the old pair from the heap until it is found by smallest() or
until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding
pair to heap.  Rebuilds the heap if the number of deleted items grows
too large, to avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]
