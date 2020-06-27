# -*- coding: utf-8 -*-
"""
    # degree matrix D
    D = np.diag(np.sum(A, axis=0))
    # transition matrix T
    T = np.dot(np.linalg.inv(D), A)
    walkLength = len(G.nodes)
    #define the starting node, say the 0-th
    p = np.array([1, 0, 0, 0, 0]).reshape(-1,1)
    visited = list()
    """
    
import networkx as nx
import numpy as np
import graph as g
import random

def wilson_algorithm(G,r):
    # adjacency matrix A
    A = nx.adj_matrix(G)
    A = A.todense()
    A = np.array(A, dtype = np.float64)
    print('adjacency: ')
    print(A)
    T = nx.Graph()
    T.add_node(r)
    V = list(G.nodes)
    V.remove(r)
    print('V:', V)
    for v in range(1, len(V)):
        random_walk(v, T)
        print('T:', T)
    

#végtelen ciklus, ki kellene javítani
def random_walk(v,T):
    neighbours = list()
    st_list = list()
    st_list.append(v)
    for n in G.neighbors(v):
        neighbours.append({v,n})
    while(st_list[-1] in list(T.nodes())) == False:
        random_number = random.randint(0,len(neighbours)-1)
        v2 = neighbours[random_number]
        for (u,v) in neighbours:
            for tree_node in list(T.nodes()):
                if (u == tree_node) or (v == tree_node):
                    T.add_nodes_from(st_list)
                else:
                    st_list.append(u)
                    st_list.append(v) 
    print('v2:', v2)
    print('neighbours of', v, ': ', neighbours)

#G = g.generate_random_graph_with_weight_1(5, 0.5)
G = nx.Graph()
G.add_nodes_from([0,1,2,3,4, 5])
G.add_edges_from([(1,4),(4,2),(4,0),(0,2),(0,3),(2,3), (4,5)])
for (u,v) in G.edges():
    G.edges[u,v]['weight'] = 1
g.draw(G)
r = list(G.nodes)[0]
wilson_algorithm(G,r)
