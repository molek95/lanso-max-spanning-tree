
import networkx as nx
import graph as g
import itertools
import multiprocessing as mp
import eigenvalue_bounds as eb
import random

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

def lowest_eigen_filter(G, Q, k=1):
    edge_collector = list()
    triangle_check_edges = span_with_degree_mul_centrality_with_triangle_check(G,Q,k)
    #print('triangle_check_edges: ', triangle_check_edges)
    for (u,v,w) in triangle_check_edges:
        g_copy = G.copy()
        g_copy.add_edge(u,v)
        smallest_eig_lower_bound = eb.lower_bound_for_second_smallest_laplacian_eigenvalue_diam(g_copy)
        edge_collector.append(((u,v), smallest_eig_lower_bound))
    edge_collector = sorted(edge_collector, key=lambda item: item[1], reverse=False)
    #print('len(edge_collector): ', len(edge_collector), 'edge_collector: ', edge_collector)    
    potential_edge = [(edge[0][0], edge[0][1], 1) for edge in edge_collector if edge[1] == edge_collector[0][1]]
    #print('len(potential_edge)', len(potential_edge), 'potential_edge: ', potential_edge)
    return potential_edge

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def new_algorithm_with_random_selection(G, Q):
    edge_list = list(span_with_degree_mul_centrality(G, Q))
    
    if len(edge_list) == 1:
        return (edge_list[0][0], edge_list[0][1])
    
    triangle_check_for_potential_edges = list()
    for (u,v,w) in edge_list:
        new_triangle = check_new_edge_forms_triangle(G, u, v)
        if new_triangle:
            triangle_check_for_potential_edges.append((u,v,1))
    
    
    if len(triangle_check_for_potential_edges) == 0:
        triangle_check_for_potential_edges = edge_list
        
    if len(triangle_check_for_potential_edges) == 1:
        return (triangle_check_for_potential_edges[0][0], triangle_check_for_potential_edges[0][1])
    
    
    edge_collector = list()
    for (u,v,w) in triangle_check_for_potential_edges:
        g_copy = G.copy()
        g_copy.add_edge(u,v)
        smallest_eig_lower_bound = eb.lower_bound_for_second_smallest_laplacian_eigenvalue_diam(g_copy)
        edge_collector.append(((u,v), smallest_eig_lower_bound))
    edge_collector = sorted(edge_collector, key=lambda item: item[1], reverse=False)
    eigenv_edge = [(edge[0][0], edge[0][1], 1) for edge in edge_collector if edge[1] == edge_collector[0][1]]
    
    random_edge = random.choice(eigenv_edge)
    return (random_edge[0], random_edge[1])

def _calculate_spanning_tree_with_one_added_edge(u,v,G):
    g_copy = G.copy()
    g_copy.add_edge(u,v)
    return ((u,v), g.calculate_number_of_spanning_trees(g_copy))

def new_algorithm(G,Q, cpu_number=1):
    edge_list = list(span_with_degree_mul_centrality(G, Q))
    #print('span_with_degree_mul: ', edge_list)
    if len(edge_list) == 1:
        print('ret_1: ', (edge_list[0][0], edge_list[0][1]))
        return (edge_list[0][0], edge_list[0][1])
    
    triangle_check_for_potential_edges = list()
    for (u,v,w) in edge_list:
        new_triangle = check_new_edge_forms_triangle(G, u, v)
        if new_triangle:
            triangle_check_for_potential_edges.append((u,v,1))
    
    
    if len(triangle_check_for_potential_edges) == 0:
        triangle_check_for_potential_edges = edge_list
        
    if len(triangle_check_for_potential_edges) == 1:
        print('ret_2: ', (triangle_check_for_potential_edges[0][0], triangle_check_for_potential_edges[0][1]))
        return (triangle_check_for_potential_edges[0][0], triangle_check_for_potential_edges[0][1])
    
    #print('triangle_check_for_potential_edges: ', triangle_check_for_potential_edges)
    edge_collector = list()
    for (u,v,w) in triangle_check_for_potential_edges:
        g_copy = G.copy()
        g_copy.add_edge(u,v)
        smallest_eig_lower_bound = eb.lower_bound_for_second_smallest_laplacian_eigenvalue_diam(g_copy)
        edge_collector.append(((u,v), smallest_eig_lower_bound))
    edge_collector = sorted(edge_collector, key=lambda item: item[1], reverse=False)
    eigenv_edge = [(edge[0][0], edge[0][1], 1) for edge in edge_collector if edge[1] == edge_collector[0][1]]
    #print('eigenv_edge: ', eigenv_edge)
    
    max_number_of_spanning_tree = list()
    g_copy = G.copy()
    pool = mp.Pool(cpu_number)
    max_number_of_spanning_tree = [pool.apply(_calculate_spanning_tree_with_one_added_edge, args=(u, v, g_copy)) for (u,v,w) in eigenv_edge]
    pool.close()
    pool.join()
    max_number_of_spanning_tree.sort(key=lambda x:x[1])
    max_number_of_spanning_tree = max_number_of_spanning_tree[::-1]
    #print('max_number_of_spanning_tree: ', max_number_of_spanning_tree)
    print('ret_3: ', max_number_of_spanning_tree[0][0])
    return max_number_of_spanning_tree[0][0]

def find_largest_path(G):
    max_eccentricity = nx.eccentricity(G)
    max_eccentricity = {k: v for k, v in sorted(max_eccentricity.items(), key=lambda item: item[1], reverse=True)}
    longest_path_vertex = list(max_eccentricity.keys())[0]
    longest_path_length = list(max_eccentricity.values())[1]
    longest_shortest_path = nx.shortest_path(G, source=longest_path_vertex)
    longest_shortest_path = {k: v for k, v in longest_shortest_path.items() if len(v) == longest_path_length + 1}
    longest_path_target = list(longest_shortest_path.keys())[0]
    return longest_path_vertex, longest_path_target

def diameter_algorithm(G, k):
    g_copy = G.copy()
    P = set()
    print('DIAM g_copy edges ', len(g_copy.edges))
    for i in range(1, k+1):
        u, v = find_largest_path(g_copy)
        g_copy.add_edge(u,v, weight=1)
        P.add((u,v))
    print('AFTER DIAM g_copy edges ', len(g_copy.edges))
    return g.calculate_number_of_spanning_trees(g_copy), P
