#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:22:38 2020

@author: adam
"""
import spanning_tree_algorithms as st_alg
import networkx as nx
import graph
import eigenvalue_bounds as eb
import random

k = 3
t = graph.create_weighted_barabasi_albert_graph(8,2, 1, 5)
t_copy = t.copy()
t_copy_2 = t.copy()
basic_span = graph.calculate_number_of_spanning_trees(t)

n = len(t.nodes())
g_comp = graph.fully_connected_graph_from_list(n)
dif = graph.difference(g_comp, t).edges(data='weight')
dif = [(u,v, random.randint(1,5)) for u,v, w in dif]
dif = list(dif)
dif_2 = dif.copy()
q = set(dif)
#print('dif ', dif)

P_3 = []
for k in range(1, 3):
    u,v,w = st_alg.weighted_new_algorithm_with_random_selection(t_copy_2, dif_2)
    print('correct random: ', u,v,w)
    dif_2.remove((u,v,w))
    t_copy_2.add_edge(u,v, weight = w)
    P_3.append((u,v))


P = []
for k in range(1, 3):
    u,v,w = st_alg.weighted_new_algorithm(t, dif)
    print('correct det: ', u,v,w)
    dif.remove((u,v,w))
    t.add_edge(u,v, weight = w)
    P.append((u,v))


print('P_det ', P)
print('P_random ', P_3)

    

P_2 = st_alg.algorithm_1(t_copy, q, 0.5, 2)
print('P_2: ', P_2)
for (u,v) in P_2:
    t_copy.add_edge(u,v)
    
print('det: ', graph.calculate_number_of_spanning_trees(t))
print('rand: ', graph.calculate_number_of_spanning_trees(t_copy_2))
print('alg_1: ', graph.calculate_number_of_spanning_trees(t_copy))
"""
span,p = st_alg.diameter_algorithm(t, 4)
print('span: ', span)
print('p: ', p)
correct_span = st_alg.graph_enumeration(t, dif, k, 8)
print(correct_span)
"""
"""
edge_collector = list()
for i in range(1, k + 1):
    #st_alg.new_algorithm(t,dif)
    print('-------------------------------')
    edge = st_alg.new_algorithm(t,dif)
    dif.remove((edge[0], edge[1], 1))
    t.add_edge(edge[0], edge[1])
    print('-------------------------------')
    edge_collector.append((edge[0], edge[1]))
    
#algorithm_span = graph.calculate_number_of_spanning_trees(t)
"""