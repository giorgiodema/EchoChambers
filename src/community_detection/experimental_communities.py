
import os
import pickle
from tqdm import tqdm

GRAPH_FILE = os.path.join("raw", "graph.pickle")
DEGREE_FILE = os.path.join("raw", "graph_degrees.pickle")

with open(GRAPH_FILE, "rb") as f:
    G = pickle.load(f)

def worker(n):
    return [len(G[n]), sum([G[n][u]["weight"] for u in G[n]]), n]

degs = map(worker, tqdm(G.nodes))
degs = sorted(degs, key=lambda x: x[0], reverse=True)

with open(DEGREE_FILE, "wb") as f:
    G = pickle.dump(degs, f)

print('aa')
        