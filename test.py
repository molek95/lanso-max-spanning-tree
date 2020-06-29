# -*- coding: utf-8 -*-

import graph 
from random import randint, seed
import networkx as nx
import spanning_tree_algorithms as st_alg
from shutil import copyfile
import os
import json
import multiprocessing as mp
from time import time

"""
graph_container = list()

for i in range(100):
    G = graph.generate_random_graph(randint(10, 100), 0.5)
    #graph.draw(G)
    graph_container.append(G)
    
print('container length', len(graph_container))

for i,g in enumerate(graph_container):
    print(i, '. graph nodes: ', len(g.nodes))
"""
###############
"""
N = 15
G2 = graph.generate_random_graph(N, 0.5)
graph.draw(G2)
G_comp = graph.fully_connected_graph_from_list(N)
graph.draw(G_comp)
DIF = graph.difference(G_comp, G2).edges(data='weight', default=1)

Q = set(DIF)

G3 = G2.copy()
G4 = G2.copy()

P1 = st_alg.greedy(G3,Q,len(Q))
P2 = st_alg.algorithm_1(G4,Q, 0.1, len(Q))
print('P1: ', P1)
print('P2: ', P2)

graph.draw(G2)
"""
"""
if not os.path.exists('graphs'):
    os.makedirs('graphs')

if not os.path.exists('graphs/base'):
    os.makedirs('graphs/base')

filename = 'test_graph_' + str(1) + '.json'
graph.save_json(filename, G2)
copyfile(filename, './graphs/base/' + filename)
G3 = graph.read_json_file('./graphs/base/' + filename)
os.remove(filename)
graph.draw(G3)
"""
"""
test_res = list()
test_res.append({
        'graph_name' : 'asd',
        'k' : 3,
        'P' : 2,
        'number_of_spanning_trees' : 5,
        'edge_list' : [(1,2), (3,4)]
})
test_res.append({
    'graph_name' : 'asd',
    'k' : 3,
    'P' : 2,
    'number_of_spanning_trees' : 5,
    'edge_list' : [(1,2), (3,4)]
})
print(test_res)
json.dump(test_res, open('asd.json', 'w'))
"""

print('Number of processors: ', mp.cpu_count())

G = graph.read_json_file('./graphs/base/graph_0.json')
N = len(G.nodes)
G_comp = graph.fully_connected_graph_from_list(N)
DIF = graph.difference(G_comp, G).edges(data='weight', default=1)
graph.draw(G)
Q = set(DIF)

print('base spanning trees: ', graph.calculate_number_of_spanning_trees(G))
spanning_tree = st_alg.test_correct_edges(G, Q, 2)
print('spanning tree: ', spanning_tree[0])
#print('edges: ', spanning_tree[1])
for edge in spanning_tree[1]:
    print(edge)

G.add_edge(2, 5, weight=1)
G.add_edge(2, 3, weight=1)
print(graph.calculate_number_of_spanning_trees(G))
"""
print('base spanning trees: ', graph.calculate_number_of_spanning_trees(G))
spanning_tree = st_alg.graph_enumeration(G, Q, 2)
print(spanning_tree)
"""
"""
for i in range(0,3):
    spanning_tree = st_alg.graph_enumeration(G, Q, i)
    print(spanning_tree)
"""