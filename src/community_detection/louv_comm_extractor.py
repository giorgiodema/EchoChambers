import community
import networkx as nx
import pickle
import os
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

GRAPH_PATH = os.path.join("raw","graph.pickle")
COMMUNITIES_PATH = os.path.join("raw","communities.pickle")

def draw_graph(G):
    nx.draw_circular(G,node_size=1,arrowsize=1,width=0.1)
    plt.show()


def draw_communities(G,comm):
    print("drwaing comminuties")
    number_of_colors = len(comm)
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    for i in range(len(comm)):
        edgelist = [(h,k) for h in comm[i] for k in comm[i] if G.has_edge(h,k)]
        nx.draw_circular(G,node_size=1,arrowsize=1,width=0.1,nodelist=comm[i],edgelist=edgelist,node_color=color[i],edge_color=color[i])
    plt.show()


def load_graph():
    G = None
    if os.path.exists(GRAPH_PATH):
        print("loading graph")
        with open(GRAPH_PATH,"rb") as f:
            s = f.read()
            G = pickle.loads(s)
    else:
        raise Exception("graph.pickle not found")
    return G


def extract_communities(G):
    print("extracting communities")
    partition = community.best_partition(G)

    communities = []
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        communities.append(list_nodes)

    with open(COMMUNITIES_PATH,"wb") as f:
        s = pickle.dumps(communities)
        f.write(s)


def load_communities():
    print("loading communities")
    if os.path.exists(COMMUNITIES_PATH):
        with open(COMMUNITIES_PATH,"rb") as f:
            s = f.read()
            communities = pickle.loads(s)

        return communities
    else:
        raise Exception("communities.pickle not found")


G = load_graph()

if not os.path.exists(COMMUNITIES_PATH):
    extract_communities(G)

communities = load_communities()
len = list(map(lambda x:len(x),communities))
len.sort()
len.reverse()

#draw_communities(G,communities)

