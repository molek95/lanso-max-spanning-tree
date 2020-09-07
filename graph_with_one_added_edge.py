#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:41:25 2020

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
from shutil import copyfile
import gershgorin
import networkx as nx
import eigenvalue_bounds as eb


def eigenvalue_report(graph_container, run_id, title):
    edges = list()
    span_trees = list()
    new_edge = list()
    eigenv_1 = list()
    eigenv_2 = list()
    eigenv_3 = list()
    eigenv_4 = list()
    eigenv_5 = list()
    eigenv_6 = list()
    eigenv_7 = list()
    eigenv_8 = list()
    eigenv_9 = list()
    eigenv_10 = list()
    eigenv_11 = list()
    eigenv_12 = list()
    eigenv_13 = list()
    eigenv_14 = list()
    eigenv_15 = list()
    lower_bound_largest_laplacian_eigenv = list()
    lower_bound_second_largest_laplacian_eigenv = list()
    lower_bound_second_smallest_laplacian_eigenv = list()
    lower_bound_for_second_smallest_laplacian_eigenvalue_diam = list()
    
    for g in graph_container:
        eigenv = graph.eigenvalues_of_laplacian(g[0])
        num_of_span = graph.calculate_number_of_spanning_trees(g[0])
        edges.append(g[0].edges())
        eigenv_1.append(eigenv[0].real)
        eigenv_2.append(eigenv[1].real)
        eigenv_3.append(eigenv[2].real)
        eigenv_4.append(eigenv[3].real)
        eigenv_5.append(eigenv[4].real)
        eigenv_6.append(eigenv[5].real)
        eigenv_7.append(eigenv[6].real)
        eigenv_8.append(eigenv[7].real)
        eigenv_9.append(eigenv[8].real)
        eigenv_10.append(eigenv[9].real)
        eigenv_11.append(eigenv[10].real)
        eigenv_12.append(eigenv[11].real)
        eigenv_13.append(eigenv[12].real)
        eigenv_14.append(eigenv[13].real)
        eigenv_15.append(eigenv[14].real)
        span_trees.append(num_of_span)
        new_edge.append(g[1])
        lower_bound_largest_laplacian_eigenv.append(eb.lower_bound_for_largest_laplacian_eigenvalue(g[0]))
        lower_bound_second_largest_laplacian_eigenv.append(eb.lower_bound_for_second_largest_laplacian_eigenvalue(g[0]))
        lower_bound_second_smallest_laplacian_eigenv.append(eb.bound_for_second_smallest_laplacian_eigenvalue(g[0])[0])
        lower_bound_for_second_smallest_laplacian_eigenvalue_diam.append(eb.lower_bound_for_second_smallest_laplacian_eigenvalue_diam(g[0]))
    
    report_data = {
        'added': new_edge,
        'edges': edges,
        'eigenv_1': eigenv_1,
        'eigenv_2': eigenv_2,
        'eigenv_3': eigenv_3,
        'eigenv_4': eigenv_4,
        'eigenv_5': eigenv_5,
        'eigenv_6': eigenv_6,
        'eigenv_7': eigenv_7,
        'eigenv_8': eigenv_8,
        'eigenv_9': eigenv_9,
        'eigenv_10': eigenv_10,
        'eigenv_11': eigenv_11,
        'eigenv_12': eigenv_12,
        'eigenv_13': eigenv_13,
        'eigenv_14': eigenv_14,
        'eigenv_15': eigenv_15,
        'span_trees': span_trees,
        'lower_bound_largest_laplacian_eigenv' : lower_bound_largest_laplacian_eigenv,
        'lower_bound_second_largest_laplacian_eigenv': lower_bound_second_largest_laplacian_eigenv,
        'lower_bound_second_smallest_laplacian_eigenv': lower_bound_second_smallest_laplacian_eigenv,
        'lower_bound_for_second_smallest_laplacian_eigenvalue_diam': lower_bound_for_second_smallest_laplacian_eigenvalue_diam
    }
    
    df = pd.DataFrame(report_data)
    
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    df.to_csv('./graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'eigenvalues.csv', index=False)
    

def largest_two_eigenvalues_and_span_reprort(graph_container, run_id, title):
    largest_eigenvalue = list()
    second_largest_eigenvalue = list()
    span_trees = list()
    diff = list()
    for g in graph_container:
        eigenv = graph.eigenvalues_of_laplacian(g[0])
        num_of_span = graph.calculate_number_of_spanning_trees(g[0])
        largest_eigenvalue.append(eigenv[0])
        second_largest_eigenvalue.append(eigenv[1])
        span_trees.append(num_of_span)
        eigen_diff = eigenv[0] - eigenv[1]
        diff.append(eigen_diff)
    
    report_data = {
        'eigenvalue_1': largest_eigenvalue,
        'eigenvalue_2': second_largest_eigenvalue,
        'diff': diff,
        'span_trees': span_trees
    }
    
    df = pd.DataFrame(report_data)
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    df.to_csv('./graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'largest_eigenvalues.csv', index=False)

def scatterplot_for_degree_mul_centrality_and_span(graph_container, run_id, title, total_edges):
    edge_centrality = list()
    span_number = list()
    for g in graph_container:
        g_copy = g[0].copy()
        centrality = vertex_cte.degree_centrality_multiplication(g_copy)
        current_centrality = [round(centrality[(u,v)], 4) for (u,v) in g_copy.edges() if u == g[1][0] and v == g[1][1]]
        num_of_span = graph.calculate_number_of_spanning_trees(g_copy)
        edge_centrality.append(current_centrality)
        span_number.append(num_of_span)
    
    df = pd.DataFrame()
    df['centrality'] = np.array(edge_centrality).reshape(np.array(edge_centrality).shape[0])
    df['span'] = np.array(span_number)
    
    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.27)
    sns.set(style="white", color_codes=True)
    sns.stripplot(x='centrality', y='span', data=df, jitter=0.5, palette="Set2", dodge=True, linewidth=1, edgecolor='gray')
    
    plt.xlabel('Degree mul centrality')
    plt.ylabel('Number of span')
    plt.title('Edges: ' + str(total_edges))
    
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    plt.savefig('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'degree_mul_cte.png')
    plt.clf()
    
def scatterplot_for_degree_add_centrality_and_span(graph_container, run_id, title, total_edges):
    edge_centrality = list()
    span_number = list()
    for g in graph_container:
        g_copy = g[0].copy()
        centrality = vertex_cte.degree_centrality_add(g_copy)
        current_centrality = [round(centrality[(u,v)], 4) for (u,v) in g_copy.edges() if u == g[1][0] and v == g[1][1]]
        num_of_span = graph.calculate_number_of_spanning_trees(g_copy)
        edge_centrality.append(current_centrality)
        span_number.append(num_of_span)
    
    df = pd.DataFrame()
    df['centrality'] = np.array(edge_centrality).reshape(np.array(edge_centrality).shape[0])
    df['span'] = np.array(span_number)

    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.27)
    sns.set(style="white", color_codes=True)
    sns.stripplot(x='centrality', y='span', data=df, jitter=0.5, palette="Set2", dodge=True, linewidth=1, edgecolor='gray')
    
    plt.xlabel('Degree mul centrality')
    plt.ylabel('Number of span')
    plt.title('Edges: ' + str(total_edges))
    
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    plt.savefig('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'degree_add_cte.png')
    plt.clf()

"""
def scatterplot_for_eigenvector_add_centrality_and_span(graph_container, run_id, title):
    edge_centrality = list()
    span_number = list()
    for g in graph_container:
        g_copy = g[0].copy()
        centrality = vertex_cte.eigenvector_centrality_add(g_copy)
        current_centrality = [(centrality[(u,v)]) for (u,v) in g_copy.edges() if u == g[1][0] and v == g[1][1]]
        num_of_span = graph.calculate_number_of_spanning_trees(g_copy)
        edge_centrality.append(current_centrality)
        span_number.append(num_of_span)
    cent = np.array(edge_centrality)
    span = np.array(span_number)
    colors = np.random.rand(len(graph_container))
    area = (30 * np.random.rand(len(graph_container)))
    plt.scatter(cent, span, s=area, c=colors, alpha=0.5)
    #plt.show()
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    plt.savefig('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'eigenvector_add_cte.png')
    plt.clf()


def scatterplot_for_eigenvector_mul_centrality_and_span(graph_container, run_id, title):
    edge_centrality = list()
    span_number = list()
    for g in graph_container:
        g_copy = g[0].copy()
        centrality = vertex_cte.eigenvector_centrality_mul(g_copy)
        current_centrality = [(centrality[(u,v)]) for (u,v) in g_copy.edges() if u == g[1][0] and v == g[1][1]]
        num_of_span = graph.calculate_number_of_spanning_trees(g_copy)
        edge_centrality.append(current_centrality)
        span_number.append(num_of_span)
    cent = np.array(edge_centrality)
    span = np.array(span_number)
    colors = np.random.rand(len(graph_container))
    area = (30 * np.random.rand(len(graph_container)))
    plt.scatter(cent, span, s=area, c=colors, alpha=0.5)
    #plt.show()
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    plt.savefig('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'eigenvector_mul_cte.png')
    plt.clf()
"""

for i in range(10):
    t = graph.create_barabasi_albert_graph(15, 2)
    
    if not os.path.exists('barabasi_albert_graph'):
        os.makedirs('barabasi_albert_graph')
    filename = 'barabasi_albert' + str(i) + '.json'
    graph.save_json(filename, t)
    copyfile(filename, './barabasi_albert_graph/' + filename)
    os.remove(filename)
    
    n = len(t.nodes())
    g_comp = graph.fully_connected_graph_from_list(n)
    dif = graph.difference(g_comp, t).edges(data='weight', default=1)
    
    potential_edges = st_alg.span_with_degree_mul_centrality(t,dif)
    triangle_check = st_alg.span_with_degree_mul_centrality_with_triangle_check(t,dif)
    eigenv_check = st_alg.lowest_eigen_filter(t, dif)
        
    graph_container = st_alg.add_only_one_edge(t, dif)
    graph_container_copy = graph_container.copy()
    graph_container_copy.insert(0, (t, 'base'))
    """
    for index, G in enumerate(graph_container_copy):
        L = nx.laplacian_matrix(G[0]).toarray()
        print(L)
        gersh = gershgorin.GregsCircles(L)
        gershgorin.plotCircles(gersh, i, 'all_edges', index)
    """
    eigenvalue_report(graph_container_copy, i, 'all_edges')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'all_edges')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'all_edges', len(dif))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'all_edges', len(dif))
    #scatterplot_for_eigenvector_add_centrality_and_span(graph_container, i, 'all_edges')
    #scatterplot_for_eigenvector_mul_centrality_and_span(graph_container, i, 'all_edges')
    
    graph_container = st_alg.add_only_one_edge(t, potential_edges)
    graph_container_copy = graph_container.copy()
    graph_container_copy.insert(0, (t, 'base'))

    """
    for index, G in enumerate(graph_container_copy):
        L = nx.laplacian_matrix(G[0]).toarray()
        gersh = gershgorin.GregsCircles(L)
        gershgorin.plotCircles(gersh, i, 'potential_edges', index)
        
    """    
    eigenvalue_report(graph_container_copy, i, 'potential_edges')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'potential_edges')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'potential_edges', len(potential_edges))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'potential_edges', len(potential_edges))
    #scatterplot_for_eigenvector_add_centrality_and_span(graph_container, i, 'potential_edges')
    #scatterplot_for_eigenvector_mul_centrality_and_span(graph_container, i, 'potential_edges')
    
    graph_container = st_alg.add_only_one_edge(t, triangle_check)
    graph_container_copy = graph_container.copy()
    graph_container_copy.insert(0, (t, 'base'))

    """
    for index, G in enumerate(graph_container_copy):
        L = nx.laplacian_matrix(G[0]).toarray()
        gersh = gershgorin.GregsCircles(L)
        gershgorin.plotCircles(gersh, i, 'triangle_check', index)
    """    
        
    eigenvalue_report(graph_container_copy, i, 'triangle_check')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'triangle_check')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'triangle_check', len(triangle_check))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'triangle_check', len(triangle_check))
    
    graph_container = st_alg.add_only_one_edge(t, eigenv_check)
    graph_container_copy = graph_container.copy()
    graph_container_copy.insert(0, (t, 'base'))

    """
    for index, G in enumerate(graph_container_copy):
        L = nx.laplacian_matrix(G[0]).toarray()
        gersh = gershgorin.GregsCircles(L)
        gershgorin.plotCircles(gersh, i, 'triangle_check', index)
    """    
        
    eigenvalue_report(graph_container_copy, i, 'eigenv_check')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'eigenv_check')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'eigenv_check', len(eigenv_check))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'eigenv_check', len(eigenv_check))