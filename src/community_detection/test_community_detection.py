import community
import random

def create_fake_data(nusers,nlinks):
    users = {}
    domains = ["A","B","C","D","E","F","G","H","I","L","M","N","O","P","Q","R","S","T","U","V","Z"]

    for i in range(nusers):
        users[i] = {}
        users[i]["domains"] = []
        users[i]["retweets"] = []
        for k in range(nlinks):
            r = random.randint(0,len(domains)-1)
            r2 = random.randint(0,nusers)
            if domains[r] not in users[i]["domains"]:
                users[i]["domains"].append(domains[r])
            if r2 not in users[i]["retweets"] and r2 != i:
                users[i]["retweets"].append(r2)
    return users

users = create_fake_data(10,5)
communities = community.detect_communities(users)
print("ciao")