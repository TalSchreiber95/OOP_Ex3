import unittest

import random as r

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


# This test class behaves as if any graph was given -
# 1. Break it down into Strongly connected components and test them:
#    I know connected_components() works when nodes do not belong to 2 different SCC's.
# 2. Get the largest SCC from the graph.
# 3. Execute shortest_path() from 1 specific node 'src' to all other nodes from it's SCC.
#    I know shortest_path() works AND connected_component(id) works when all paths are valid
#    and nodes do not belong to 2 different SCC.

class GraphAlgoTest(unittest.TestCase):
    if __name__ == '__main__':
        unittest.main()

    # This test method can test a random graph with 3 SCC's if no params are given
    # If given @param 'graph' as DiGraph(), then testing the shortest_path method will
    # Get the largest SCC and test all routes (which must exist) on that SCC.
    # If scc param is None - will take the largest SCC from the given graph, or the example graph.
    def test_shortest_path(self, SCC: list = None, graph: object = None):
        V = r.randint(20, 30)
        if SCC is None:
            if graph is not None:
                SCC = self.get_max_scc(graph)
            else:
                graph = self.make_graph(V, V * 4)
                SCC = self.get_max_scc(graph)
        elif graph is None:
            graph = self.make_graph(V, V * 4)
        if SCC is not None and graph is not None:
            try:
                algo = GraphAlgo(graph)
                first_node = SCC[0]

                for node in SCC:
                    if node.key != first_node.key:
                        sp1 = algo.shortest_path(first_node.key, node.key)
                        assert len(sp1[1]) > 1
                        dist1 = sp1[1][len(sp1[1]) - 1].weight
                        assert dist1 == sp1[0]
                        sp2 = algo.shortest_path(node.key, first_node.key)
                        assert len(sp2[1]) > 1
                        dist2 = sp2[1][len(sp2[1]) - 1].weight
                        assert dist2 == sp2[0]

                # algo.get_graph().add_node(-10)
                # sp = algo.shortest_path(first_node.key, algo.get_graph().get_node(-10))
                # assert sp[0] == float('inf') and len(sp[1]) == 0
            except AssertionError as e:
                print(e)
                self.fail("shortest_path_test failed with graph {}".format(algo.get_graph().__str__()))

    def test_connected_components(self, graph: object = None):
        if graph is None:
            V = r.randint(20, 30)
            graph = self.make_graph(V, V * 2)
        try:
            ga = GraphAlgo(graph)
            if ga.get_graph().v_size == 0:
                return
            ALL_SCC = ga.connected_components()
            ALL_SCC2 = ga.connected_components()
            assert len(ALL_SCC) == len(ALL_SCC2)
            node = ALL_SCC[0][0]
            ALL_SCC.pop(0)

            # Check that a node in a certain SCC does NOT belong to another SCC.
            for scc in ALL_SCC:
                assert node not in scc
                # self.connected_component_test(ga.get_graph(), scc[0].key)  # TODO: Test each SCC with shortest_path()

        except AssertionError as e:
            print(e)
            print("connected_components() Failed!")
            self.fail()

    def test_algorithms(self, graph: object = None):
        if graph is None:
            graph = self.example_graph()

        algo = GraphAlgo(graph)

        self.test_connected_components(algo.get_graph())  # Tests ALL SCC's On the graph!

        SCC = self.get_max_scc(algo.get_graph())  # Get the largest SCC and test shortest_path() method on it!

        self.test_shortest_path(SCC, graph=algo.get_graph())  # Test all shortest paths on SCC (They All Exist!)

    def test_save_load(self):

        algo = GraphAlgo()

        assert algo.load_from_json('../data/Graphs_no_pos/G_10_80_0.json')
        assert algo.load_from_json('../data/Graphs_on_circle/G_10_80_1.json')
        assert algo.load_from_json('../data/Graphs_random_pos/G_10_80_2.json')

        test = algo.get_graph()  # G_10_80_2
        our_node = None
        for node in test.get_all_v().values():
            our_node = node
            break

        assert test.remove_node(our_node.key)
        algo.save_to_json('../data/G_10_80_0_TEST.json')

        algo.load_from_json('../data/Graphs_no_pos/G_10_80_0.json')
        g1 = algo.get_graph()
        algo.load_from_json('../data/G_10_80_0_TEST.json')
        g2 = algo.get_graph()

        assert not g1 == g2

    """Graph creation methods:"""

    def graph_creator(self, node_size: int = 0, edge_size: int = 0) -> object:
        g1 = DiGraph()

        for i in range(0, node_size):
            g1.add_node(i)

        nodes = self.nodes_to_array(g1)

        counter = 0
        while counter < edge_size:
            r1 = int((r.random() * node_size))
            r2 = int((r.random() * node_size))
            w = (r.random() * 10)
            if g1.add_edge(nodes[r1], nodes[r2], w):
                counter += 1
        return g1

    def nodes_to_array(self, graph: object = None) -> list:
        if graph is None:
            return []

        ans = []

        for key in graph.get_all_v():
            ans.append(key)

        return ans

    def make_graph(self, V: int = 0, E: int = 0) -> object:
        V = V  # Full graph of V vertices
        E = E
        if E > V * (V - 1):
            E = V * (V - 1)
        return self.graph_creator(V, E)

    def example_graph(self) -> object:
        g = DiGraph()
        for i in range(7):
            g.add_node(i)

        g.add_edge(0, 2, 1)
        g.add_edge(2, 0, 1)
        g.add_edge(3, 0, 1)
        g.add_edge(0, 3, 1)
        g.add_edge(6, 0, 1)
        g.add_edge(4, 2, 1)
        g.add_edge(4, 5, 1)
        g.add_edge(1, 4, 1)
        g.add_edge(5, 1, 1)

        return g

    def get_max_scc(self, graph: object = None) -> list:
        if graph is None:
            return None
        algo = GraphAlgo(graph
                         )
        ALL_SCC = algo.connected_components()
        max_scc = 0
        MAX_SCC = []

        for scc in ALL_SCC:
            if len(scc) > max_scc:
                max_scc = len(scc)
                MAX_SCC = scc
        return MAX_SCC
