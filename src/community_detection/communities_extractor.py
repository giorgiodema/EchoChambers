import communities
import os
import pickle
from networkx.algorithms.connectivity.connectivity import node_connectivity


TWEET_PATH = os.path.join("raw","user_data.pickle")
COMM_PATH = os.path.join("raw","communities.pickle")
GRAPH_PATH = os.path.join("raw","graph.pickle")

with open(TWEET_PATH,"rb") as f:
    s = f.read()
    users = pickle.loads(s)

G = None
if os.path.exists(GRAPH_PATH):
    print("loading graph")
    with open(GRAPH_PATH,"rb") as f:
        s = f.read()
        G = pickle.loads(s)
else:
    print("creating graph")
    G = communities.create_network(users)
    with open(GRAPH_PATH,"wb") as f:
        print("saving graph")
        s = pickle.dumps(G)
        f.write(s)
#communities.draw_graph(G)
#node_conn = node_connectivity(G)
#print("node connectivity: "+str(node_conn))
comm = communities.extract_communities(G)
with open(COMM_PATH,"wb") as f:
    s = pickle.dumps(comm)
    f.write(s)

communities.draw_communities(G,comm)