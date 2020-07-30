#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:34:13 2020

@author: adam
"""

import networkx as nx

def degree_centrality_multiplication(G):
    degree_centrality_to_edges = dict()
    degree_centrality = nx.degree_centrality(G)
    for (u,v) in G.edges:
        edge_centrality = degree_centrality[u] * degree_centrality[v]
        #degree_centrality_to_edges.append(((u,v), edge_centrality))
        edge = (u,v)
        degree_centrality_to_edges[edge] = edge_centrality
    return degree_centrality_to_edges

def degree_centrality_add(G):
    degree_centrality_to_edges = dict()
    degree_centrality = nx.degree_centrality(G)
    for (u,v) in G.edges:
        edge_centrality = degree_centrality[u] + degree_centrality[v]
        #degree_centrality_to_edges.append(((u,v), edge_centrality))
        edge = (u,v)
        degree_centrality_to_edges[edge] = edge_centrality
    return degree_centrality_to_edges

"""
N = 5
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edges_from([
    (1,2), (1,3), (1,4), (1,5), (1,6), (2,5), (3,4),
    (2,3), (2,4), (3,6), (4,5), (5,6), (4,6)
])

a = degree_centrality_multiplication(G)
print(a)
print('----------')
b = degree_centrality_add(G)
print(b)
"""