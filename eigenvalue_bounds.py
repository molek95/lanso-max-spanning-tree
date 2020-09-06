#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:30:29 2020

@author: adam
"""

import networkx as nx
import math

def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

# (30) lower bound
def lower_bound_for_largest_laplacian_eigenvalue(G):
    lower_bound_collector = list()
    for (u,v) in G.edges:
        u_neighbors = [n for n in G.neighbors(u)]
        v_neighbors = [n for n in G.neighbors(v)]
        u_v_intersect = intersection(u_neighbors, v_neighbors)
        cuv = G.degree(u) - len(u_v_intersect) - 1
        cvu = G.degree(v) - len(u_v_intersect) - 1
        tu = (G.degree(u) * G.degree(u)) + (2 * G.degree(u))
        temp_val_1 = tu + ( (2 * G.degree(v) + 4) * (2 * G.degree(v) + 4) ) + (4 * cuv * cvu)
        temp_val_2 = 0.5 * (tu - (2 * G.degree(v)) - 2 + math.sqrt(temp_val_1))
        bound = math.sqrt(temp_val_2)
        lower_bound_collector.append(bound)
    
    return max(lower_bound_collector)

# (42)
def lower_bound_for_second_largest_laplacian_eigenvalue(G):
    degree_collector = [(v, G.degree(v)) for v in G.nodes]
    degree_col = sorted(degree_collector, key=lambda item: item[1], reverse=True)
    u = degree_col[0][0]
    v = degree_col[1][0]
    u_neighbors = [n for n in G.neighbors(u)]
    v_neighbors = [n for n in G.neighbors(v)]
    cuv = len(intersection(u_neighbors, v_neighbors))
    
    if G.has_edge(u,v):
        return (G.degree(v) + 2 + math.sqrt( ((G.degree(v) - 2) * (G.degree(v) - 2)) + 4 * cuv )) / 2
    else:
        return (G.degree(v) + 1 + math.sqrt( ((G.degree(v) - 1) * (G.degree(v)) - 1) - 4 * cuv )) / 2

# (48)
def bound_for_second_smallest_laplacian_eigenvalue(G):
    n = len(G.nodes())
    vertex_connectivity = nx.node_connectivity(G)
    edge_connectivity = nx.edge_connectivity(G)
    lower_bound = 2 * (edge_connectivity) * (1 - math.cos(math.pi / n))
    upper_bound = vertex_connectivity
    return lower_bound, upper_bound

# (51)
def lower_bound_for_second_smallest_laplacian_eigenvalue_diam(G):
    n = len(G.nodes())
    m = len(G.edges())
    return (2 * n) / (2 + n*(n-1) * (nx.diameter(G) - 2 * m * (nx.diameter(G))))