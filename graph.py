import networkx as nx
import matplotlib.pyplot as plt
import itertools
from scipy import linalg
from scipy.sparse import csr_matrix

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
    # diff_edges = r_edges - s_edges
    DIF.add_edges_from(diff_edges)
    
    return DIF

def calculate_number_of_spanning_trees(G):
    L = nx.laplacian_matrix(G)
    L = csr_matrix.todense(L)
    L1 = L[:-1,:-1]
    return round(linalg.det(L1))

def test_correct_edges(G, Q, number_of_edges_from_Q):
    Q = list(Q)
    for idx in enumerate(Q):
        G_copy = G.copy(G)
        if (idx[0] <= len(Q) - number_of_edges_from_Q):
            for index in range(idx[0], idx[0]+number_of_edges_from_Q):
                print('index:', index)
                (u,v,w) = Q[index]
                G_copy.add_edge(u,v, weight=w)
        print('G_copy edges:', G_copy.edges())
            



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