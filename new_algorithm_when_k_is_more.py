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
import time

basic_graph_collector = list()
basic_span_collector = list()
correct_span_collector = list()
correct_edge_collector = list()
algorithm_span_collector = list()
algorithm_edge_collector = list()
algorithm_time = list()
improved_algorithm_span_collector = list()
improved_algorithm_edge_collector = list()
improved_algorithm_time = list()
algorithm_1_span_collector = list()
algorithm_1_edge_collector = list()
algorithm_1_time = list()

k = 3
for index in range(10):
    t = graph.create_barabasi_albert_graph(10,2)
    t_copy = t.copy()
    t_copy_2 = t.copy()
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
    start_time = time.time()
    for i in range(1, k + 1):
        u,v,w = st_alg.new_algorithm_with_random_selection(t,dif)
        t.add_edge(u, v)
        edge_collector.append((u,v,w))
        
    algorithm_span = graph.calculate_number_of_spanning_trees(t)
    algorithm_span_collector.append(algorithm_span)
    algorithm_edge_collector.append(edge_collector)
    algorithm_time.append((time.time() - start_time)) 
        
    improved_edge_collector = list()
    start_time = time.time()
    for i in range(1, k + 1):
        u,v,w = st_alg.new_algorithm(t_copy_2,dif)
        t_copy_2.add_edge(u, v)
        improved_edge_collector.append((u,v,w))
    
    improved_algorithm_span = graph.calculate_number_of_spanning_trees(t_copy_2)
    improved_algorithm_span_collector.append(improved_algorithm_span)
    improved_algorithm_edge_collector.append(improved_edge_collector)
    improved_algorithm_time.append((time.time() - start_time))
    
    q = set(dif)
    start_time = time.time()
    p = st_alg.algorithm_1(t_copy, q, 0.5, k)
    for (u,v) in p:
        t_copy.add_edge(u, v)
        
    algorithm_1_span_collector.append(graph.calculate_number_of_spanning_trees(t_copy))
    algorithm_1_edge_collector.append(p)
    algorithm_1_time.append((time.time() - start_time))
    
    
report_data = {
    'basic_graph_collector': basic_graph_collector,
    'basic_span_collector': basic_span_collector,
    'correct_span_collector': correct_span_collector,
    'correct_edge_collector': correct_edge_collector,
    'algorithm_span_collector': algorithm_span_collector,
    'algorithm_edge_collector': algorithm_edge_collector,
    'algorithm_time': algorithm_time,
    'improved_algorithm_span_collector': improved_algorithm_span_collector,
    'improved_algorithm_edge_collector': improved_algorithm_edge_collector,
    'improved_algorithm_time': improved_algorithm_time,
    'algorithm_1_span_collector': algorithm_1_span_collector,
    'algorithm_1_edge_collector': algorithm_1_edge_collector,
    'algorithm_1_time': algorithm_1_time,
}

df = pd.DataFrame(report_data)

if not os.path.exists('improved_algorithm_result'):
    os.makedirs('improved_algorithm_result')
if not os.path.exists('improved_algorithm_result/3'):
    os.makedirs('improved_algorithm_result/3')
df.to_csv('./improved_algorithm_result/3/algorithm_res.csv', index=False)