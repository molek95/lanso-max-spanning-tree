#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 20:59:10 2020

@author: adam
"""


import spanning_tree_algorithms as st_alg
import graph
import pandas as pd
import os
import time
import algorithm_analyzer as alg_analize
import sys

def compare_algorithms(k, sample_size, barabasi_albert_n, barabas_albert_m, result_file):
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
    greedy_span_collector = list()
    greedy_edge_collector = list()
    greedy_time = list()
    
    for index in range(sample_size):
        global_start_time = time.time()
        t = graph.create_barabasi_albert_graph(barabasi_albert_n, barabas_albert_m)
        t_copy = t.copy()
        t_copy_2 = t.copy()
        t_copy_3 = t.copy()
        basic_graph_collector.append(t.edges)
        
        basic_span = graph.calculate_number_of_spanning_trees(t)
        basic_span_collector.append(basic_span)
        
        print(str(index+1) + '. graph is created')
        print('time: ', time.time() - global_start_time)
        n = len(t.nodes())
        g_comp = graph.fully_connected_graph_from_list(n)
        dif = graph.difference(g_comp, t).edges(data='weight', default=1)
        dif = list(dif)
        dif_2 = dif.copy()
        dif_3 = dif.copy()
        dif_4 = dif.copy()
        
        correct_span = st_alg.graph_enumeration(t, dif, k, 8)
        correct_span_collector.append(correct_span[0])
        correct_edge_collector.append(correct_span[1])
        
        print('correct spanning tree no. : ', correct_span)
        print('time: ', time.time() - global_start_time)
        
        edge_collector = list()
        start_time = time.time()
        for i in range(1, k + 1):
            edge = st_alg.new_algorithm_with_random_selection(t,dif_2)
            dif_2.remove((edge[0],edge[1],1))
            t.add_edge(edge[0], edge[1])
            edge_collector.append((edge))
        
        print('random_select algorithm res: ', edge_collector)
        print('time: ', time.time() - global_start_time)
            
        algorithm_span = graph.calculate_number_of_spanning_trees(t)
        algorithm_span_collector.append(algorithm_span)
        algorithm_edge_collector.append(edge_collector)
        algorithm_time.append((time.time() - start_time))
        
        print('random select span: ' , algorithm_span)
        print('time: ', time.time() - global_start_time)
            
        improved_edge_collector = list()
        start_time = time.time()
        for i in range(1, k + 1):
            edge = st_alg.new_algorithm(t_copy_2,dif_3)
            dif_3.remove((edge[0], edge[1], 1))
            t_copy_2.add_edge(edge[0], edge[1])
            improved_edge_collector.append(edge)
            
        print('improved algorithm res: ', improved_edge_collector)
        print('time: ', time.time() - global_start_time)
        
        improved_algorithm_span = graph.calculate_number_of_spanning_trees(t_copy_2)
        improved_algorithm_span_collector.append(improved_algorithm_span)
        improved_algorithm_edge_collector.append(improved_edge_collector)
        improved_algorithm_time.append((time.time() - start_time))
        
        print('improved algorithm span: ', improved_algorithm_span)
        print('time: ', time.time() - global_start_time)
        
        q = set(dif)
        start_time = time.time()
        p = st_alg.algorithm_1(t_copy, q, 0.5, k)
        for (u,v) in p:
            t_copy.add_edge(u, v)
            
        print('algorithm1 res: ', p)
        print('time: ', time.time() - global_start_time)
        algorithm_1_span = graph.calculate_number_of_spanning_trees(t_copy)
        algorithm_1_span_collector.append(algorithm_1_span)
        algorithm_1_edge_collector.append(p)
        algorithm_1_time.append((time.time() - start_time))
        
        print('algorithm1 span: ', algorithm_1_span)
        print('time: ', time.time() - global_start_time)
        
        start_time = time.time()
        q_2 = set(dif_3)
        greedy_p = st_alg.greedy(t_copy_3, q_2, k)
        greedy_span = graph.calculate_number_of_spanning_trees(t_copy)
        greedy_span_collector.append(greedy_span)
        greedy_edge_collector.append(greedy_p)
        greedy_time.append((time.time() - start_time))
        
        
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
        'greedy_span_collector': greedy_span_collector,
        'greedy_edge_collector': greedy_edge_collector,
        'greedy_time': greedy_time
    }
    
    df = pd.DataFrame(report_data)
    
    if not os.path.exists('improved_algorithm_result'):
        os.makedirs('improved_algorithm_result')
    if not os.path.exists('improved_algorithm_result/big_graphs'):
        os.makedirs('improved_algorithm_result/big_graphs')
    if not os.path.exists('improved_algorithm_result/big_graphs/' + str(k)):
        os.makedirs('improved_algorithm_result/big_graphs/' + str(k))
    df.to_csv('./improved_algorithm_result/big_graphs/' + str(k) + '/' + str(result_file) + '.csv', index=False)

 
if __name__ == "__main__":
    
    if (sys.argv):
        k = int(sys.argv[1])
        sample_size = int(sys.argv[2])
        barabasi_n = int(sys.argv[3])
        barabasi_m = int(sys.argv[4])
        result_file = str(sys.argv[5])
        report_file = str(sys.argv[6])
    else:
        print('Some parameters are missing')
    
    compare_algorithms(k, sample_size, barabasi_n, barabasi_m, result_file)
    alg_analize.algorithm_evaluation(result_file, report_file, k)
    