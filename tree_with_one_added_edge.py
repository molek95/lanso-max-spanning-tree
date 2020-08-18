#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:43:10 2020

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

def eigenvalue_report(graph_container, run_id, title):
    edges = list()
    eigenvalues = list()
    span_trees = list()
    new_edge = list()
    for g in graph_container:
        eigenv = graph.eigenvalues_of_laplacian(g[0])
        num_of_span = graph.calculate_number_of_spanning_trees(g[0])
        edges.append(g[0].edges())
        eigenvalues.append(eigenv)
        span_trees.append(num_of_span)
        new_edge.append(g[1])
    
    report_data = {
        'added': new_edge,
        'edges': edges,
        'eigenvalues': eigenvalues,
        'span_trees': span_trees
    }
    
    df = pd.DataFrame(report_data)
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    df.to_csv('./tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'eigenvalues.csv', index=False)

def largest_two_eigenvalues_and_span_reprort(graph_container, run_id, title):
    largest_eigenvalue = list()
    second_largest_eigenvalue = list()
    span_trees = list()
    for g in graph_container:
        eigenv = graph.eigenvalues_of_laplacian(g[0])
        num_of_span = graph.calculate_number_of_spanning_trees(g[0])
        largest_eigenvalue.append(eigenv[0])
        second_largest_eigenvalue.append(eigenv[1])
        span_trees.append(num_of_span)
    
    report_data = {
        'eigenvalue_1': largest_eigenvalue,
        'eigenvalue_2': second_largest_eigenvalue,
        'span_trees': span_trees
    }
    
    df = pd.DataFrame(report_data)
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    df.to_csv('./tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'largest_eigenvalues.csv', index=False)

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
    df['centrality'] = np.array(edge_centrality)[:,0]
    df['span'] = np.array(span_number)
    
    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.27)
    sns.set(style="white", color_codes=True)
    sns.stripplot(x='centrality', y='span', data=df, jitter=0.5, palette="Set2", dodge=True, linewidth=1, edgecolor='gray')
    
    plt.xlabel('Degree mul centrality')
    plt.ylabel('Number of span')
    plt.title('Edges: ' + str(total_edges))
    
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    plt.savefig('tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'degree_mul_cte.png')
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
    df['centrality'] = np.array(edge_centrality)[:,0]
    df['span'] = np.array(span_number)
    
    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.27)
    sns.set(style="white", color_codes=True)
    sns.stripplot(x='centrality', y='span', data=df, jitter=0.5, palette="Set2", dodge=True, linewidth=1, edgecolor='gray')
    
    plt.xlabel('Degree mul centrality')
    plt.ylabel('Number of span')
    plt.title('Edges: ' + str(total_edges))
    
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    plt.savefig('tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'degree_add_cte.png')
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
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    plt.savefig('tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'eigenvector_add_cte.png')
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
    if not os.path.exists('tree_with_one_added'):
        os.makedirs('tree_with_one_added')
    if not os.path.exists('tree_with_one_added/' + str(run_id)):
        os.makedirs('tree_with_one_added/' + str(run_id))
    if not os.path.exists('tree_with_one_added/' + str(run_id) + '/' + str(title)):
        os.makedirs('tree_with_one_added/' + str(run_id) + '/' + str(title))
    plt.savefig('tree_with_one_added/' + str(run_id) + '/' + str(title) + '/' + 'eigenvector_mul_cte.png')
    plt.clf()    
"""
for i in range(10):
    t = graph.create_barabasi_albert_tree(15)
    n = len(t.nodes())
    g_comp = graph.fully_connected_graph_from_list(n)
    dif = graph.difference(g_comp, t).edges(data='weight', default=1)
    
    potential_edges = st_alg.span_with_degree_mul_centrality(t,dif)
    
    graph_container = st_alg.add_only_one_edge(t, dif)
    eigenvalue_report(graph_container, i, 'all_edges')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'all_edges')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'all_edges', len(dif))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'all_edges', len(dif))
    #scatterplot_for_eigenvector_add_centrality_and_span(graph_container, i, 'all_edges')
    #scatterplot_for_eigenvector_mul_centrality_and_span(graph_container, i, 'all_edges')
    
    graph_container = st_alg.add_only_one_edge(t, potential_edges)
    eigenvalue_report(graph_container, i, 'potential_edges')
    largest_two_eigenvalues_and_span_reprort(graph_container, i, 'potential_edges')
    scatterplot_for_degree_mul_centrality_and_span(graph_container, i, 'potential_edges', len(potential_edges))
    scatterplot_for_degree_add_centrality_and_span(graph_container, i, 'potential_edges', len(potential_edges))
    #scatterplot_for_eigenvector_add_centrality_and_span(graph_container, i, 'potential_edges')
    #scatterplot_for_eigenvector_mul_centrality_and_span(graph_container, i, 'potential_edges')

