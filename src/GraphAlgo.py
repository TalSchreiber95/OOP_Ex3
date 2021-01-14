import json
import random

import matplotlib.pyplot as plt
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph, GeoLocation
from src.GraphInterface import GraphInterface
from queue import PriorityQueue
from queue import Queue


class GraphAlgo(GraphAlgoInterface):
    """
    * This class represents a set of graph theory algorithms to
    * apply on a directed, weighted graph data structure, including:
    * Saving and loading a graph, calculating shortest paths on the graph from
    * one node to another,
     checking if the graph is strongly connected, and so on...
    """

    def __init__(self, directed_graph: object = None): # TODO: should be change
        self._graph = DiGraph()
        if directed_graph is not None:
            if isinstance(directed_graph, DiGraph):
                self._graph = directed_graph

    def get_graph(self) -> GraphInterface:
        """
        @return: the directed graph on which the algorithm works on.
        """
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns: True if the loading was successful, False o.w.
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
            # print("load successes")
        except Exception as e:
            print(e)
            print("load failed")
            flag = False
        finally:
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
                for src in self._graph.out_edges.keys():
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
                # print("Save Json was succeeded ")
            except Exception as e:
                print("Save Json was failed ")
                print(e)
                flag = False
            finally:
                return flag

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        * returns the the shortest path between src to dest - as an ordered List of nodes:
        * src--> n1-->n2-->...dest
        * Logic only was taken from: https://en.wikipedia.org/wiki/Shortest_path_problem
        * Note if no such path --> returns null;
        @Runtime: Regular BFS using a priority queue = O(|V|+|E|).
        @param id1  - start node
        @param id2 - end (target) node
        @return - the path between src and dest if there is one.
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
            path = self.rebuild_path(prev_node, src, dest)  # A list of nodes that represents the path between id1->id2

            total_dist = path[len(path) - 1].weight
            return total_dist, path

        return float('inf'), []

    def rebuild_path(self, node_map: dict = None, src: int = 0, dest: int = 0) -> list:
        """
        * This method back-tracks, takes a map of int keys and NodeData values
        * inserts all nodes in the path to a list and return the list
        """
        if node_map is None or src == dest:
            return None
        ans = [self._graph.get_node(dest)]
        next_node = node_map.get(dest)

        while next_node.key is not src:  # Backtrack from dest to src
            ans.append(node_map.get(next_node.key))
            next_node = node_map.get(next_node.key)
        if self._graph.get_node(src) not in ans:
            ans.append(self._graph.get_node(src))

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
        * Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        * Notes: If the graph is None or id1 is not in the graph, the function should return an empty list []
        @param id1: The node id
        @return: The list of nodes in the SCC
        """
        if self._graph is None or self._graph.get_node(id1) is None:
            return []

        self.reset_tags()  # This method executes a BFS and tag nodes so reset_tags() must be called.

        # Traverse the original graph, from node id1, and tag all reachable nodes
        ans = []
        src = id1  # alias
        original_graph = self.get_graph()
        self.traverse_breadth_first(src, original_graph)
        # Transpose/Reverse graph's edges
        transposed_graph = self.reverse_graph()
        # Traverse the transposed graph, from node id1, and un-tag all reachable nodes
        self.traverse_breadth_first(src, transposed_graph)

        # Iterate over nodes in the transposed graph and find the nodes that are tagged twice!
        for key in transposed_graph.get_all_v():
            node = transposed_graph.get_node(key)
            if node.tag == 2:
                ans.append(self._graph.get_node(node.key))  # Append original node
        return ans

    def traverse_breadth_first(self, src: int = 0, graph: GraphInterface = None):
        """
        * This method is made to traverse any node in the graph and set tag on them using bfs algorithm.
        """
        if not isinstance(graph, DiGraph) or graph is None or self._graph.get_node(src) is None:
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

    def reverse_graph(self) -> GraphInterface:
        """
        * This method transposes the given graph.
        * The new graph will have the same set of vertices V = {v1, v2, .. , v(n)},
        * And all transposed edges. E = {(v1,v2), (v2,v6), .. }, E(transposed) = {(v2,v1), (v6,v2), ..}.
        * @param g - the given graph.
        * @return a transposed directed_weighted_graph.
        """
        ans = DiGraph()

        nodes = self._graph.get_all_v()  # {key: NodeData}
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
        * This method finds all the Strongly Connected Components(SCC) in the graph.
        * Notes: If the graph is None the function should return an empty list []
        @return: The list all SCC
        """
        self.reset_tags()
        ans = []
        visited = dict()  # A dictionary of visited nodes

        for key in self._graph.get_all_v():
            if not visited.get(key):
                path = self.connected_component(key)
                for node in path:
                    visited.__setitem__(node.key, True)
                ans.append(path)
        return ans

    def plot_graph(self):
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner using get_random_location() function.
        """
        g = self.get_graph()
        plt.title("Our graph:" + g.__str__())
        plt.xlabel("X")
        plt.ylabel("-<")  # I should flip 'Y' letter so I decided to write it by a tricky way. :)
        for src, node in g.get_all_v().items():
            # Print the node point
            if node.location is None:
                pos = self.get_random_location()  # get a elegant location
                node.location = GeoLocation(pos)
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
        """
        * This method was made to return a random location for a node when then node doesn't have any location.
        * How it work?
        * We get the max and min of the bounding box and then we set the nodes location on a random range inside it.
        * if there is no bounding box , which means there is no node location enough to set this bounding box,
        * so we set the nodes location in a range of x=[32,33],y=[35,36],z=0.
        """
        max_x, max_y, max_z, min_x, min_y, min_z = self.get_max_and_min()
        if max_x == float('-inf') and min_x == float('inf') and max_y == float('-inf') and min_y == float('inf') and \
                max_z == float('-inf') and min_z == float('inf'):
            x = random.uniform(32, 33)
            y = random.uniform(35, 36)
            z = 0
            ans = x, y, z
            return ans
        counter = 0
        for src, node in self._graph.get_all_v().items():
            if node.location is not None:
                counter += 1
        x = random.uniform(max_x, min_x)
        y = random.uniform(max_y, min_y)
        z = random.uniform(max_z, min_z)
        if counter == 0:  # means all nodes doesn't have any location
            x = random.uniform(32, 33)
            y = random.uniform(35, 36)
            z = 0
            ans = x, y, z
        else:
            ans = x, y, z
        return ans

    def get_max_and_min(self):
        """
        This method get the max and min of the bounding box on current graph.
        @return max and min of bounding box , o.w -inf&inf
        """
        max_x = float('-inf')
        min_x = float('inf')
        max_y = float('-inf')
        min_y = float('inf')
        max_z = float('-inf')
        min_z = float('inf')
        ans = max_x, max_y, max_z, min_x, min_y, min_z
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
        if counter > 4:
            ans = max_x, max_y, max_z, min_x, min_y, min_z
        return ans

    def __repr__(self):
        return self._graph.__repr__()

    def __str__(self):
        return self._graph.__str__()
