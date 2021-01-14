import networkx as nx

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import random as r
import time


# class Network:
#
#     def __init__(self):
#         self.G = nx.DiGraph()
#
#     def load(self, file_path):
#         algo = GraphAlgo()
#         algo.load_from_json(file_path)
#         # print(algo.__repr__)
#         for i in algo.get_graph().get_all_v().keys():
#             self.G.add_node(i)
#         for i in algo.get_graph().get_all_v().keys():
#             for j, w in algo.get_graph().all_out_edges_of_node(i).items():
#                 self.G.add_edge(i, j, weight=w.weight)
#         return self.G
#

# def graph_creator(node_size: int = 0, edge_size: int = 0) -> object:
#     g1 = DiGraph()
#
#     for i in range(0, node_size):
#         g1.add_node(i)
#
#     nodes = nodes_to_array(g1)
#
#     counter = 0
#     while counter < edge_size:
#         r1 = int((r.random() * node_size))
#         r2 = int((r.random() * node_size))
#         w = (r.random() * 10)
#         if g1.add_edge(nodes[r1], nodes[r2], w):
#             counter += 1
#     return g1
#
#
# def nodes_to_array(graph: object = None) -> list:
#     if graph is None:
#         return []
#
#     ans = []
#
#     for key in graph.get_all_v():
#         ans.append(key)
#
#     return ans
#
#
# def make_graph(V: int = 0, E: int = 0) -> object:
#     V = V  # Full graph of V vertices
#     E = E
#     if E > V * (V - 1):
#         E = V * (V - 1)
#     return graph_creator(V, E)

def load_graph(file_path: str = "") -> object:
    g = DiGraph()
    algo = GraphAlgo(g)
    algo.load_from_json(file_path)

    # G = nx.DiGraph()
    #
    # for i in algo.get_graph().get_all_v().keys():
    #     G.add_node(i)
    # for i in algo.get_graph().get_all_v().keys():
    #     for j, w in algo.get_graph().all_out_edges_of_node(i).items():
    #         G.add_edge(i, j, weight=w.weight)
    return transfer_to_nx(algo.get_graph())

def transfer_to_nx(graph: object = None) -> object:
    if graph is None:
        return None

    algo = GraphAlgo(graph)
    # algo.load_from_json(file_path)

    G = nx.DiGraph()

    for i in algo.get_graph().get_all_v().keys():
        G.add_node(i)
    for i in algo.get_graph().get_all_v().keys():
        for j, w in algo.get_graph().all_out_edges_of_node(i).items():
            G.add_edge(i, j, weight=w.weight)
    return G


if __name__ == '__main__':
    # nx = Network()
    # nx.load('../data/A5')
    # # print(dir(nx.G))

    # g = DiGraph()
    # algo = GraphAlgo(g)
    # algo.load_from_json('../data/Graphs_random_pos/G_30000_240000_2.json')


    # # Testing shortest_path
    # print("Start")
    # start = time.time()
    # print(nx.dijkstra_path(G, 0, 993))
    # end = time.time() - start
    # print(end)
    # print("End")

    # G = transfer_to_nx(make_graph(V, E))

    # Testing SCC's
    # generator = max(nx.kosaraju_strongly_connected_components(G))
    # # print(dir(generator))
    # print(generator.pop())
    # print("End")

    print("Start")
    start = time.time()
    algo = GraphAlgo()
    algo.load_from_json('../data/Graphs_random_pos/G_30000_240000_2.json')

    G = load_graph('../data/Graphs_random_pos/G_30000_240000_2.json')  # Returns nx.DiGraph object.

    for scc in nx.kosaraju_strongly_connected_components(G):
        print(scc)

    end = time.time() - start
    print(end)
    print("--------------------------------------------")
    for scc in algo.connected_components():
        print(scc)
    end = time.time() - start
    print(end)
