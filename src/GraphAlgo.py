import json
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from src.GraphInterface import GraphInterface
from queue import PriorityQueue


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self, directed_graph: object = None):
        self._graph = DiGraph()
        if directed_graph is not None:
            if isinstance(directed_graph, DiGraph):
                self._graph = directed_graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        flag = True
        try:
            with open(file_name, 'r') as jsonFile:
                load = json.load(jsonFile)
                graphJson = DiGraph()
            for node in load["Nodes"]:
                if "pos" in node:
                    posJ = tuple(map(float, str(node["pos"]).split(",")))
                    graphJson.add_node(node_id=node["id"], pos=posJ)
                else:
                    graphJson.add_node(node_id=node["id"])
            for edge in load["Edges"]:
                graphJson.add_edge(id1=edge["src"], id2=edge["dest"], weight=edge["w"])
            self._graph = graphJson
            print("load successes")
        except Exception as e:
            print(e)
            print("load failed")
            flag = False
        finally:
            # jsonFile.close()
            return flag

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        flag = True
        with open(file_name, "w") as jsonFile:
            try:
                d = {"Edges": [], "Nodes": []}
                for src in self._graph.outEdges.keys():
                    for dst, w in self._graph.all_out_edges_of_node(src).items():
                        d["Edges"].append({"src": src, "w": w.weight, "dest": dst})
                for key, value in self._graph.nodes.items():
                    if value.location is None:
                        d["Nodes"].append({"id": key})
                    else:
                        d["Nodes"].append({"pos": str(value.location), "id": key})
                s = d.__str__()
                s = s.replace(" ", "")
                s = s.replace("'", "\"")
                jsonFile.write(s)
                print("Save Json was succeeded ")
            except Exception as e:
                print("Save Json was failed ")
                print(e)
                flag = False
            finally:
                # jsonFile.close()
                return flag

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through

        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])

        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        # Edge cases
        # Either one of the nodes does not exist in the graph.
        if id1 not in self._graph.get_all_v() or id2 not in self._graph.get_all_v():
            return float('inf'), []
        if id1 == id2:  # The path from a node to itself is empty and the total distance is 0
            return 0, []

        # Initialization
        src = id1
        dest = id2

        self.reset_tags()
        self.set_weights_infinity()

        prev_node = dict()  # A map that stores: {key(int), caller(Node)} (Which node called which)
        pq = PriorityQueue()  # A queue to prioritize nodes with lower weight
        visited = dict()  # Keep track of visited nodes
        path = []  # A list of nodes that represents the path between id1 and id2

        total_dist = 0.0
        destination_found = False
        curr = self._graph.get_node(id1)
        curr.weight = 0
        visited[curr.key] = True

        pq.put(curr)

        # Traverse
        while not pq.empty():

            curr = pq.get()  # Pop the next node with the lowest weight O(log(n))
            neighbors = self._graph.all_out_edges_of_node(curr.key)  # Neighbors of curr node
            for i in neighbors:  # Iterate over neighbors of curr
                out_edge = neighbors[i]
                neighbor = self._graph.get_node(out_edge.dest)
                if not visited.get(neighbor.key):  # Process node if not visited
                    total_dist = curr.weight + out_edge.weight
                    if total_dist < neighbor.weight:
                        neighbor.weight = total_dist
                        prev_node.__setitem__(neighbor.key, curr)
                    if neighbor not in pq.queue:  # If not already in the queue, enqueue neighbor.
                        pq.put(neighbor)
            # Finished processing curr's neighbors
            if curr.key == dest:
                destination_found = True
            visited[curr.key] = True

        if destination_found:
            path = self.rebuild_path(prev_node, src, dest)
            total_dist = path[len(path) - 1].weight
            return total_dist, path

        return float('inf'), []

    def rebuild_path(self, node_map: dict = None, src: int = 0, dest: int = 0) -> list:
        if node_map is None:
            return None
        ans = [self._graph.get_node(dest)]  # Start from the end

        for called_node in node_map.keys():
            calling_node = node_map.get(called_node)
            ans.append(calling_node)
            if calling_node.key == src:
                break

        ans.reverse()
        return ans

    def reset_tags(self):
        for key in self._graph.get_all_v().keys():
            node = self.get_graph().get_node(key)
            node.tag = 0

    def set_weights_infinity(self):
        for key in self._graph.get_all_v().keys():
            node = self._graph.get_node(key)
            node.weight = float('inf')

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        pass

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        pass

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        pass

    def __repr__(self):
        return self._graph.__repr__()


if __name__ == '__main__':
    g1 = DiGraph()

    g1.add_node(0)
    g1.add_node(1)
    g1.add_node(2)
    g1.add_node(3)
    g1.add_node(4)

    g1.add_edge(0,1,1)
    g1.add_edge(1,2,2)
    g1.add_edge(2,3,1)
    g1.add_edge(2,1,1)
    g1.add_edge(0,4,2)
    g1.add_edge(4,0,3)
    g1.add_edge(4,2,0.1)
    g1.add_edge(2,4,2)

    ga = GraphAlgo(g1)
    print(ga.shortest_path(4, 3))

    # file = 'A5.txt'
    # g1 = GraphAlgo()
    # g2 = g1.load_from_json(file_name=file)
    # print("\n\n\n\ngraph algo is\n\n")
    # print(f"Graph load check:{g2} \n\n")
    # print("before remove")
    # print(g1.get_graph().__repr__())
    # g1.get_graph().remove_node(1)
    # print("after remove")
    # print(g1)
    # print(g1.save_to_json("TalTest.txt"))
    # print(g1.load_from_json("TalTest.txt"))
    # print(g1)
