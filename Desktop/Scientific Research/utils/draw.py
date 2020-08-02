import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos

def _position_communities(g, partition, **kwargs):

    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos

def _find_between_community_edges(g, partition):

    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges

def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos

def test():
    # to install networkx 2.0 compatible version of python-louvain use:
    # pip install -U git+https://github.com/taynaud/python-louvain.git@networkx2
    from community import community_louvain

    g = nx.karate_club_graph()
    partition = community_louvain.best_partition(g)
    pos = community_layout(g, partition)

    nx.draw(g, pos, node_color=list(partition.values()))
    plt.show()
    return

def draw_graph(g):
    pos = nx.spring_layout(g)
    plt.figure(figsize=(16, 16))
    plt.axis('off')
    nx.draw_networkx_nodes(g, pos,
                        node_size=600,
                        cmap=plt.cm.RdYlBu,
                        alpha=0.9)
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    nx.draw_networkx_labels(g, pos)
    plt.show()

def draw_partition(g, partition):
    plt.figure(figsize=(16, 16))
    plt.axis('off')
    pos = community_layout(g, partition)
    nx.draw(g, pos,
            node_color=list(partition.values()),
            node_size=600,
            with_labels=True,
            cmap=plt.cm.RdYlBu,
            alpha=0.9)
    plt.show()

def draw_partition2(g, partition):
    pos = nx.spring_layout(g)
    plt.figure(figsize=(16, 16))
    plt.axis('off')
    nx.draw_networkx_nodes(g, pos,
                        node_size=600,
                        cmap=plt.cm.RdYlBu,
                        node_color=list(partition.values()),
                        alpha=0.9)
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    plt.show(g)

def draw_partition3(g, partition):
    pos = nx.spring_layout(g)
    plt.figure(figsize=(16, 16))
    plt.axis('off')
    nx.draw_networkx_nodes(g, pos,
                        node_size=600,
                        cmap=plt.cm.RdYlBu,
                        node_color=partition,
                        alpha=0.9)
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    nx.draw_networkx_labels(g, pos)
    plt.show(g)