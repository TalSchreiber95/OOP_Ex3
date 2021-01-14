import networkx as nx

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import random as r
import time

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

    print("Start shortest path")
    print("Start")
    start = time.time()
    algo = GraphAlgo()
    algo.load_from_json('../data/Graphs_random_pos/G_30000_240000_2.json')

    G = transfer_to_nx(algo.get_graph())  # Returns nx.DiGraph object.

    spNX = nx.dijkstra_path(G, 0, 100)

    end = time.time() - start
    print(end)
    print("End")

    print("Start")
    start = time.time()
    sp = algo.shortest_path(0, 100)
    end = time.time() - start
    print(end)
    print("End")
    print("End shortest path")
    print("--------------------------------------------")

    print("Start SCC")
    start = time.time()
    algo = GraphAlgo()
    algo.load_from_json('../data/Graphs_random_pos/G_30000_240000_2.json')

    G = load_graph('../data/Graphs_random_pos/G_30000_240000_2.json')  # Returns nx.DiGraph object.

    for scc in nx.kosaraju_strongly_connected_components(G):
        print(scc)

    end = time.time() - start
    print(end)
    print("End")

    for scc in algo.connected_components():
        print(scc)
    end = time.time() - start
    print(end)
    print("End SCC")
    print("--------------------------------------------")
