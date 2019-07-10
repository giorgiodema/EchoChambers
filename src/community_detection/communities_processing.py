import pickle
import os
from collections import Counter


# Loading communities from file
COMMUNITIES_PATH = os.path.join("raw","communities.pickle")
PROCESSED_PATH = os.path.join("raw","communities.txt")
with open(COMMUNITIES_PATH,"rb") as f:
    comm = pickle.load(f)

communities = {}
for c in comm:
    if comm[c] not in communities:
        communities[comm[c]] = [c]
    else:
        communities[comm[c]].append(c)

communities_list = []
for community in communities:
    communities_list.append((communities[community], len(communities[community])))

communities_list.sort(key=lambda x: x[1], reverse=True)
communities_list = list(map(lambda x:x[0],communities_list))

    
# write back communities in communities.txt, each raw is a community, represented as a sequence of users id
# separated by commas
with open(PROCESSED_PATH,"w") as f:
    for c in communities_list:
        for id in c:
            print(str(id),end=',',file=f)
        print("\n",end="",file=f)




