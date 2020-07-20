#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:53:26 2020

@author: adam
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.sparse import csr_matrix
from scipy import linalg

def _expand(G, explored_nodes, explored_edges):
    frontier_nodes = list()
    frontier_edges = list()
    for v in explored_nodes:
        for u in nx.neighbors(G,v):
            if not (u in explored_nodes):
                frontier_nodes.append(u)
                frontier_edges.append([(u,v), (v,u)])

    return zip([explored_nodes | frozenset([v]) for v in frontier_nodes], [explored_edges | frozenset(e) for e in frontier_edges])

def find_all_spanning_trees(G, root=0):
    explored_nodes = frozenset([root])
    explored_edges = frozenset([])
    solutions = [(explored_nodes, explored_edges)]

    for ii in range(G.number_of_nodes()-1):
        solutions = [_expand(G, nodes, edges) for (nodes, edges) in solutions]
        solutions = set([item for sublist in solutions for item in sublist])

    return [nx.from_edgelist(edges) for (nodes, edges) in solutions]

# TODO: különböző feszítőfák száma G-ben amiben megtalálható e él / összes különböző feszítőfa meghatározása

"""
def draw_ST(ST):
    for g in ST:
        fig, ax = plt.subplots(1,1)
        nx.draw_networkx(g, with_labels=True, node_size = 200, node_color='orange',font_size=10,ax=ax)
        plt.axis('off')
        plt.title('spanning tree')
        plt.show()
"""
        
N = 5
G = nx.Graph()
G.add_nodes_from([0,1,2,3,4,5])
G.add_edges_from([
    (0,1), (0,2), (0,3), (0,4), (0,5), (1,4), (2,3),
    (1,2), (1,3), (2,5), (3,4), (4,5), (3,5)
])

fig, ax = plt.subplots(1,1)
nx.draw_networkx(G, with_labels=True, node_size = 200, node_color='orange',font_size=10,ax=ax)
plt.axis('off')
plt.title('base')

ST = find_all_spanning_trees(G)
print(len(ST))
for i,span in enumerate(ST):
    print(i, ':', span.edges)