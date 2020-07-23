# -*- coding: utf-8 -*-

import graph
import spanning_tree_algorithms as st_alg
import spanning_edge_betweenness_centrality as sp_ebc
import vertex_centrality_to_edge as vertex_cte

from shutil import copyfile
import os
from random import randint
import json
import sys
import networkx as nx
import pandas as pd
import multiprocessing as mp
import time


def save_base_graphs(g, index, run_id, graph_type): 
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    if not os.path.exists('graphs/base'):
        os.makedirs('graphs/base')
    if not os.path.exists('graphs/base/' + str(run_id)):
        os.makedirs('graphs/base/' + str(run_id))
    if not os.path.exists('graphs/base/' + str(run_id) + '/' + str(graph_type)):
        os.makedirs('graphs/base/' + str(run_id) + '/' + str(graph_type))
    
    filename = 'graph_' + str(index) + '.json'
    graph.save_json(filename, g)
    copyfile(filename, './graphs/base/' + str(run_id) + '/' + str(graph_type) + '/' + filename)
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
    
def run_algorithms_and_generate_json_results(graph_container, fix_k):
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
            res = st_alg.graph_enumeration(g_copy, q, i, cpu_number)
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

def create_csv(graph_data, path, run_id, graph_type):
    g_index = list()
    g_k = list()
    g_algorithm = list()
    g_nodes = list()
    g_edges = list()
    g_complementer_edges = list()
    g_added_edges = list()
    g_all_edge_betweenness_centrality = list()
    g_number_of_spanning_trees = list()
    g_time = list()
    g_span_ebc = list()
    g_vertex_degree_mul_to_edge = list()
    g_vertex_degree_add_to_edge = list()
    
    
    for g_data in graph_data:
        g_index.append(g_data['index'])
        g_k.append(g_data['k'])
        g_algorithm.append(g_data['algorithm'])
        g_nodes.append(g_data['nodes'])
        g_edges.append(g_data['edges'])
        g_complementer_edges.append(g_data['complementer_edges'])
        g_added_edges.append(g_data['added_edges'])
        g_all_edge_betweenness_centrality.append(g_data['all_edge_betweenness_centrality'])
        g_number_of_spanning_trees.append(g_data['number_of_spanning_trees'])
        g_time.append(g_data['time'])
        g_span_ebc.append(g_data['spanning_edge_betweenness_centrality'])
        g_vertex_degree_mul_to_edge.append(g_data['vertex_degree_mul_to_edge'])
        g_vertex_degree_add_to_edge.append(g_data['g_vertex_degree_add_to_edge'])
        
    df_graph_data = {
            'id' : g_index,
            'k' : g_k,
            'algorithm' : g_algorithm,
            'nodes' : g_nodes,
            'edges' : g_edges,
            'complementer_edges' : g_complementer_edges,
            'betweenness_centrality (new edges)' : g_added_edges,
            'betweenness_centrality (all edges)' : g_all_edge_betweenness_centrality,
            'number_of_spanning_trees' : g_number_of_spanning_trees,
            'time': g_time,
            'spanning_edge_betweenness_centrality': g_span_ebc,
            'vertex_degree_mul_to_edge': g_vertex_degree_mul_to_edge,
            'vertex_degree_add_to_edge': g_vertex_degree_add_to_edge
        }
    
    df = pd.DataFrame(df_graph_data)
    df.to_csv('./report/' + str(run_id) + '/' + str(graph_type) + '/' + path + '.csv', index=False)

def create_report(graph_container, fix_k, cpu_number, run_id, graph_type):
    if not os.path.exists('report'):
        os.makedirs('report')
        
    if not os.path.exists('report/' + str(run_id)):
        os.makedirs('report/' + str(run_id))
        
    if not os.path.exists('report/' + str(run_id) + '/' + str(graph_type)):
        os.makedirs('report/' + str(run_id) + '/' + str(graph_type))
    
    agl1_graph_data = list()
    greedy_graph_data = list()
    enumeration_graph_data = list()
    
    for index, g in enumerate(graph_container):
        node_number = len(g.nodes())
        g_comp = graph.fully_connected_graph_from_list(node_number)
        dif = graph.difference(g_comp, g).edges(data='weight', default=1)
        
        q = set(dif)
        
        for i in range(1, fix_k):
            start = time.time()
            g_copy = g.copy(g)
            p = st_alg.algorithm_1(g_copy, q, threshold, i)
            number_of_spanning_trees = graph.calculate_number_of_spanning_trees(g_copy)
            edge_betweenness_centrality = nx.edge_betweenness_centrality(g_copy)
            ST = sp_ebc.find_all_spanning_trees(g_copy)
            spanning_edge_betweennes = sp_ebc.get_spanning_edge_betweenness(g_copy, ST)
            vertex_degree_mul_to_edge = vertex_cte.degree_centrality_multiplication(g_copy)
            vertex_degree_add_to_edge = vertex_cte.degree_centrality_add(g_copy)
            new_edge_betweenness_centrality = [
                (edge_key, edge_betweenness_centrality[edge_key]) for p_edge in p for edge_key in edge_betweenness_centrality.keys() if p_edge == edge_key
                ]
            end = time.time()
            agl1_graph_data.append({
                    'index' : index,
                    'algorithm' : 'algorithm_1',
                    'k' : i,
                    'nodes' : list(g_copy.nodes()),
                    'edges' : list(g.edges()),
                    'complementer_edges' : q,
                    'added_edges' : new_edge_betweenness_centrality,
                    'all_edge_betweenness_centrality' : edge_betweenness_centrality,
                    'number_of_spanning_trees' : str(number_of_spanning_trees),
                    'time' : end - start,
                    'spanning_edge_betweenness_centrality' : spanning_edge_betweennes,
                    'vertex_degree_mul_to_edge' : vertex_degree_mul_to_edge,
                    'vertex_degree_add_to_edge' : vertex_degree_add_to_edge
                })
    
        for i in range(1, fix_k):
            start = time.time()
            g_copy = g.copy(g)
            p = st_alg.greedy(g_copy, q, i)
            number_of_spanning_trees = graph.calculate_number_of_spanning_trees(g_copy)
            edge_betweenness_centrality = nx.edge_betweenness_centrality(g_copy)
            ST = sp_ebc.find_all_spanning_trees(g_copy)
            spanning_edge_betweennes = sp_ebc.get_spanning_edge_betweenness(g_copy, ST)
            vertex_degree_mul_to_edge = vertex_cte.degree_centrality_multiplication(g_copy)
            vertex_degree_add_to_edge = vertex_cte.degree_centrality_add(g_copy)
            new_edge_betweenness_centrality = [
                (edge_key, edge_betweenness_centrality[edge_key]) for p_edge in p for edge_key in edge_betweenness_centrality.keys() if p_edge == edge_key
                ]
            end = time.time()
            greedy_graph_data.append({
                    'index' : index,
                    'algorithm' : 'greedy',
                    'k' : i,
                    'nodes' : list(g_copy.nodes()),
                    'edges' : list(g.edges()),
                    'complementer_edges' : q,
                    'added_edges' : new_edge_betweenness_centrality,
                    'all_edge_betweenness_centrality' : edge_betweenness_centrality,
                    'number_of_spanning_trees' : str(number_of_spanning_trees),
                    'time' : end - start,
                    'spanning_edge_betweenness_centrality' : spanning_edge_betweennes,
                    'vertex_degree_mul_to_edge' : vertex_degree_mul_to_edge,
                    'vertex_degree_add_to_edge' : vertex_degree_add_to_edge
                })
            
        for i in range(1, fix_k):
            start = time.time()
            g_copy = g.copy(g)
            res = st_alg.graph_enumeration(g_copy, q, i, cpu_number)
            p = list(res[1])
            number_of_spanning_trees = res[0]

            for (u,v,w) in p[0]:
                g_copy.add_edge(u, v, weight = w)

            edge_betweenness_centrality = nx.edge_betweenness_centrality(g_copy)
            ST = sp_ebc.find_all_spanning_trees(g_copy)
            spanning_edge_betweennes = sp_ebc.get_spanning_edge_betweenness(g_copy, ST)
            vertex_degree_mul_to_edge = vertex_cte.degree_centrality_multiplication(g_copy)
            vertex_degree_add_to_edge = vertex_cte.degree_centrality_add(g_copy)
            p = [x[:2] for x in p[0]]
            
            new_edge_betweenness_centrality = [
                (edge_key, edge_betweenness_centrality[edge_key]) for p_edge in p for edge_key in edge_betweenness_centrality.keys() if p_edge == edge_key
                ]
            end = time.time()
            enumeration_graph_data.append({
                    'index' : index,
                    'algorithm' : 'graph_enumeration',
                    'k' : i,
                    'nodes' : list(g_copy.nodes()),
                    'edges' : list(g.edges()),
                    'complementer_edges' : q,
                    'added_edges' : new_edge_betweenness_centrality,
                    'all_edge_betweenness_centrality' : edge_betweenness_centrality,
                    'number_of_spanning_trees' : str(number_of_spanning_trees),
                    'time' : end - start,
                    'spanning_edge_betweenness_centrality' : spanning_edge_betweennes,
                    'vertex_degree_mul_to_edge' : vertex_degree_mul_to_edge,
                    'vertex_degree_add_to_edge' : vertex_degree_add_to_edge
                })
    
    create_csv(agl1_graph_data, 'algorithm_1', run_id, graph_type)
    create_csv(greedy_graph_data, 'greedy', run_id, graph_type)
    create_csv(enumeration_graph_data, 'enumeration', run_id, graph_type)


if __name__ == "__main__":
    
    if(sys.argv):
        number_of_graphs = int(sys.argv[1])
        lower_node_bound = int(sys.argv[2])
        upper_node_bound = int(sys.argv[3])
        edge_probability = float(sys.argv[4])
        threshold = float(sys.argv[5])
        fix_k = int(sys.argv[6]) + 1
        cpu_number = int(sys.argv[7])
        run_id = int(sys.argv[8])
    else:
        number_of_graphs = 10
        lower_node_bound = 8
        upper_node_bound = 10
        edge_probability = 0.5
        threshold = 0.1
        fix_k = 3
        cpu_number = mp.cpu_count()
        run_id = 0
        
    weight_list = [1 for i in range(upper_node_bound)]
    graph_container = list()
    tree_container = list()
    
    for i in range(number_of_graphs):
        G = graph.generate_random_graph_with_unit_weight(randint(lower_node_bound, upper_node_bound), edge_probability)
        graph_container.append(G)
        save_base_graphs(G,i, run_id, 'erdos-renyi')
    
    #run_algorithms_and_generate_json_results(graph_container, fix_k, cpu_number)
    create_report(graph_container, fix_k, cpu_number, run_id, 'erdos-renyi')
    
    for i in range(number_of_graphs):
        T = nx.random_tree(randint(lower_node_bound, upper_node_bound))
        tree_container.append(T)
        save_base_graphs(T, i, run_id, 'tree')
    
    create_report(tree_container, fix_k, cpu_number, run_id, 'tree')
