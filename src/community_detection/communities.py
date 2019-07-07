import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
from datetime import datetime

def detect_communities(users):
    """Description\n
    Parameters:\n
    users (dict): key is the user id, each user has two lists:\n
    users[uid][domains] : list of domains cited by the user\n
    users[uid][retweets]: list of users ids retweeted by user
    \n
    Returns:\n
    list: list of communities, each community is a set of uids

   """
    # initialize edges
    edges_list = []
    for i in range(len(users)):
        for k in range(i+1,len(users)):
            for di in users[i]["domains"]:
                if di in users[k]["domains"]:
                    edges_list.append((i,k))
        for id in users[i]["retweets"]:
            edges_list.append((i,id))

    edges_set = set(edges_list)
    edges_weights = {}
    for e in edges_set:
        edges_weights[e] = edges_list.count(e)

    # initialize Graph
    G = nx.Graph()
    G.add_nodes_from(list(users.keys()))
    G.add_edges_from(edges_set)
    for (i,j) in edges_set:
        G[i][j]['weight'] = edges_weights[(i,j)]
    
    #draw graph
    nx.draw_circular(G)
    plt.show()

    # detect communities using label propagation algorithm
    communities = community.asyn_lpa_communities(G,weight="weight",seed=int(datetime.now().timestamp()))
    res = []
    for c in communities:
        res.append(c)
    return res
