
import re
import json
import pickle
import networkx as nx
import itertools
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict
import os

import tweet_parser_utils 
import user_graph_utils

FLUSH_ALWAYS = True

BASE_PATH = os.path.join("src", "tweet_data_extractor")
#JSON_PATH = os.path.join("raw", "tweets_json")  #json directory path
JSON_PATH = os.path.join("raw")  #json directory path
CACHE_FILE = os.path.join("raw", "graph.pickle")



def get_user_graph():
    if os.path.isfile(CACHE_FILE) and not FLUSH_ALWAYS:
        print(" [-] Pickled data found, loading...")
        with open(CACHE_FILE, "rb") as file_in:
            return pickle.load(file_in)

    print(" [-] Creating user data from tweets...")

    G_bipartite = nx.Graph()
    users, domains = set(), set()


    all_tweets = tweet_parser_utils.tweets_iter(JSON_PATH)

    # Create bipartite graph   < users - domains >
    print(" [*] Creating bipartite graph < users - domains >")                 
    for tweet in all_tweets:
        urls = tweet["entities"]["urls"]
        user = tweet["user"]["id"]
        rtw_user = tweet["retweeted_status"]["user"]["id"] if "retweeted_status" in tweet else None

        # create user key in users
        if not user in users:
            users.add(user)
            G_bipartite.add_node(user)

        if not rtw_user is None and not rtw_user in users:
            users.add(rtw_user)
            G_bipartite.add_node(rtw_user)

        # retrieve urls domains
        for url in urls:
            url = url["expanded_url"]

            # if the url is internal in twitter return it all
            if "twitter" in url[:20]:
                domain = url
            # else if the url is not internal in twitter then take only its domain
            else:
                domain = tweet_parser_utils.extract_domain(url)
                if domain is None:
                    continue

            # if domain first appereance, create key in domains
            if not domain in domains:
                domains.add(domain)
                G_bipartite.add_node(domain)
            
            # if edge does not exist create it with weigth 1
            if not G_bipartite.has_edge(user, domain):
                G_bipartite.add_edge(user, domain, weight=1)
            else:
                G_bipartite[user][domain]["weight"] += 1


    # Merge bipartite graph in final graph
    G_final = user_graph_utils.merge_bipartite(G_bipartite, users, domains)

    # Add links by retweet
    tweet_itr = tweet_parser_utils.tweets_iter(JSON_PATH)
    user_graph_utils.add_links_retweet(G_final, tweet_itr)

    # Get userid mappings (useful later)
    tweet_itr = tweet_parser_utils.tweets_iter(JSON_PATH)
    map_usrname_usrid, map_twtid_usrid = tweet_parser_utils.get_mappings(tweet_itr)

    # Add links by mentioning
    tweet_itr = tweet_parser_utils.tweets_iter(JSON_PATH)
    user_graph_utils.add_links_mentioning(G_final, map_usrname_usrid, tweet_itr)

    # Add links by reply
    tweet_itr = tweet_parser_utils.tweets_iter(JSON_PATH)
    user_graph_utils.add_links_reply(G_final, map_twtid_usrid, tweet_itr)

    # Trash nodes with no edges
    user_graph_utils.remove_dead_nodes(G_final)


    print(f" [-] Graph construction finished, users {len(G_final.nodes)}, links {len(G_final.edges)}")
    pickle.dump(G_final, open(CACHE_FILE, "wb"))

    return G_final


if __name__ == "__main__":
	get_user_graph()