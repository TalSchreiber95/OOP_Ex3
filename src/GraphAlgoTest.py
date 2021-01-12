import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class GraphAlgoTest(unittest.TestCase):
    if __name__ == '__main__':
        unittest.main()

    def make_graph(self) -> object:
        g1 = DiGraph()
        g1.add_node(0)
        g1.add_node(1)
        g1.add_node(2)
        g1.add_node(3)
        g1.add_node(4)

        g1.add_edge(0, 1, 1)
        g1.add_edge(1, 2, 2)
        g1.add_edge(2, 3, 1)
        # g1.add_edge(2, 1, 1)
        g1.add_edge(0, 4, 2)
        g1.add_edge(4, 0, 3)
        # g1.add_edge(4, 2, 0.1)
        g1.add_edge(2, 4, 2)
        g1.add_edge(0, 1, 1)
        g1.add_edge(1, 0, 1)
        g1.add_edge(0, 2, 1)
        return g1

    def test_load_from_json(self):
        self.fail()

    def test_save_to_json(self):
        self.fail()

    def test_shortest_path(self):
        print("Test shortest_path()")
        ga = GraphAlgo(self.make_graph())
        # print(ga.shortest_path(1, 3))
        ga.load_from_json('../data/A5.txt')
        print(ga.shortest_path(0, 2))

    def test_connected_component(self):
        self.fail()

    def test_connected_components(self):
        self.fail()

    def test_plot_graph(self):
        self.fail()
