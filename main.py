# -*- coding: utf-8 -*-

import graph
import spanning_tree_algorithms as st_alg
from shutil import copyfile
import os
from random import randint
import json
import sys

def save_base_graphs(g, index): 
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    if not os.path.exists('graphs/base'):
        os.makedirs('graphs/base')
    
    filename = 'graph_' + str(index) + '.json'
    graph.save_json(filename, g)
    copyfile(filename, './graphs/base/' + filename)
    os.remove(filename)
    
def load_base_graphs(filename):
    if not os.path.exists('graphs'):
        raise 'Directory `graphs` not found'
    if not os.path.exists('graphs/base'):
        raise 'Directory `graphs/base` not found'
    return graph.read_json_file('./graphs/base/' + filename)

def save_result(data, index, directory_name, alg_name):
    if not os.path.exists('graphs/' + directory_name):
        os.makedirs('graphs/' + directory_name)
    filename = alg_name + str(index) + '.json'
    json.dump(data, open('./graphs/' + directory_name + '/' + filename, 'w'), indent=2)


if __name__ == "__main__":
    
    fix_k = 5
    
    if(sys.argv and len(sys.argv) == 6):
        number_of_graphs = int(sys.argv[1])
        lower_node_bound = int(sys.argv[2])
        upper_node_bound = int(sys.argv[3])
        edge_probability = float(sys.argv[4])
        threshold = float(sys.argv[5])
    else:
        number_of_graphs = 10
        lower_node_bound = 5
        upper_node_bound = 8
        edge_probability = 0.5
        threshold = 0.1
        
    weight_list = [1 for i in range(upper_node_bound)]
    graph_container = list()
    
    for i in range(number_of_graphs):
        G = graph.generate_random_graph_with_unit_weight(randint(lower_node_bound, upper_node_bound), edge_probability)
        graph_container.append(G)
        save_base_graphs(G,i)
    

    for index,g in enumerate(graph_container):
        node_number = len(g.nodes())
        g_comp = graph.fully_connected_graph_from_list(node_number)
        dif = graph.difference(g_comp, g).edges(data='weight', default=1)
        
        q = set(dif)
        algorithm_1_result_collector = list()
        greedy_result_collector = list()
        total_result_collector = list()
        
        # run algorithm 1
        for i in range(1, fix_k):
            g_copy = g.copy(g)
            p = st_alg.algorithm_1(g_copy, q, threshold, i)
            number_of_spanning_trees = graph.calculate_number_of_spanning_trees(g_copy)
            result = {
                    'graph_name' : 'graph_' + str(index),
                    'number_of_nodes': len(g_copy.nodes()),
                    'k' : i,
                    'P' : list(p),
                    'number_of_spanning_trees' : number_of_spanning_trees,
                    'edge_list' : list(g_copy.edges())
            }
            algorithm_1_result_collector.append(result)
            
        # run greedy
        for i in range(1, fix_k):
            g_copy = g.copy(g)
            p = st_alg.greedy(g_copy, q, i)
            number_of_spanning_trees = graph.calculate_number_of_spanning_trees(g_copy)
            result = {
                    'graph_name' : 'graph_' + str(index),
                    'number_of_nodes': len(g_copy.nodes()),
                    'k' : i,
                    'P' : list(p),
                    'number_of_spanning_trees' : number_of_spanning_trees,
                    'edge_list' : list(g_copy.edges())
            }
            greedy_result_collector.append(result)
            
        for i in range(1, fix_k):
            g_copy = g.copy(g)
            res = st_alg.graph_enumeration(g_copy, q, i)
            result = {
                    'graph_name' : 'graph_' + str(index),
                    'number_of_nodes': len(g_copy.nodes()),
                    'k' : i,
                    'P' : list(res[1]),
                    'number_of_spanning_trees' : res[0],
                    'edge_list': list(g_copy.edges())
            }
            total_result_collector.append(result)
          
        save_result(algorithm_1_result_collector, index, 'algorithm_1', 'algorithm_1_')
        save_result(greedy_result_collector, index, 'greedy', 'greedy_')
        save_result(total_result_collector, index, 'enumeration', 'enumeration_')
        