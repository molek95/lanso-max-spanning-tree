#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:53:26 2020

@author: adam
"""

import networkx as nx

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

def get_spanning_edge_betweenness(G, all_spanning_trees):
    spanning_edge_betweenness_data = list()
    for edge in G.edges:
        edge_sp_counter = 0
        for span_tree in all_spanning_trees:
            if edge in span_tree.edges:
                edge_sp_counter = edge_sp_counter + 1
        spanning_edge_betweennes = edge_sp_counter / len(all_spanning_trees)
        spanning_edge_betweenness_data.append((edge, spanning_edge_betweennes))
    return spanning_edge_betweenness_data
        
"""
N = 5
G = nx.Graph()
G.add_nodes_from([0,1,2,3,4,5])
G.add_edges_from([
    (0,1), (0,2), (0,3), (0,4), (0,5), (1,4), (2,3),
    (1,2), (1,3), (2,5), (3,4), (4,5), (3,5)
])

ST = find_all_spanning_trees(G)
for g in ST:
    print(g.edges)
spanning_edge_betweennes = get_spanning_edge_betweenness(G, ST)
print(spanning_edge_betweennes)
"""
