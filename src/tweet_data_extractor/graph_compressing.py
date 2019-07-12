
from matplotlib import pyplot as plt
from math import log
import os
import pickle
from tqdm import tqdm
from collections import defaultdict, Counter


def compress_graph(G, Gname):
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

    with open(os.path.join("raw", "compressed", Gname+".compressed"), "wb") as f:
        pickle.dump(graph, f)



def merge_compressed_graphs(G1, G2, G1name, G2name):
    G1 = G
    with open(os.path.join("raw", "graph-compressed_weighted_set_1.pickle"), "rb") as f:
        G2 = pickle.load(f)

    for n in set(G1.keys()).union(set(G2.keys())):
        if (n in G1) and (n in G2):
            G1[n] = G1[n] + G2[n]
        elif (not n in G1) and (n in G2):
            G1[n] = G2[n].copy()
        if n in G2:
            del G2[n]
    
    with open(os.path.join("raw", "graph-compressed_weighted_set_merged.pickle"), "wb") as f:
        pickle.dump(G1, f)



if __name__ == '__main__':
    Gname = "graph-compressed_weighted_set.pickle"
    Gpath = os.path.join("raw", Gname)

    COMPRESS = True

    if COMPRESS:
        with open(Gpath, "rb") as f:
            G = pickle.load(f)

        compress_graph(G, Gname)
    
    else:
        G2name = "graph-compressed_weighted_set.pickle"
        G2path = os.path.join("raw", G2name)
        with open(G2path, "rb") as f:
            G2 = pickle.load(f)
        merge_compressed_graphs(G, G2, Gpath, G2path)
