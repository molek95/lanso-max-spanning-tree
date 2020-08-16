#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:22:38 2020

@author: adam
"""
import spanning_tree_algorithms as st_alg
import networkx as nx
import graph

t = graph.create_barabasi_albert_tree(10)
n = len(t.nodes())
g_comp = graph.fully_connected_graph_from_list(n)
dif = graph.difference(g_comp, t).edges(data='weight', default=1)

potential_edges = st_alg.span_with_degree_mul_centrality(t,dif)
