import json
import random

import matplotlib.pyplot as plt
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph, NodeData, GeoLocation
from src.GraphInterface import GraphInterface
from queue import PriorityQueue
from queue import Queue


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

        total_dist = 0.0
        destination_found = False
        curr = self._graph.get_node(id1)
        curr.weight = total_dist
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
            path = self.rebuild_path(prev_node, src, dest)  # A list of nodes that represents the path between id1
            # and id2

            total_dist = path[len(path) - 1].weight
            return total_dist, path

        return float('inf'), []

    # This method back-tracks, takes a map of int keys and NodeData values
    # inserts all nodes in the path to a list and return the list
    def rebuild_path(self, node_map: dict = None, src: int = 0, dest: int = 0) -> list:
        if node_map is None or src == dest:
            return None
        ans = [self._graph.get_node(dest)]
        # print(node_map)
        next_node = node_map.get(dest)
        # print(next_node)

        while next_node.key is not src:  # Backtrack from dest to src
            print(ans)
            ans.append(node_map.get(next_node.key))
            next_node = node_map.get(next_node.key)

        # for prev in node_map.keys():  # Iterate over the map until reached source node.
        #     calling_node = node_map.get(prev)
        #     ans.append(calling_node)
        #     if calling_node.key == src:
        #         break

        ans.reverse()  # Inserted from
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
        if self._graph is None or self._graph.get_node(id1) is None:
            return []
        self.reset_tags()
        # Traverse the original graph, from node id1, and tag all reachable nodes
        ans = []
        src = id1  # alias

        self.traverse_breadth_first(src, self._graph)
        # Reverse graph's edges
        temp = self.reverse_graph()
        self.traverse_breadth_first(src, temp)

        for key in temp.get_all_v():
            node = temp.get_node(key)
            if node.tag == 2:
                ans.append(node)

        print(self._graph.__repr__())
        # Traverse the reversed graph, from node id1, and un-tag all reachable nodes
        #
        return ans

    def traverse_breadth_first(self, src: int = 0, graph: object = None):
        if not isinstance(graph, DiGraph) or graph is None:
            return
        curr = graph.get_node(src)

        q = Queue()

        q.put(curr)
        curr.tag += 1

        while not q.empty():

            curr = q.get()
            out_edges = graph.all_out_edges_of_node(curr.key)

            for i in out_edges:
                out_edge = out_edges[i]
                neighbor = graph.get_node(out_edge.dest)  # Get curr's neighbor
                if neighbor.tag == curr.tag - 1:
                    neighbor.tag += 1  # If un-tagged -> tag it.
                    q.put(neighbor)  # and enqueue it

    def reverse_graph(self) -> object:
        ans = DiGraph()
        # {key: NodeData}
        nodes = self._graph.get_all_v()
        for key in nodes:
            ans.add_node(key)
            ans.get_node(key).tag = self._graph.get_node(key).tag

        for key in nodes:
            out_edges = self._graph.all_out_edges_of_node(key)
            for edge in out_edges:
                e = out_edges.get(edge)
                ans.add_edge(e.dest, e.src, e.weight)

        return ans

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Components(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        ans = []
        visited = dict()  # A dictionary of visited nodes

        for key in self._graph.get_all_v():
            if not visited.get(key):
                path = self.connected_component(key)
                for node in path:
                    visited.__setitem__(node.key, True)
                ans.append(path)
        return ans

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        g = self.get_graph()
        plt.title("Our graph:" + g.__str__())
        plt.xlabel("X")
        plt.ylabel("-<")  # I should flip y letter so I decided to write it by a tricky way. :)
        for src, node in g.get_all_v().items():
            # Print the node point
            if node.location is None:
                # pos = 0, 0, 0

                pos = self.get_random_location()
                node.location = GeoLocation(pos)
                # node.location.y = GeoLocation(pos)
            plt.plot(node.location.x, node.location.y, marker='o', markerfacecolor='red', markersize=3, color='yellow')
            plt.text(node.location.x, node.location.y, str(node.key))

            # Print the edge line
            for dest in g.all_out_edges_of_node(src).keys():
                x1 = g.get_all_v()[src].location.x
                y1 = g.get_all_v()[src].location.y
                if g.get_all_v()[dest].location is None:
                    pos = self.get_random_location()
                    g.get_all_v()[dest].location = GeoLocation(pos)
                    g.get_all_v()[dest].location = GeoLocation(pos)
                x2 = g.get_all_v()[dest].location.x
                y2 = g.get_all_v()[dest].location.y
                plt.arrow(x1, y1, x2 - x1, y2 - y1, width=0.00001, linewidth=0.05)

        plt.show()

    def get_random_location(self):
        max_x, max_y, max_z, min_x, min_y, min_z = self.get_max_and_min()
        counter = 0
        for src, node in self._graph.get_all_v().items():
            if node.location is not None:
                counter += 1
        x = random.uniform(max_x, min_x)
        y = random.uniform(max_y, min_y)
        z = random.uniform(max_z, min_z)
        if counter == 0:  # means all nodes doesn't have any location
            ans = 0.5, 0.5, 0.5
        else:
            ans = x, y, z
        return ans

    def get_max_and_min(self):
        max_x = float('-inf')
        min_x = float('inf')
        max_y = float('-inf')
        min_y = float('inf')
        max_z = float('-inf')
        min_z = float('inf')
        counter = 0
        for src, node in self._graph.get_all_v().items():
            if node.location is not None:
                x = node.location.x
                y = node.location.y
                z = node.location.z
                counter += 1
                max_x = x if x > max_x else max_x
                min_x = x if x < min_x else min_x
                max_y = y if y > max_y else max_y
                min_y = y if y < min_y else min_y
                max_z = z if z > max_z else max_z
                min_z = z if z < min_z else min_z
        if counter > 0:
            ans = max_x, max_y, max_z, min_x, min_y, min_z
        else:
            ans = 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
        return ans

    def __repr__(self):
        return self._graph.__repr__()

    def __str__(self):
        return self._graph.__str__()


if __name__ == '__main__':
    # g1 = DiGraph()

    # g1.add_node(0)
    # g1.add_node(1)
    # g1.add_node(2)
    # g1.add_node(3)
    # g1.add_node(4)

    # g1.add_edge(0, 1, 1)
    # g1.add_edge(1, 2, 2)
    # g1.add_edge(2, 3, 1)
    # # g1.add_edge(2, 1, 1)
    # g1.add_edge(0, 4, 2)
    # g1.add_edge(4, 0, 3)
    # # g1.add_edge(4, 2, 0.1)
    # g1.add_edge(2, 4, 2)
    # g1.add_edge(0, 1, 1)
    # g1.add_edge(1, 0, 1)
    # g1.add_edge(0, 2, 1)

    # ga = GraphAlgo(g1)
    # print(ga.shortest_path(4, 3))
    # print(ga.connected_component(1))
    # print(ga.connected_components())

    file = '../data/Graphs_on_circle/G_10_80_1.json'
    g1 = GraphAlgo()
    g2 = g1.load_from_json(file_name=file)
    g1.plot_graph()
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
