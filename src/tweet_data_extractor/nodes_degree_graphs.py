
from matplotlib import pyplot as plt
from math import log
import os
import pickle
from tqdm import tqdm
from collections import defaultdict

GRAPH_FILE = os.path.join("raw", "graph.pickle")
DEGREE_FILES = os.path.join("raw", "graph_ultra_big_degrees.pickle")

with open(GRAPH_FILE, "rb") as f:
    G = pickle.load(f)

degs = [len(G[n]) for n in G.nodes]
#pickle.dump(sorted(degs), open(DEGREE_FILES, "wb"))

d = defaultdict(int)
for deg in degs:
    d[deg] += 1

x, y, area = [], [], []
for i in tqdm(range(max(degs))):
    if d[i] == 0:
        continue
    x.append(i)
    y.append(0)
    area.append(d[i])

plt.scatter(x,y,s=area)
plt.show()

exclude_first = 1
plt.scatter(x[exclude_first:],y[exclude_first:],s=area[exclude_first:])
plt.show()


plt.plot(x,area)
plt.ylim((0,1500))
plt.xlim((0,3000))
plt.show()

