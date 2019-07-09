
from matplotlib import pyplot as plt
from math import log
import os
import pickle
from tqdm import tqdm
from collections import defaultdict

GRAPH_FILE = os.path.join("raw", "graph-compressed.pickle")

with open(GRAPH_FILE, "rb") as f:
    G = pickle.load(f)



def prune_nodes():
    """Discards nodes that have less than [1,5] edges"""
    for node in tqdm(list(G.nodes)):
        if len(G[node]) <= 1:
            G.remove_node(node)

    print(f"Saving 1-pruned graph nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-1-pruned.pickle"), "wb") as f:
        pickle.dump(G, f)


    for node in tqdm(list(G.nodes)):
        if len(G[node]) <= 2:
            G.remove_node(node)

    print(f"Saving 2-pruned graph nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-2-pruned.pickle"), "wb") as f:
        pickle.dump(G, f)


    for node in tqdm(list(G.nodes)):
        if len(G[node]) <= 3:
            G.remove_node(node)

    print(f"Saving 3-pruned graph nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-3-pruned.pickle"), "wb") as f:
        pickle.dump(G, f)


    for node in tqdm(list(G.nodes)):
        if len(G[node]) <= 4:
            G.remove_node(node)

    print(f"Saving 4-pruned graph nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-4-pruned.pickle"), "wb") as f:
        pickle.dump(G, f)


    for node in tqdm(list(G.nodes)):
        if len(G[node]) <= 5:
            G.remove_node(node)

    print(f"Saving 5-pruned graph nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-5-pruned.pickle"), "wb") as f:
        pickle.dump(G, f)





def compress_graph():
    graph = {}
    for node in tqdm(list(G.nodes)):
        if not node in graph:
            graph[node] = set()
        for neighbor in G.neighbors(node):
            graph[node].add(neighbor)
        G.remove_node(node)

    print(f"Saving compressed nodes {len(G.nodes)}, edges {len(G.edges)}")
    with open(os.path.join("raw", "graph-compressed.pickle"), "wb") as f:
        pickle.dump(graph, f)


def compress_graph_weighted_set():
    graph = {}
    for node in tqdm(list(G.nodes)):
        if not node in graph:
            graph[node] = set()
        for neighbor in G.neighbors(node):
            graph[node].add((neighbor, G[node][neighbor]["weight"]))
        G.remove_node(node)

    with open(os.path.join("raw", "graph-compressed_weighted_set.pickle"), "wb") as f:
        pickle.dump(graph, f)


def compress_graph_weighted_list():
    graph = {}
    for node in tqdm(list(G.nodes)):
        if not node in graph:
            graph[node] = []
        for neighbor in G.neighbors(node):
            graph[node].append([neighbor, G[node][neighbor]["weight"]])
        G.remove_node(node)

    with open(os.path.join("raw", "graph-compressed_weighted_list.pickle"), "wb") as f:
        pickle.dump(graph, f)


if __name__ == '__main__':
    #compress_graph_weighted_list()
    pass