import communities
import random
from datetime import datetime

random.seed(datetime.now())

def create_fake_data(nusers,nlinks):
    users = {}
    domains = [str(i) for i in range(1000)]

    for i in range(nusers):
        users[i] = {}
        users[i]["domains"] = []
        users[i]["retweets"] = []
        for k in range(nlinks):
            if random.randint(0,10)%5==0:
                r = random.randint(0,len(domains)-1)
                #r2 = random.randint(0,nusers)
                if domains[r] not in users[i]["domains"]:
                    users[i]["domains"].append(domains[r])
                #if r2 not in users[i]["retweets"] and r2 != i:
                #    users[i]["retweets"].append(r2)
    return users

users = create_fake_data(100,10)
G = communities.create_network(users)
communities.draw_graph(G)
comm = communities.extract_communities(G)
communities.draw_communities(G,comm)
print(len(comm))