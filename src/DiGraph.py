from GraphInterface import GraphInterface


class GeoLocation(object):
    def __init__(self, location=None):
        self.location = location
        if location is not None:
            self.x = location[0]
            self.y = location[1]
            self.z = location[2]

    def distance(self, other):
        d1 = (self.x - other.x) ** 2  # (x1-x2)^2
        d2 = (self.y - other.y) ** 2
        d3 = (self.z - other.z) ** 2
        return (d1 + d2 + d3) ** 0.5


class NodeData(object):
    def __init__(self, key: int, tag=0, info="", location=None, weight=1):
        self.key = key
        self.tag = tag
        self.info = info
        self.weight = weight
        if location is not None:
            self.location = GeoLocation(location)
        else:
            self.location = None


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
        self.inEdges[id2][id1] = weight
        self.outEdges[id1][id2] = weight
        return True

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
        self.nodes[node_id] = NodeData(node_id, location=pos)
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
        for j in self.inEdges.keys():
            if node_id in self.inEdges[j].keys():
                del self.outEdges[j][node_id]
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
            if node_id1 in self.outEdges or node_id1 in self.inEdges:
                del self.outEdges[node_id1][node_id2]
                del self.inEdges[node_id2][node_id1]
                self.sizeE -= 1
                return True
        return False