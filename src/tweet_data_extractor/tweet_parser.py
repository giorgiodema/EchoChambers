import json
import pickle
import networkx as nx
import itertools
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict
import os


def _extract_domain(link: str) -> str:
	"""Extract the domain of an url"""
	link_split = link.split('/')
	if link.startswith('http'):
		domain = link_split[2] if len(link_split)>=3 else None
	else:
		domain = None
	return domain


def get_user_graph():
    BASE_PATH = os.path.join("src", "tweet_data_extractor")
    JSON_PATH = os.path.join(BASE_PATH, "tweets_json")  #json directory path
    CACHE_FILE = os.path.join(BASE_PATH, "user_data.pickle")

    if os.path.isfile(CACHE_FILE):
        print(" [*] Pickled data found, loading...")
        with open(CACHE_FILE, "rb") as file_in:
            return pickle.load(file_in)

    print(" [*] Creating user data from tweets...")

    G = nx.Graph()
    users, domains = set(), set()

    # Create bipartite graph   < users - domains > 
    for filename in tqdm(os.listdir(JSON_PATH)):
        if filename.endswith(".json"): 
            with open(os.path.join(JSON_PATH, filename), "r", encoding="utf-8") as json_file:
                tweets = json.load(json_file)
                
                for tweet in tweets:
                    urls = tweet["entities"]["urls"]
                    user = tweet["user"]["id"]

                    # create user key in users
                    if not user in users:
                        users.add(user)
                        G.add_node(user)

                    # retrieve urls domains
                    for url in urls:
                        url = url["expanded_url"]

                        # if the url is internal in twitter return it all
                        if "twitter" in url[:20]:
                        	domain = url
                        # else if the url is not internal in twitter then take only its domain
                        else:
                            domain = _extract_domain(url)
                            if domain is None:
                                continue

                        # if domain first appereance, create key in domains
                        if not domain in domains:
                            domains.add(domain)
                        
                        # if edge does not exist create it with weigth 1
                        if not G.has_edge(user, domain):
                            G.add_edge(user, domain, weight=1)
                        else:
                            G[user][domain]["weight"] += 1

    # Merge bipartite graph: for each pair of users that points the same domain add an edge between them
    G_result = nx.Graph()
    G_result.add_nodes_from(users)
    for domain in tqdm(domains):
        linked_usrs = G[domain]
        for user1, user2 in itertools.combinations(linked_usrs, 2):
            G_result.add_edge(user1, user2)

    pickle.dump(G_result, open(CACHE_FILE, "wb"))

    return G_result


if __name__ == "__main__":
	get_user_graph()