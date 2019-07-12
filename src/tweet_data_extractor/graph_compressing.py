
from matplotlib import pyplot as plt
from math import log
import os
import pickle
from tqdm import tqdm
from collections import defaultdict, Counter

GRAPH_NAME = "graph-compressed_weighted_set.pickle"
GRAPH_FILE = os.path.join("raw", GRAPH_NAME)

with open(GRAPH_FILE, "rb") as f:
    G = pickle.load(f)

for node in G:
    print(G[node])
exit()

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


def compress_graph_weighted_dict():
    graph = {}
    for node in tqdm(list(G.nodes)):
        node_dict = Counter()
        can_remove = True
        for neighbor in G.neighbors(node):
            node_dict[neighbor] = G[node][neighbor]["weight"]
            if not neighbor in graph:
                can_remove = False 
        graph[node] = node_dict
        if can_remove:
            G.remove_node(node)

    if not os.path.isdir(os.path.join("raw", "compressed")):
        os.mkdir(os.path.join("raw", "compressed"))

    with open(os.path.join("raw", "compressed", GRAPH_NAME+".compressed"), "wb") as f:
        pickle.dump(graph, f)



def merge_graphs_weighted_dict():
    G1 = G
    with open(os.path.join("raw", "graph-compressed_weighted_set_1.pickle"), "rb") as f:
        G2 = pickle.load(f)
    '''G2 = {           #test code
        2: Counter({3:1, 5:1}),
        3:Counter({2:1, 5:1}),
        5:Counter({2:1, 3:1})
    }'''

    for n in set(G1.keys()).union(set(G2.keys())):
        if (n in G1) and (n in G2):
            G1[n] = G1[n] + G2[n]
        elif (not n in G1) and (n in G2):
            G1[n] = G2[n].copy()
        if n in G2:
            del G2[n]
    
    with open(os.path.join("raw", "graph-compressed_weighted_set_merged.pickle"), "wb") as f:
        pickle.dump(G1, f)


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
    compress_graph_weighted_dict()
    #merge_graphs_weighted_dict()
