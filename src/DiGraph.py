from GraphInterface import GraphInterface


class EdgeData(object):
    """
    * This class represents an edge from one node to another on a given graph.
    * Edges has some fields like from where to where (src to dest), a tag,
    * information (String) and weight.
    * An edge is one sided on the graph data structure we're running,
    * meaning if there's an edge from src to dest, then not necessarily there's an edge
    * from dest to src.
    """

    def __init__(self, src: int, dest: int, tag: int = 0, info: str = "", weight: float = 0):
        self.src = src
        self.dest = dest
        self.tag = tag
        self.info = info
        self.weight = weight

    def getWeight(self) -> float:
        return self.weight


class GeoLocation(object):
    """
     * This class represents a GeoLocation as a vector <x,y,z>, aka Point3D.
     * Created for using Gui and printing the graph on the axes
    """

    def __init__(self, location: tuple = None):
        if location is not None:
            if len(location) == 3:
                self.x = location[0]
                self.y = location[1]
                self.z = location[2]

    def distance(self, other):
        """
        * This method was made to get the distance between two vector
        @return: distance
        """
        d1 = (self.x - other.x) ** 2  # (x1-x2)^2
        d2 = (self.y - other.y) ** 2
        d3 = (self.z - other.z) ** 2
        return (d1 + d2 + d3) ** 0.5

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


class NodeData(object):
    """
    * This class represents a node on a graph.
     * A node has a unique key, a tag,
     * Metadata (info=String) ,weight and location.
    """

    def __init__(self, key: int, tag=0, info="", location: tuple = None, weight=0):
        self.key = key
        self.tag = tag
        self.info = info
        self.weight = weight
        if location is not None:
            self.location = GeoLocation(location)
        else:
            self.location = None

    def __cmp__(self, other):
        """
        * This comparator was made to compare the two given node's weight for helping us in shortest path method
        """
        if other is None or not isinstance(other, NodeData):
            return 1
        if self.weight > other.weight:
            return 1
        elif self.weight < other.weight:
            return -1
        else:
            return 0

    def __lt__(self, other):
        """
        * This "less then" comparator was made to compare the two given node's weight for helping us in shortest path
        * method
        @return: 1 if node isn't NodeData type OR this.node bigger then other.node,
                -1 this.node smaller then other.node,
                0 if both node are equal.
        """
        if other is None or not isinstance(other, NodeData):
            return 1
        if self.weight > other.weight:
            return 1
        elif self.weight < other.weight:
            return -1
        else:
            return 0

    def __repr__(self):
        return "{} w:({})".format(self.key, self.weight)


class DiGraph(GraphInterface):
    """
     * This class represents a directed, weighted graph data structure.
     * Graph data is stored in dictionary inorder to achieve O(1) access to nodes and edges.
     * The graph supports some methodology like adding/removing nodes/edges from the graph,
     * connecting nodes on the graph and holding counts of edge size and node size.
    """

    def __init__(self):
        self.nodes = dict()
        self.outEdges = dict()
        self.inEdges = dict()
        self.sizeE = 0
        self.sizeV = 0
        self.sizeMc = 0

    def v_size(self) -> int:
        """
        @return: The number of vertices in this graph
        """
        return self.sizeV

    def e_size(self) -> int:
        """
        @return: The number of edges in this graph
        """
        return self.sizeE

    def get_all_v(self) -> dict:
        """
        * return a dictionary of all the nodes in the Graph, each node is represented using a pair
        * (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        * return a dictionary of all the nodes connected to (into) node_id ,
        * each node is represented using a pair (other_node_id, weight)
        """
        return self.inEdges.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        * return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        * (other_node_id, weight)
        """
        return self.outEdges.get(id1)

    def get_mc(self) -> int:
        """
        @return: The current version of this graph.
        """
        return self.sizeMc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        * Connects an edge with weight w between node src to node dest.
        Adds an edge to the graph.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        @param id1: src node of the edge
        @param id2: dest node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        """
        if id1 not in self.nodes or id2 not in self.nodes or id1 == id2:
            return False
        if weight < 0:
            return False
        if id2 in self.outEdges.get(id1) or id1 in self.inEdges.get(id2):
            return False  # If edge (src,dest) did not exist before, increment edgeSize.
        self.sizeE += 1
        self.sizeMc += 1
        edge = EdgeData(src=id1, dest=id2, tag=0, info=f"{id1}-->{id2}", weight=weight)
        self.inEdges[id2][id1] = edge
        self.outEdges[id1][id2] = edge
        return True

    def get_node(self, key):
        return self.nodes.get(key)

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        * adds a new node to the graph with the given node_data.
        * Note: if the node id already exists the node will not be added
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        """
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = NodeData(key=node_id, location=pos)
        self.outEdges[node_id] = {}
        self.inEdges[node_id] = {}
        self.sizeV += 1
        self.sizeMc += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        * Deletes the node (with the given ID) from the graph -
        * and removes all edges which starts or ends at this node.
        * Note: if the node id does not exists the function will do nothing
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        """
        if node_id not in self.nodes:
            return False
        for i in self.outEdges.keys():
            if node_id in self.outEdges[i].keys():
                del self.outEdges[i][node_id]
                self.sizeE -= 1
        for j in self.inEdges.keys():
            if node_id in self.inEdges[j].keys():
                del self.inEdges[j][node_id]
                self.sizeE -= 1
        self.outEdges.pop(node_id)
        self.inEdges.pop(node_id)
        self.nodes.pop(node_id)
        self.sizeV -= 1
        self.sizeMc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        * Deletes the edge from the graph.
        * Note: If such an edge does not exists the function will do nothing
        @param node_id1: src node of the edge
        @param node_id2: dest node of the edge
        @return: True if the edge was removed successfully, False o.w.
        """
        if node_id1 in self.nodes and node_id2 in self.nodes and node_id2 != node_id1:
            if node_id2 in self.outEdges[node_id1] and node_id1 in self.inEdges[node_id2]:
                del self.outEdges[node_id1][node_id2]
                del self.inEdges[node_id2][node_id1]
                self.sizeE -= 1
                return True
        return False

    def __repr__(self):
        s = "Graph info:\n|V|={} , |E|={} , MC={}\n".format(self.sizeV, self.sizeE, self.sizeMc)
        for key in self.nodes.keys():
            s += "{} --> in [".format(self.nodes[key])
            n = 0
            for w in self.all_in_edges_of_node(key).keys():
                s += "{}({})".format(str(w), self.inEdges[key][w].weight)
                s += " ,"
                n += 1
            if n > 0:
                s = s[:-2]
            s += "]\n"
            s += "{} --> Out [".format(self.nodes[key])
            n = 0
            for w in self.all_out_edges_of_node(key).keys():
                s += "{}({})".format(str(w), self.outEdges[key][w].weight)
                s += " ,"
                n += 1
            if n > 0:
                s = s[:-2]
            s += "]\n"
        return s

    def __str__(self):
        return "\n|V|={} , |E|={} , MC={}".format(self.sizeV, self.sizeE, self.sizeMc)
