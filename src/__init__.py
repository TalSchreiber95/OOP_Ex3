from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo

g1 = DiGraph()
g1.add_node(0)
g1.add_node(1)
g1.add_node(2)
g1.add_node(3)
g1.add_node(4)

g1.add_edge(0, 1, 1)
g1.add_edge(1, 2, 2)
g1.add_edge(2, 3, 1)
g1.add_edge(2, 1, 1)
g1.add_edge(0, 4, 2)
g1.add_edge(4, 0, 3)
g1.add_edge(4, 2, 0.1)
g1.add_edge(2, 4, 2)
g1.add_edge(0, 1, 1)
g1.add_edge(1, 0, 1)
g1.add_edge(0, 2, 1)

ga = GraphAlgo(g1)

print("Created the graph")