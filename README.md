# Welcome to our OOP_Ex3 Python project!
In this final OOP Course assignment we are here to present our last data structure design, which was written in Java,
Redesigned and rewritten in Python!
In total writing in python was very fun and interesting (Both of us writers write usually in java)


## Here you will find: 

### A Directed, Weighted Graph Data Structure. 
> A data structure in which vertices reside, which can be connected with edges that carry weight and some more attributes.
DiGraph classes methods:
We Have used three dictionaries that represent the graph. nodes: This dict represents the nodes on the graph by key and value(NodeData). out_edges: This dict represents the outgoing edges from each node (by key) to all of it's neighbors. in_edges: This dict represents the incoming edges from each node (by key) to all of it's neighbors.

### A Graph Algorithms and GUI Class.
> A class in which we have written some graph theory algorithms that apply to directed, weighted graphs.
This class also shows in a GUI window a graph of the form G = (V, E)

### An Algorithm Comparison Table.
> A table of the algorithms mentioned above, and their total, min, max and avrage over 10 iterations of runnning large graphs.
You can find this table in our Wiki pages found here https://github.com/TalSchreiber95/OOP_Ex3/wiki/Comparisons-with-other-environments-and-libs


# DiGraph classes methods:

We Have used three dictionaries that represent the graph. nodes: This dict represents the nodes on the graph by key and value(NodeData). out_edges: This dict represents the outgoing edges from each node (by key) to all of it's neighbors. in_edges: This dict represents the incoming edges from each node (by key) to all of it's neighbors.

### `Initialization of a DiGraph (Directed, Weighted Graph)`

A DiGraph object has a few properties such as: A few dictionaries (mentioned above), Sizes of Vertices(NodeData) and Edges(EdgeData) and 
a Meta-Changes counter (mc) that counts how many changes have been done on a given DiGraph.

### `def add_edge(src: int, dest: int, w: float) -> bool`

First need to ask if those nodes exist on this graph, no--> do nothing. Second, need to ask if the edge's weight is greater than or equal to 0 (due to the requirement of the interface), no--> do nothing. Next need to ask if those two nodes are the same nodes, yes --> break this function , else continue connecting those node. Next we'll connect those nodes on both dictionaries(in/out_edges). Note: If this node is already connected their weight will be updated according to the last connection (If it is not the same as last weight)

### `def remove_edge(src: int, dest: int) -> bool`

First we check if there is an edge between src and dest, and src != dest. If so --> remove from both incoming and outgoing edge dicts. Otherwise --> return None.

### `def add_node(node_id: int, pos: tuple) -> bool`
First we check if the given node_id already exists on the graph, if so do nothing and return False. Otherwise, adds the node to the nodes dictionary
and updates the relevant class fields.

### `def remove_node(key: int) -> bool`

First we need to ask if our graph contains this key node, no--> return None. Second, we delete all out going edges from the key node, and then all incoming edges into key node with an iterator. We delete the node from the nodes dictionary and return True if succeed. False otherwise.


# GraphAlgo class methods:

### >`def connected_component(id: int) -> list`
* This method returns a list represents the Strongly Connected Component (SCC) that node 'id'
belongs to. This method uses the Kosaraju's algorithm (Which traverses the graph, transposes all of the graph's edges and traverses it again).

### >`def connected_components() -> List[list]`
* This method returns a List of lists of all SCC's on the graph. This method uses the connected_component(id) method, 
and keeps track of all visited nodes within a certain SCC, and returns all SCC's of unvisited nodes.

### >`def shortest_path(id1: int, id2: int) -> tuple (float, list)` 
* Traverse the current graph Breadth-First inorder to find the shortest path from node 'id1' to node 'id2'.
This is done using a `Priority-Queue` data structure that prioritizes nodes by the lowest current path by weight.
This method was implemented with inspiration from Dijkstra's algorithm.
The method returns a tuple, which at index 0 contains the total distance from id1 to id2, and at index 1 contains the list 
of nodes that are on the shortest path.
<center> 
<h3> Illustration of Dijkstra </h3>

![alt text](https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif)

</center>

### >`def plot_graph(self) -> None` 
This method "plots" the graph, meaning if a node has a position (x, y, z) - it will be displayed on a GUI window 
at the specified location, otherwise - we have written a private method called >`def get_random_location()` 
which is in our GraphAlgo.py file, and it computes a random location based on all other nodes from the same graph,
which already have a location. If ALL nodes don't have a position - Randomly calculate positions of x=[32,33],y=[35,36],z=0.
Finally the method then shows the graph on a GUI window.


### >`def load/save_from_json(file_name: str) -> bool`
* Save or load the graph into / from a file located in the path that 'file_name' represents
This is done by reading or writing into a file using a json format.



# How To Run
* Download project zip file from **https://github.com/ItaySharabi/OOP_Ex3.git** or **https://github.com/TalSchreiber95/OOP_Ex3.git**

### Manually:

* Start PyCharm, IntelliJ or any other Python workspace environment, and open OOP_Ex3 project.
* You can either show a graph from the test class with the method >`def plot_graph() -> None`
* Or you can test algorithms as mentioned above on random graphs at your choice! use method: >`def make_graph(V=vertices, E=edges) -> DiGraph`

* Hit RUN (Green 'Play' button)! 

* Enjoy! :)
