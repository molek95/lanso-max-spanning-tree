#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:11:46 2020

@author: adam
"""


import graph
import spanning_tree_algorithms as st_alg
import networkx as nx

filename = 'barabasi_albert0.json'
t = graph.read_json_file('./barabasi_albert_graph/' + filename)
#graph.draw(t)
n = len(t.nodes())
g_comp = graph.fully_connected_graph_from_list(n)
dif = graph.difference(g_comp, t).edges(data='weight', default=1)
    
potential_edges = st_alg.span_with_degree_mul_centrality(t,dif)
print(potential_edges)
"""
potential_edges:  [(4, 13, 1), (4, 12, 1), (4, 14, 1), (4, 11, 1), (11, 14, 1), (11, 13, 1), (11, 12, 1), (12, 14, 1), (12, 13, 1), (13, 14, 1)]
#print(potential_edges)
#12-13 max
all_path = nx.all_pairs_shortest_path(t)
nodes_with_longest_shortest_path = list()

for path in all_path:
    last_key = list(path[1])[-1]
    nodes_with_longest_shortest_path.append((path[0], len(path[1][last_key])))

nodes_with_longest_shortest_path.sort(key=lambda x:x[1], reverse=True)
print(nodes_with_longest_shortest_path)
len_longest_shortest_path = nodes_with_longest_shortest_path[0][1]

potential_nodes = list()
for node_data in nodes_with_longest_shortest_path:
    if node_data[1] == len_longest_shortest_path:
        potential_nodes.append(node_data[0])

print(potential_nodes)

print(graph.calculate_number_of_spanning_trees(t))
print('potential_edges: ', potential_edges)
#span = st_alg.graph_enumeration(t, potential_edges, 1, 8)
#print(span)
print('triangles_1 : ', nx.triangles(t)[4], nx.triangles(t)[11])
t.add_edge(4, 11,weight = 1) # a jó nem növeli a háromszögek számát
#graph.draw(t)

print('triangles_2 : ', nx.triangles(t)[4], nx.triangles(t)[11])
"""