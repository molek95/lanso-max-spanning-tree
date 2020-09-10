#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 20:59:10 2020

@author: adam
"""


import spanning_tree_algorithms as st_alg
import graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import vertex_centrality_to_edge as vertex_cte
import os
import seaborn as sns

basic_graph_collector = list()
basic_span_collector = list()
correct_span_collector = list()
correct_edge_collector = list()
algorithm_span_collector = list()
algorithm_edge_collector = list()
algorithm_1_span_collector = list()
algorithm_1_edge_collector = list()

k = 2
for index in range(10):
    t = graph.create_barabasi_albert_graph(10,2)
    t_copy = t.copy()
    basic_graph_collector.append(t.edges)
    
    basic_span = graph.calculate_number_of_spanning_trees(t)
    basic_span_collector.append(basic_span)
    
    n = len(t.nodes())
    g_comp = graph.fully_connected_graph_from_list(n)
    dif = graph.difference(g_comp, t).edges(data='weight', default=1)
    correct_span = st_alg.graph_enumeration(t, dif, k, 8)
    correct_span_collector.append(correct_span[0])
    correct_edge_collector.append(correct_span[1])
    
    edge_collector = list()
    for i in range(1, k + 1):
        u,v,w = st_alg.new_algorithm_with_random_selection(t,dif)
        t.add_edge(u, v)
        edge_collector.append((u,v,w))
        
    algorithm_span = graph.calculate_number_of_spanning_trees(t)
    algorithm_span_collector.append(algorithm_span)
    algorithm_edge_collector.append(edge_collector)
    
    q = set(dif)
    p = st_alg.algorithm_1(t_copy, q, 0.5, k)
    for (u,v) in p:
        t_copy.add_edge(u, v)
        
    algorithm_1_span_collector.append(graph.calculate_number_of_spanning_trees(t_copy))
    algorithm_1_edge_collector.append(p)
    
    
report_data = {
    'basic_graph_collector': basic_graph_collector,
    'basic_span_collector': basic_span_collector,
    'correct_span_collector': correct_span_collector,
    'correct_edge_collector': correct_edge_collector,
    'algorithm_span_collector': algorithm_span_collector,
    'algorithm_edge_collector': algorithm_edge_collector,
    'algorithm_1_span_collector': algorithm_1_span_collector,
    'algorithm_1_edge_collector': algorithm_1_edge_collector,
}

df = pd.DataFrame(report_data)

if not os.path.exists('algorithm_result'):
    os.makedirs('algorithm_result')
df.to_csv('./algorithm_result/algorithm_res.csv', index=False)