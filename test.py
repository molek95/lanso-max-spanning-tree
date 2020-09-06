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

t = graph.create_barabasi_albert_graph(10,2)
#graph.draw(t)
    
lb = eb.lower_bound_for_largest_laplacian_eigenvalue(t)
print('lower bound: ', lb)
lb2 = eb.lower_bound_for_second_largest_laplacian_eigenvalue(t)
print('second lower bound: ', lb2)
lb3, ub = eb.bound_for_second_smallest_laplacian_eigenvalue(t)
print('lb3: ', lb3)
print('ub: ', ub)
lb4 = eb.lower_bound_for_second_smallest_laplacian_eigenvalue_diam(t)
print('lb4: ', lb4)
"""
n = len(t.nodes())
g_comp = graph.fully_connected_graph_from_list(n)
dif = graph.difference(g_comp, t).edges(data='weight', default=1)

potential_edges = st_alg.span_with_degree_mul_centrality(t,dif)
"""