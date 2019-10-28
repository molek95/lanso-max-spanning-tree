
import networkx as nx
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
def greedy_th(G, Q, e, k):
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
