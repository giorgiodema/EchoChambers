import communities
import os
import pickle

TWEET_PATH = os.path.join("raw","user_data.pickle")
COMM_PATH = os.path.join("raw","communities.pickle")
GRAPH_PATH = os.path.join("raw","graph.pickle")

with open(TWEET_PATH,"rb") as f:
    s = f.read()
    users = pickle.loads(s)

G = communities.create_network(users)
with open(GRAPH_PATH,"wb") as f:
    s = pickle.dumps(G)
    f.write(s)

comm = communities.extract_communities(G)
with open(COMM_PATH,"wb") as f:
    s = pickle.dumps(comm)
    f.write(s)

communities.draw_communities(G,comm)