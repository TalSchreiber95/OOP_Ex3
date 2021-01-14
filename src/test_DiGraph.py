from unittest import TestCase

from src.DiGraph import DiGraph
import random as r


class TestDiGraph(TestCase):

    def test_get_mc(self):
        g1 = self.example_graph()

        mc_count = g1.get_mc()
        v = g1.v_size
        e = g1.e_size

        g1.remove_node(5)
        g1.remove_edge(1, 4)

        assert v == g1.v_size + 1
        assert e == g1.e_size + 3
        assert mc_count + 2 == g1.mc_size

    def test_remove_node(self):

        g1 = self.example_graph()
        # print(g1.__repr__())

        mc_count = g1.get_mc()
        v = g1.v_size
        e = g1.e_size

        g1.remove_node(0)

        assert v == g1.v_size + 1
        assert e == g1.e_size + 5
        assert mc_count  + 1 == g1.mc_size

    def test_remove_edge(self):

        g1 = self.example_graph()

        mc_count = g1.get_mc()
        v = g1.v_size
        e = g1.e_size

        g1.remove_edge(5, 1)

        assert v == g1.v_size
        assert e == g1.e_size + 1
        assert mc_count + 1 == g1.mc_size

        assert g1.out_edges.get(5).get(1) is None

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
