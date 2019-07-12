
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



def merge_compressed_graphs(G1, G2, Gcompname):
    for n in tqdm(set(G1.keys()).union(set(G2.keys()))):
        if (n in G1) and (n in G2):
            G1[n] = G1[n] + G2[n]
        elif (not n in G1) and (n in G2):
            G1[n] = G2[n].copy()
        if n in G2:
            del G2[n]
    
    with open(os.path.join("raw", f"{Gcompname}"), "wb") as f:
        pickle.dump(G1, f)



if __name__ == '__main__':
    graphs = {"graph_01.pickle","graph_03.pickle","graph_00_fragment_1.pickle","graph_00_fragment_2.pickle","graph_00_fragment_3.pickle","graph_00_fragment_4.pickle"}

    for fname in graphs:
        with open(os.path.join("raw", fname), "rb") as f:
            G = pickle.load(f)
        compress_graph(G, fname)
        del G

    Gcompressed = list(map(lambda x: x+".compressed", graphs))

    for i in range(0,6,2):
        fname1 = Gcompressed[i]
        fname2 = Gcompressed[i+1]
        with open(os.path.join("raw", "compressed", fname1), "rb") as f:
            G1 = pickle.load(f)
        with open(os.path.join("raw", "compressed", fname2), "rb") as f:
            G2 = pickle.load(f)
        merge_compressed_graphs(G1, G2, str(i))
        del G1, G2

    
    with open(os.path.join("raw",str(0)), "rb") as f:
        G1 = pickle.load(f)
    with open(os.path.join("raw",str(2)), "rb") as f:
        G2 = pickle.load(f)
    merge_compressed_graphs(G1, G2, "02")
    del G1, G2


    with open(os.path.join("raw","02"), "rb") as f:
        G1 = pickle.load(f)
    with open(os.path.join("raw",str(4)), "rb") as f:
        G2 = pickle.load(f)
    merge_compressed_graphs(G1, G2, "merged_final")
    del G1, G2
