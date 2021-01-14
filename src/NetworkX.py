import networkx as nx

from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import time as timeit


def compare_sccs(g_algo_nx: nx.DiGraph, laps):

    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.time()
        # s = g_algo.connected_components()
        # g_algo.connected_components()
        nx.kosaraju_strongly_connected_components(g_algo_nx)
        time = timeit.time() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    # print("All Scc's in the Graph:", s)
    return "Min Time: " + "{:.6f}".format(min_time) + " Max Time: " + "{:.6f}".format(max_time) + " Avg Time: " + \
           "{:.6f}".format(avg)


def compare_shortest_path(g_algo_nx: nx.DiGraph, laps):

    # curr_graph = g_algo_nx
    keys = list(g_algo_nx.nodes.keys())
    min_node = min(keys)
    max_node = max(keys)

    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.time()
        # s = g_algo.shortest_path(min_node, max_node)
        s = nx.dijkstra_path(g_algo_nx,min_node, max_node)
        time = timeit.time() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    print("Shortest Path between src:", min_node, "and dest:", max_node, "is:" + str(s))
    return "Min Time: " + "{:.6f}".format(min_time) + " Max Time: " + "{:.6f}".format(max_time) + " Avg Time: " + \
           "{:.6f}".format(avg)


def load_graph(file_path: str = "") -> object:
    g = DiGraph()
    algo = GraphAlgo(g)
    algo.load_from_json(file_path)
    return transfer_to_nx(algo.get_graph())


def transfer_to_nx(graph: object = None) -> object:
    if graph is None:
        return None

    algo = GraphAlgo(graph)
    # algo.load_from_json(file_path)

    GnX = nx.DiGraph()

    for i in algo.get_graph().get_all_v().keys():
        GnX.add_node(i)
    for i in algo.get_graph().get_all_v().keys():
        for j, w in algo.get_graph().all_out_edges_of_node(i).items():
            GnX.add_edge(i, j, weight=w.weight)
    return GnX


if __name__ == '__main__':

    graph = "../data/Graphs_random_pos/G_30000_240000_2.json"
    G1 = load_graph(graph)
    G2 = load_graph(graph)

    # algo.load_from_json(graph)
    print("********** Start of Testing SCC's **********\n")
    print('\n', compare_sccs(G1, 10), '\n')
    print("********** End of Testing SCC's **********\n\n")

    # algo.load_from_json(graph)
    print("********** Start of Testing Shortest Path **********\n")
    print('\n', compare_shortest_path(G2, 10), '\n')
    print("********** End of Testing Shortest Path **********\n\n")

