#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:58:19 2019

@author: adamm
"""
import graph 
import algorithm1 as alg1
#import networkx as nx

N = 7
weight_list = [1, 1, 1, 1, 1, 1, 1]
G = graph.create_graph_with_weight(N, weight_list)
graph.draw(G)
G_comp = graph.fully_connected_graph_from_list(N)
#graph.draw(G_comp)
print('G nodes:', G.nodes())
print('G_comp nodes: ', G_comp.nodes())
DIF = graph.difference(G_comp, G).edges(data='weight', default=1)

Q = set(DIF)
print('Q: ', Q)
#P = alg1.greedy_th(G, Q, 0.1, len(Q))
for i in range(1,len(Q)+1):
    P = alg1.greedy_th(G, Q, 0.1, i)
    print('P: ', P)
    print('i: ', i)
    print('lenP: ', len(P))
    G_copy = G.copy(G)
    for (u,v) in P:
        G_copy.add_edge(u,v, weight=1)
    number_of_spanning_trees = graph.calculate_number_of_spanning_trees(G_copy)
    print(i, '. Number of spanning trees (according to algorithm1): ', number_of_spanning_trees)