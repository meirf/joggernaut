Joggernaut
========
Joggernaut aims to provide the incline and distance control of a treadmill using natural elevation changes of NYC streets. Provides a route in South Harlem based on starting coordinates, distance range and elevation specifications. 

###Core Algorithm
**Input**

* starting coordinates, S
* minimum distance, D0
* maximum distance, D1
* lower elevation min, X.a
* lower elevation max, X.b
* upper elevation min, Y.a
* upper elevation max, Y.b
* graph, G = {N, E}, each node in N has a node id, lat/long coordinates and an elevation value; each edge in E has two node ids and a distance value
* number of ranges, R
* number of *attempted* paths per range, Q

**Ouput**

We divide up [D0, D1] into R equally sized ranges, {[D0, D0+(D1-D0)/R)]...[D1-(D1-D0)/R), D1]}. For each of these ranges [Ri.a, Ri.b] we attempt Q number of times to find:

* path,  P: { P0, P1, ... Pn}, where each Pi is in G.N, that satisfies:

    a. P0 == S

    b. Ri.a <= sum_edges(P)<= Ri.b

    c. For every node Pi in P, X.a <= elevation(Pi) <= Y.b

    d. Pi != Pi+2 For any node sequence in P: Pi, Pi+1, Pi+2.

    e. There must be at least one node, Pi in P, such that X.a <= elevation(Pi) <= X.b

     f. There must be at least one node, Pi in P, such that Y.a <= elevation(Pi) <= Y.b. Note: This need not be different than the node that satisfies criteria e.

     g. If PE is the set of nodes in P that satisfies criteria e. and PF  is the set of nodes in P that satisfies criteria f., then there must be at least one pair of node, (Pj, Pk) where Pj is in PE and Pk is in PF and j<=k.

*The output of the algorithm is a list of ranges; along with each range is a list of paths and the distance of each path.*


**Method**

[For a precise view of this implementation, see the code here.](https://github.com/meirf/joggernaut/blob/master/jogger/graph_preparation/graph_algorithms.py)

Before we attempt to walk the tree to find the paths, we have to compute some data. To make sure the paths satisfy criteria c., we modify G->G' by removing all nodes/edges with elevations outside of [X.a, Y.b]. We also compute closest distance, C, which oontains a tuple (X'',Y'') for every node in G', where X'' is the distance from a given node to the closest node with elevation in [X.a, X.b] and Y'' is the distance from a given node to the closest node with elevation in [Y.a, Y.b]. Note that either of these values can be zero if the node itself is in that range. We use None value if there no path to a node in that elevation range. For the shortest path algorithm we use Dijkstra on every node in G'.

For the graph traversal, we use a random walk. this random walk will directly aim to satisfy criteria a., b.,e. and f. Note that c. has already been satisfied by going form G->G'. The random walk will not aim to satisfy d. and g. Rather, after the traversal completes, we check whether they have been satisfied. If they are not satisfied, they are discarded.

To satisfy a., we start by adding S to P. We continue to add nodes to the path by randomly choosing a node from a filtered set of candidate nodes. The candidate nodes start as the neighbors of the previously added node in the path. If a node is not viable it is removed from this list. A node is not viable if adding it will put the path distance above the current range's max distance. It is also not viable if e. has not been satisfied yet and either C has a None value for this node in [X.a,X.b] or C has a value for this node that will cause path distance to exceed Ri.b. It is also not viable if f. has not been satisfied yet and either C has a None value for this node in [Y.a,Y.b] or C has a value for this node that will cause path distance to exceed Ri.b. We continue to add nodes until the filtered candidate set has at least one element. When there are no elements we check that the total distance is in [Ri.a, Ri.b] ; if so we check criteria d. and g. for total satisfiability.

###Client-Server Interaction

There is only one type of request sent from the client to the server. This request consists of S, D0, D1, X.a, X.b, Y.a and Y.b. The client stores the response data until it overwritten by another response. 

A request is triggered whenever the user clicks either of the two elevation sliders or sets the source coordinates. A request is also triggered when the minimum distance is moved left or the maximum distance is moved right. In the aforementioned cases, as soon as the response comes back, a path is randomly chosen from all the returned paths and displayed.

When the user moves the minimum distance to the right or maximum distance to the left, the client only makes a request to the server (and randomly chooses and displays a path from the response) if it has no more paths in memory that are in that distance range. Otherwise, a path is randomly taken from the paths in memory. When the user clicks the "Get Alternate Route" button, no request is made to the server. Rather, a path is randomly chosen from paths in memory and displayed.

Computing distances across many ranges within [D0, D1] allows for lower latency when the user shrinks the distance range and asks for an alternate route.

###Verification/Testing

[Here is the code used for testing.](https://github.com/meirf/joggernaut/blob/master/jogger/tests.py)

It contains tests that cover much of the app's functionality. Importantly, it contains tests that cover the criteria mentioned  "Core Algorithm -> Output" (above). Specifically see lines 565 to 612. Because the tests are not run manually, we can test results from 1000's of runs of the algorithm.

###Tuning

The section above "Core Algorithm -> Input" says that R and Q are inputs to this algorithm. These are not however controlled by the client and are hardcoded into the server. 

If these numbers are too low, there would be more requests to the server. The optimization of not making requests when the distance range is shrunk would be limited.

If these numbers are too high, the time for the server to fulfill a request would be too long.

###Input Unsatisfiability

Here are a few cases when the user will be warned of her input.

* If X.a > Y.b
* No node exists in G with elevation in [X.a, X.b]
* No node exists in G with elevation in [Y.a, Y.b]
* S has not been set
* No node exists in G with elevation in [X.a, X.b] starting from S within D1 distance
* No node exists in G with elevation in [Y.a, Y.b] starting from S within D1 distance

###Technologies Used

The app is built using the Django framework. It is written primarily in Python. Javascript and HTML are used on the front-end. The database used is SQLite. The source code is stored on Github. This file is written in Github-Flavored Markdown(GFM).

###Data Sources

The only 'manual' work done to get the data for the graph used was to place markers on street corners to get node coordinates. I then exported this Google Map as kml file. I parsed this kml file for latitude/longitude coordinates of the street corners. I then built an adjacency list for these nodes. Once I had the coordinates for these nodes, I used [Google's Elevation API](https://developers.google.com/maps/documentation/elevation) to get elevation values for each node.I used [Google's Distance API](https://developers.google.com/maps/documentation/distancematrix/) to get the distances of each edge.
[Google's Static Map API](https://developers.google.com/maps/documentation/staticmaps/) was used for getting path images.
