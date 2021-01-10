import json
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from src.GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self._graphAlgo = DiGraph()

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self._graphAlgo

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
                    x = node["pos"][0]
                    y = node["pos"][1]
                    z = node["pos"][2]
                    # st = str(node["pos"]).split(",")
                    # posJ = tuple(map(float, str(st[0], st[1], st[2])))
                    posJ = x, y, z
                    # posJ = tuple(map(float, str(node["pos"]).split(",")))
                    graphJson.add_node(node_id=node["id"], pos=posJ)
                else:
                    graphJson.add_node(node_id=node["id"])

            for edge in load["Edges"]:
                graphJson.add_edge(id1=edge["src"], id2=edge["dest"], weight=edge["w"])
            self._graphAlgo = graphJson
            print("load successes")
        except Exception as e:
            print(e)
            print("load failed")
            flag = False
        finally:
            jsonFile.close()
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
                d = {"Nodes": [], "Edges": []}
                for src in self._graphAlgo.outEdges.keys():
                    for dst, w in self._graphAlgo.all_out_edges_of_node(src).items():
                        d["Edges"].append({"src": src, "w": w, "dest": dst})

                for node in self._graphAlgo.nodes.values():
                    # print(node.location)  # TODO: should check how to get location from node
                    if node.location is None:
                        d["Nodes"].append({"id": node.node_id})
                    else:
                        d["Nodes"].append({"pos": str(node.location), "id": node})
                jsonFile.write(d.__repr__())
                print("Save Json was succeeded ")
                flag = True
            except Exception as e:
                print("Save Json was failed ")
                print(e)
                flag = False
            finally:
                jsonFile.close()
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
        pass

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
        return self._graphAlgo.__repr__()


if __name__ == '__main__':
    file = 'A5.txt'
    g1 = GraphAlgo()
    g2 = GraphAlgo.load_from_json(g1, file_name=file)
    print("\n\n\n\ngraph algo is\n\n")
    print(f"Graph load check:{g2} \n\n")
    print(g1.get_graph().__repr__())
    g1.get_graph().remove_node(1)
    print(g1.get_graph().__repr__())
    print(g1.save_to_json("TalTest"))  # should be fix
