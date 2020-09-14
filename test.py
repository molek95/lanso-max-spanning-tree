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
k = 3
t = graph.create_barabasi_albert_graph(10,2)
t_copy = t.copy()

basic_span = graph.calculate_number_of_spanning_trees(t)

n = len(t.nodes())
g_comp = graph.fully_connected_graph_from_list(n)
dif = graph.difference(g_comp, t).edges(data='weight', default=1)
dif = list(dif)
#correct_span = st_alg.graph_enumeration(t, dif, k, 8)

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
