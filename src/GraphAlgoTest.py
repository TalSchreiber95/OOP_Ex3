import unittest

import random as r

from src.DiGraph import DiGraph, EdgeData
from src.GraphAlgo import GraphAlgo


# This test class will test the algorithms applied to a given weighted, directed graph data structure.
# I'd like to do the following test:
# Create a randomly connected graph, with 10 nodes and [30, 46] edges
# Consider an arbitrary node 'src' from a SCC on the graph.
# Find A strongly Connected Component(SCC) that has more than 3 Nodes. TODO: First test - DONE
# Find all shortest paths(They all exist!), from 'src' to all nodes on that SCC. TODO: Second test
# TODO: All of these tests don't include save() and load() methods!
class GraphAlgoTest(unittest.TestCase):
    if __name__ == '__main__':
        unittest.main()

    def make_graph(self) -> object:
        V = 100
        E = V * 2
        return self.graph_creator(V, r.randint(200, 300))

    def test_load_from_json(self):
        self.fail()

    def test_save_to_json(self):
        self.fail()

    # This test takes a graph and a source node and test it's connectivity component
    # It relies on the fact that there are 3 or more nodes in the SCC of 'src',
    # But if not - The test will blindly pass
    def connected_component_test(self, graph: object = None, src: int = 0):
        try:
            ga = GraphAlgo(graph)
            print("Test connected_component() {}".format(ga.connected_component(src)))

            original_SCC = ga.connected_component(src)
            original_SCC = ga.connected_component(src)
            SCC2 = ga.connected_component(src)
            assert len(original_SCC) == len(SCC2)

            for key in ga.get_graph().get_all_v():
                node = ga.get_graph().get_node(key)
                if node not in original_SCC:  # Then there is no bidirectional path between them!
                    sp1 = ga.shortest_path(src, key)
                    sp2 = ga.shortest_path(key, src)
                    assert len(sp1[1]) == 0 or len(sp2[1]) == 0
                    break  # Do this once

        except Exception as e:
            print(e)
            self.fail(e)

    def connected_components_test(self, graph: object = None):
        if graph is None:
            return
        try:
            print("Test connected_components()")
            ga = GraphAlgo(graph)

            ALL_SCC = ga.connected_components()
            print(ALL_SCC)
            node = ALL_SCC[0][0]
            ALL_SCC.pop(0)

            # Check that a node in a certain SCC does NOT belong to another SCC.
            for scc in ALL_SCC:
                assert node not in scc
                self.connected_component_test(ga.get_graph(), scc[0].key)  # TODO: Test each SCC
                # print("{} is not in {}".format(node.key, scc))

        except AssertionError as e:
            print(e)
            print("connected_components() Failed!")
            self.fail()

    def test_plot_graph(self):
        self.fail()

    def shortest_path_test(self, g: object = None, src: int = 0, nodes: list = None):
        if nodes is None or g is None:
            self.fail("Either the graph or the node list are None")
            return

        ga = GraphAlgo(g)
        try:
            for node in nodes:
                if node.key != src:
                    sp = ga.shortest_path(src, node.key)
                    assert (sp[0] > 0)  # The distance is positive.
                    assert (len(sp[1]) > 1)  # The list must contain more than 2 nodes.

            sp = ga.shortest_path(src, src)
            assert (sp[0] == 0)
            assert (len(sp[1]) == 0)


        except AssertionError as e:
            print("shortest_path() failed!")
            print(e)

    def test_algorithms(self):
        ga = GraphAlgo(self.make_graph())  # Get a random graph.
        print(ga.get_graph().__str__())

        # Find the first SCC list with 4 or more nodes in it
        # If there is none -> continue with any scc that we get.
        for i in range(ga.get_graph().v_size()):
            scc = ga.connected_component(i)
            size_of_scc = len(scc)
            if size_of_scc >= 3:
                break

        # Define a source node 'src' as the first node from the above SCC.
        src = scc[0].key

        # TODO: Test #2: Test all shortest paths on the given node list.
        # Note: All paths must exist by definition of SCC.
        self.shortest_path_test(ga.get_graph(), src, scc)  # test_shortest_path()

        # TODO: Test #3: Remove a node that is in scc, from the graph, and compare with the new list

        self.connected_components_test(ga.get_graph())  # This test includes testing ALL SCC's

    def graph_creator(self, node_size: int = 0, edge_size: int = 0) -> object:
        g1 = DiGraph()

        for i in range(0, node_size):
            g1.add_node(i)

        counter = 0
        while counter < edge_size:

            r1 = int((r.random() * node_size))
            r2 = int((r.random() * node_size))
            w = (r.random() * 10)
            edge = EdgeData(r1, r2, w)
            if edge not in g1.all_out_edges_of_node(r1):
                g1.add_edge(edge.src, edge.dest, edge.weight)
                counter += 1
        return g1
