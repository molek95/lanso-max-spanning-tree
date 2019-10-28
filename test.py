# -*- coding: utf-8 -*-

import graph 
import networkx as nx
import itertools

G = nx.Graph()
G1 = nx.Graph()
G1.add_nodes_from([1,2,3,4,5,6])
G.add_nodes_from([1,2,3,4])
G.add_edge(1,3, weight=1)
G.add_edge(1,4, weight=1)
G.add_edge(2,3, weight=1)
G.add_edge(2,4, weight=1)
G.add_edge(3,4, weight=1)
spanning_trees = graph.calculate_number_of_spanning_trees(G)
print('Number of spanning trees: ', spanning_trees)
Q={(1,2,1), (3,4,1), (5,6,1)}
edges = itertools.combinations(Q,2)
print('edges:', edges)
for (u,v) in edges:
    G1.add_edge(u,v)
print(G1.edges())