#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:58:19 2019

@author: adamm
"""
import graph 
import algorithm1 as alg1

if __name__ == "__main__":

    N = 7
    weight_list = [1, 1, 1, 1, 1, 1, 1]
    G = graph.create_graph_with_weight(N, weight_list)
    graph.draw(G)
    G_comp = graph.fully_connected_graph_from_list(N)
    #print('G nodes:', G.nodes())
    #print('G_comp nodes: ', G_comp.nodes())
    DIF = graph.difference(G_comp, G).edges(data='weight', default=1)
    
    Q = set(DIF)
    #print('Q: ', Q)
    
    G_test = G.copy(G)

    for i in range(1,len(Q)+1):
        G_copy = G.copy(G)
        P = alg1.greedy_th(G_copy, Q, 0.1, i)
        number_of_spanning_trees = graph.calculate_number_of_spanning_trees(G_copy)
        print('Number of spanning trees (according to algorithm1), when k =',i, ' is: ' ,number_of_spanning_trees)
        print('G: ', G_copy.edges())
    for i in range(1, len(Q)+1):
        graph.test_correct_edges(G_test, Q, i)