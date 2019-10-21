#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:58:19 2019

@author: adamm
"""
import graph 
#import algorithm1 as alg1

N = 7
G = graph.create_star_with_weight(N)
graph.draw(G)
G_comp = graph.complete_graph_from_list(N)
graph.draw(G_comp)
print('G nodes:', G.nodes())
print('G_comp nodes: ', G_comp.nodes())
print('DIF: ', graph.difference(G_comp, G).edges())
#Q = set(G.edges)
#P = alg1.greedy_th_1(G, Q, 0.01, 4)
#print('P: ', P)