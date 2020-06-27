
import networkx as nx
import graph as g

"""
def greedy_th(G,Q,e,k):
    q = len(Q)
    P = set()
    er_max = 0
    for (u,v) in Q:
        er_temp = nx.resistance_distance(G,u,v)
        if er_temp >= er_max:
            er_max = er_temp
    th = er_max
    while th >= (e/q)*er_max:
        for (u,v) in (Q-P):
            if (len(P)< k) and (nx.resistance_distance(G,u,v) >= th):
                G.add_edge(u,v)
                P.add((u,v))
        th=(1-e)*th
    return P

"""
"""
@input:
    G: G=(V,E), connected graph
    Q: A candidate edge set with |Q| = q.
    e: Error parameter
    k: Number of edges to add
@output:
    P: A subset of Q with most k edges
"""
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