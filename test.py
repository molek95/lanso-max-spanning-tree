# -*- coding: utf-8 -*-

import graph 
import networkx as nx

G = nx.Graph()
G.add_nodes_from([1,2,3,4])
G.add_edge(1,3, weight=1)
G.add_edge(1,4, weight=1)
G.add_edge(2,3, weight=1)
G.add_edge(2,4, weight=1)
G.add_edge(3,4, weight=1)
spanning_trees = graph.calculate_number_of_spanning_trees(G)
print('Number of spanning trees: ', spanning_trees)