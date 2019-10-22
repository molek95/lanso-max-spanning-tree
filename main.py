#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:58:19 2019

@author: adamm
"""
import graph 
import algorithm1 as alg1
import numpy as np
import networkx as nx

N = 7
G = graph.create_star_with_weight(N)
graph.draw(G)
G_comp = graph.fully_connected_graph_from_list(N)
graph.draw(G_comp)
print('G nodes:', G.nodes())
print('G_comp nodes: ', G_comp.nodes())
DIF = graph.difference(G_comp, G).edges()
print('DIF: ', DIF)
Q = set(DIF)
P = alg1.greedy_th(G, Q, 0.01, len(Q))

print('P: ', P)
print('lenQ: ', len(Q))
print('lenP: ', len(P))

L = nx.normalized_laplacian_matrix(G)
L1 = np.squeeze(np.asarray(L))
print(L1)
#print(np.linalg.det(L1))