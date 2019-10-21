import networkx as nx
import matplotlib.pyplot as plt
import itertools

"""
Creates a star graph.
@params:
    N - number of nodes
    weight_values - list of edge weights, optional parameter
@return:
    G - star graph
"""
def create_star_with_weight(N, weight_values=1):
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
    G - graph with edges of S-R
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