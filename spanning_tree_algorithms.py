
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
def graph_enumeration(G, Q, k, cpu_number):
    edge_combination = list(itertools.combinations(Q, k))
    pool = mp.Pool(cpu_number)
    max_number_of_spanning_tree = [pool.apply(test_new_edge, args=(edge, G, k)) for edge in edge_combination]
    pool.close()
    pool.join()
    max_number_of_spanning_tree.sort(key=lambda x:x[0])
    max_number_of_spanning_tree = max_number_of_spanning_tree[::-1]
    return max_number_of_spanning_tree[0]

def add_only_one_edge(G, Q):
    graph_container = list()
    for (u,v,w) in Q:
        G_copy = G.copy()
        G_copy.add_edge(u, v, weight = w)
        graph_container.append((G_copy, (u,v,w)))
    return graph_container

def span_with_degree_mul_centrality(G, Q, k=1):
    degree_container = list()
    min_degree_nodes_container = list()
    potential_edge_container = list()
    min_degree_set = set()
    for node in G.nodes:
        degree_container.append((node, G.degree[node]))
    degree_container.sort(key=lambda x:x[1])
    #print(degree_container)
    
    for min_degree_nodes in degree_container:
        if min_degree_nodes[1] == degree_container[0][1]:
            min_degree_nodes_container.append(min_degree_nodes[0])
            min_degree_set.add(degree_container[0][1])
    if len(min_degree_nodes_container) == 1:
        for min_degree_nodes in degree_container:
            if min_degree_nodes[1] == degree_container[1][1]:
                min_degree_nodes_container.append(min_degree_nodes[0])
                min_degree_set.add(degree_container[1][1])
    #print('min_degree_nodes_container', min_degree_nodes_container)
    #print('min_degree_set', min_degree_set)
    min_degree_list = list(min_degree_set)
    for (u,v,w) in Q:
        if u in min_degree_nodes_container and v in min_degree_nodes_container and (G.degree[u] == min_degree_list[0] or G.degree[v] == min_degree_list[0]):
            potential_edge_container.append((u,v, 1))
    #print('potential_edge_container', potential_edge_container)
        
    #print('len(Q)', len(Q))
    #print('len(potential_edge_container)', len(potential_edge_container))
    return potential_edge_container

def span_with_degree_mul_centrality_with_triangle_check(G, Q, k=1):
    degree_container = list()
    min_degree_nodes_container = list()
    potential_edge_container = list()
    min_degree_set = set()
    for node in G.nodes:
        degree_container.append((node, G.degree[node]))
    degree_container.sort(key=lambda x:x[1])
    #print(degree_container)
    
    for min_degree_nodes in degree_container:
        if min_degree_nodes[1] == degree_container[0][1]:
            min_degree_nodes_container.append(min_degree_nodes[0])
            min_degree_set.add(degree_container[0][1])
    if len(min_degree_nodes_container) == 1:
        for min_degree_nodes in degree_container:
            if min_degree_nodes[1] == degree_container[1][1]:
                min_degree_nodes_container.append(min_degree_nodes[0])
                min_degree_set.add(degree_container[1][1])
    #print('min_degree_nodes_container', min_degree_nodes_container)
    #print('min_degree_set', min_degree_set)
    min_degree_list = list(min_degree_set)
    for (u,v,w) in Q:
        if u in min_degree_nodes_container and v in min_degree_nodes_container and (G.degree[u] == min_degree_list[0] or G.degree[v] == min_degree_list[0]):
            potential_edge_container.append((u,v))
    #print('potential_edge_container', potential_edge_container)
        
    #print('len(Q)', len(Q))
    #print('len(potential_edge_container)', len(potential_edge_container))
    triangle_check_for_potential_edges = list()
    for (u,v) in potential_edge_container:
        new_triangle = check_new_edge_forms_triangle(G, u, v)
        if new_triangle:
            triangle_check_for_potential_edges.append((u,v,1))
    return triangle_check_for_potential_edges

def check_new_edge_forms_triangle(G, u, v):
    g_copy = G.copy()
    u_triangle = nx.triangles(g_copy, u)
    v_triangle = nx.triangles(g_copy, v)
    g_copy.add_edge(u,v)
    if nx.triangles(g_copy, u) > u_triangle or nx.triangles(g_copy, v) > v_triangle:
        return False
    return True