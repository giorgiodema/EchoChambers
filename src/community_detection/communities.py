import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from networkx.algorithms import community
from datetime import datetime
from tqdm import tqdm
import sys


def create_network(users):
    """Description\n
    Parameters:\n
    users (dict): key is the user id, each user has two lists:\n
    users[uid][domains] : list of domains cited by the user\n
    users[uid][retweets]: list of users ids retweeted by user
    \n
    Returns:\n
    graph: network graph
   """
    # initialize edges
    #print("\nInitialize Edges:",end=" ")
    #sys.stdout.flush()
    edges_list = Counter()
    processed = []
    ids = list(users.keys())
    for i in tqdm(range(len(ids))):
        for k in range(i+1,len(ids)):
            for di in users[ids[i]]["domains"]:
                if di in users[ids[k]]["domains"]:
                    edges_list[(ids[i],ids[k])] += 1
        for id in users[ids[i]]["retweets"]:
            edges_list[(ids[i],id)] += 1


    # initialize Graph
    G = nx.Graph()
    G.add_nodes_from(list(users.keys()))
    G.add_edges_from(list(edges_list.keys()))
    #print("\nAdd Edges:",end=" ")
    #sys.stdout.flush()
    for (i,j), weight in tqdm(edges_list.items()):
        G[i][j]['weight'] = weight
    
    return G


def extract_communities(G):
    """Description\n
    Parameters:\n
    G (Graph): network graph
    Returns:\n
    list: list of communities, each community is a set of uids

   """

    #draw graph
    #nx.draw_circular(G)
    #plt.show()

    # detect communities using label propagation algorithm
    communities = community.asyn_lpa_communities(G,weight="weight",seed=int(datetime.now().timestamp()))
    res = []
    for c in communities:
        res.append(c)
    return res

def draw_graph(G):
    nx.draw_circular(G,node_color="#ffe001")
    plt.show()

def draw_communities(G,comm):
    number_of_colors = len(comm)
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    for i in range(len(comm)):
        edgelist = [(h,k) for h in comm[i] for k in comm[i] if h>k]
        nx.draw_circular(G,node_size=10,arrowsize=1,width=0.1,nodelist=comm[i],edgelist=edgelist,node_color=color[i],edge_color=color[i])
    plt.show()

