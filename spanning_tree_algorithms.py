
import networkx as nx
import graph as g
import itertools
import multiprocessing as mp

def algorithm_1(G, Q, e, k):
    q = len(Q)
    if (k > q):
        return 'k is larger then q'
    P = set()
    er_max = 0
    for (u, v, w) in Q:
        # er_temp = G[u][v]['weight'] * nx.resistance_distance(G, u, v)
        er_temp = w * nx.resistance_distance(G, u, v)
        #print('ER (u,v):', (u,v, er_temp))
        if er_temp >= er_max:
            er_max = er_temp
    th = er_max
    # print ('ER max:', er_max)
    while th >= (e/q) * er_max:
        for (u, v, w) in (Q-P):
            if (len(P) < k) and (w * nx.resistance_distance(G, u, v) >= th):
                G.add_edge(u, v, weight=w)
                P.add((u,v))
        th = (1-e)*th
    return P


def greedy(G, Q, k):
    if k > len(Q):
        return 'k is larger then q'
    P = set()
    for index in range(1,k+1):
        spanning_tree_container = list()
        for (u, v, w) in (Q-P):
            G_copy = G.copy()
            G_copy.add_edge(u, v, weight = w)
            current_spanning_tree = g.calculate_number_of_spanning_trees(G_copy)
            spanning_tree_container.append((current_spanning_tree, (u,v,w)))
        most_useful_edge = max(spanning_tree_container, key=lambda item:item[0])[1]
        x = most_useful_edge[0]
        y = most_useful_edge[1]
        w = most_useful_edge[2]
        P.add((x, y))
        G.add_edge(x,y, weight = w)
    return P

def test_new_edge(edge_set, G, k):
    max_number_of_spanning_tree = 0
    G_copy = G.copy(G)
    best_edges = list()
    for (u,v,w) in edge_set:
        G_copy.add_edge(u,v, weight=w)
        number_of_spanning_tree = g.calculate_number_of_spanning_trees(G_copy)
        if (number_of_spanning_tree > max_number_of_spanning_tree):
            max_number_of_spanning_tree = number_of_spanning_tree
            best_edges.clear()
            best_edges.append(edge_set)

    return (max_number_of_spanning_tree, best_edges)

# test_correct_edges
def graph_enumeration(G, Q, k):
    edge_combination = list(itertools.combinations(Q, k))
    pool = mp.Pool(mp.cpu_count())
    max_number_of_spanning_tree = [pool.apply(test_new_edge, args=(edge, G, k)) for edge in edge_combination]
    pool.close()
    pool.join()
    max_number_of_spanning_tree.sort(key=lambda x:x[0])
    max_number_of_spanning_tree = max_number_of_spanning_tree[::-1]
    return max_number_of_spanning_tree[0]

"""
def test_correct_edges(G, Q, k):
    max_number_of_spanning_tree = g.calculate_number_of_spanning_trees(G)
    edge_combination = itertools.combinations(Q, k)
    best_edges = set()
    for edge in edge_combination:
        G_copy = G.copy(G)
        for (u,v,w) in edge:
            G_copy.add_edge(u,v, weight=w)
        number_of_spanning_tree = g.calculate_number_of_spanning_trees(G_copy)
        if (number_of_spanning_tree > max_number_of_spanning_tree):
            max_number_of_spanning_tree = number_of_spanning_tree
            best_edges.clear()
            best_edges.add(edge)
    print('test_correct_edges_ Maximum spanning tree when k =', k, ' is: ', max_number_of_spanning_tree)
    return (max_number_of_spanning_tree, best_edges)
"""