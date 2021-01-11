from GraphInterface import GraphInterface


class EdgeData(object):
    def __init__(self, src: int, dest: int, tag: int, info: str, weight: float = 0):
        self.src = src
        self.dest = dest
        self.tag = tag
        self.info = info
        self.weight = weight

    def getWeight(self) -> float:
        return self.weight


class GeoLocation(object):
    def __init__(self, location: tuple = None):
        if location is not None:
            self.x = location[0]
            self.y = location[1]
            self.z = location[2]

    def distance(self, other):
        d1 = (self.x - other.x) ** 2  # (x1-x2)^2
        d2 = (self.y - other.y) ** 2
        d3 = (self.z - other.z) ** 2
        return (d1 + d2 + d3) ** 0.5

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


class NodeData(object):
    def __init__(self, key: int, tag=0, info="", location: tuple = None, weight=0):
        self.key = key
        self.tag = tag
        self.info = info
        self.weight = weight
        if location is not None:
            self.location = GeoLocation(location)
        else:
            self.location = None

    def __repr__(self):
        return "{}".format(self.key)


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.nodes = dict()
        self.outEdges = dict()
        self.inEdges = dict()
        self.sizeE = 0
        self.sizeV = 0
        self.sizeMc = 0

    def v_size(self) -> int:
        """
                  Returns the number of vertices in this graph
                  @return: The number of vertices in this graph
                  """
        return self.sizeV

    def e_size(self) -> int:
        """
                Returns the number of edges in this graph
                @return: The number of edges in this graph
                """
        # self.sizeE = 0
        # for dest in self.inEdges.keys():
        #     self.sizeE = len(self.all_in_edges_of_node(dest))
        return self.sizeE

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
                    (node_id, node_data)
                   """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
                each node is represented using a pair (other_node_id, weight)
                 """
        return self.inEdges.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
               (other_node_id, weight)
               """
        return self.outEdges.get(id1)

    def get_mc(self) -> int:
        """
                   Returns the current version of this graph,
                   on every change in the graph state - the MC should be increased
                   @return: The current version of this graph.
                   """
        return self.sizeMc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
                  Adds an edge to the graph.
                  @param id1: The start node of the edge
                  @param id2: The end node of the edge
                  @param weight: The weight of the edge
                  @return: True if the edge was added successfully, False o.w.

                  Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
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

    def getNode(self, key):
        if self.nodes[key] == key:
            return self.nodes[key]

    def add_node(self, node_id: int, pos: tuple = None) -> bool:

        """
              Adds a node to the graph.
              @param node_id: The node ID
              @param pos: The position of the node
              @return: True if the node was added successfully, False o.w.

              Note: if the node id already exists the node will not be added
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
                  Removes a node from the graph.
                  @param node_id: The node ID
                  @return: True if the node was removed successfully, False o.w.

                  Note: if the node id does not exists the function will do nothing
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
                 Removes an edge from the graph.
                 @param node_id1: The start node of the edge
                 @param node_id2: The end node of the edge
                 @return: True if the edge was removed successfully, False o.w.

                 Note: If such an edge does not exists the function will do nothing
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


if __name__ == '__main__':
    g = DiGraph()  # creates an empty directed graph
    for n in range(5):
        g.add_node(n)
    g.add_edge(0, 3, 2)
    g.add_edge(1, 0, 2.1)
    g.add_edge(3, 2, 1.4)
    g.add_edge(1, 5, 1.1)
    g.add_edge(3, 4, 1.9)
    g.remove_edge(0, 3)
    g.add_edge(0, 3, 1.2)
    print(g.outEdges[1])
    print(g)  # prints the __repr__ (func output)
    print(g.get_all_v())  # prints a dict with all the graph's vertices.
    print(g.all_in_edges_of_node(1))
    print(g.all_out_edges_of_node(1))
