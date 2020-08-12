#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:53:30 2020

@author: adam
"""
import graph
import pandas as pd
import ast

def eigenvalue_report(graph_container, run_id, graph_type):
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
    df.to_csv('./report/' + str(run_id) + '/' + str(graph_type) + '/' + 'eigenvalues.csv', index=False)

def csv_to_dataframe(file, cols):
    df = pd.read_csv(file, usecols = cols)
    return df

def sort_centralities(df, centrality, index):
    centrality_col = df[centrality].to_numpy()
    res = ast.literal_eval(centrality_col[index])
    sorted_res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
    print(sorted_res)
    
#df = csv_to_dataframe('report/12/tree/algorithm_1.csv', ['id','k' ,'betweenness_centrality (all edges)', 'betweenness_centrality (new edges)'])
#print(df)

#sort_centralities(df, 'betweenness_centrality (all edges)', 0)
    