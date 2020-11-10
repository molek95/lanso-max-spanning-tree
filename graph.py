import networkx as nx
import matplotlib.pyplot as plt
import itertools
from scipy import linalg
from scipy.sparse import csr_matrix
import random
from networkx.readwrite import json_graph
import json
import numpy as np


def create_barabasi_albert_tree(N, weight_values=1):
    t = nx.barabasi_albert_graph(N, 1)
    for (u,v) in t.edges:
        t[u][v]['weight'] = weight_values
    return t
    

def create_barabasi_albert_graph(n, m, weight_values=1):
    g = nx.barabasi_albert_graph(n, m)
    for (u,v) in g.edges:
        g[u][v]['weight'] = weight_values
    return g

def create_weighted_barabasi_albert_graph(n, m, lower_weight=1, upper_weight=5):
    g = nx.barabasi_albert_graph(n, m)
    for (u,v) in g.edges:
        g[u][v]['weight'] = random.randint(lower_weight, upper_weight)
    return g


"""
Creates a star graph.
@params:
    N - number of nodes
    weight_values - list of edge weights, optional parameter
@return:
    G - star graph
"""
def create_graph_with_weight(N, weight_values=1):
    G = nx.Graph()
    if isinstance(weight_values, list):
        for node in range(1, N):
            G.add_edge(0, node, weight=weight_values[node])
    else:
        for node in range(1, N):
            G.add_edge(0, node, weight=1)
    return G

"""
Creates a fully connected graph.
@params:
    N - number of nodes
    create_using - subgraph
@return:
    G - fully connected graph
"""
def fully_connected_graph_from_list(N, create_using=None):
    G = nx.empty_graph(N, create_using)
    if N > 1:
        if G.is_directed():
            edges = itertools.permutations(G.nodes, 2)
        else:
            edges = itertools.combinations(G.nodes, 2)
        for (u,v) in edges:
            G.add_edge(u,v, weight=1)
    return G

"""
Edge difference of 2 graphs.
@params:
    S - "source" graph
    R - reference graph
@return:
    DIF - graph with edges of S-R
"""
def difference(S, R):
    DIF = nx.create_empty_copy(R)
    DIF.name = 'Difference of (%s and %s)' % (S.name, R.name)
    if set(S) != set(R):
        raise nx.NetworkXError('Node sets of graphs are not equal')
    
    r_edges = set(R.edges())
    s_edges = set(S.edges())
    
    diff_edges = r_edges.symmetric_difference(s_edges)
    DIF.add_edges_from(diff_edges)
    
    return DIF

def calculate_number_of_spanning_trees(G):
    L = nx.laplacian_matrix(G)
    L = csr_matrix.todense(L)
    L1 = L[:-1,:-1]
    return round(linalg.det(L1))

def eigenvalues_of_laplacian(G):
    L = nx.laplacian_matrix(G)
    L = csr_matrix.todense(L)
    eigenValues, eigenVectors = np.linalg.eig(L)
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    #eigenVectors = eigenVectors[:,idx]
    return eigenValues

def draw(G):
    elarge = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 0.5]
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G,pos,edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.axis('off')
    plt.show()
    
def generate_random_graph(number_of_nodes, edge_probability):
    is_connected = False
    while is_connected == False:
        G = nx.gnp_random_graph(number_of_nodes, edge_probability)
        is_connected = nx.is_connected(G)
    for (u,v) in G.edges():
        G.edges[u,v]['weight'] = round(random.uniform(0,1), 2)
    return G

def generate_random_graph_with_unit_weight(number_of_nodes, edge_probability):
    is_connected = False
    while is_connected == False:
        G = nx.gnp_random_graph(number_of_nodes, edge_probability)
        is_connected = nx.is_connected(G)
    for i, (u,v) in enumerate(G.edges()):
        G.edges[u,v]['weight'] = 1
    return G

def generate_random_tree_with_weight(number_of_nodes, weight=1):
    T = nx.random_tree(number_of_nodes)
    for (u, v) in T.edges():
        T.edges[u,v]['weight'] = weight
    return T

def save_json(filename, graph):
    g = graph
    g_json = json_graph.node_link_data(g)
    json.dump(g_json, open(filename, 'w'), indent=2)
    
def read_json_file(filename):
   with open(filename) as f:
       js_graph = json.load(f)
   return json_graph.node_link_graph(js_graph)
