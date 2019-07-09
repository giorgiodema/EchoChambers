
from tqdm import tqdm
import networkx as nx
import itertools

import tweet_parser_utils

def update_edge(G, u, v):
    """If <u,v> edge does not exists create it, otherwise increment its weight by 1"""
    if not G.has_edge(u, v):
        G.add_edge(u, v, weight=1)
    else:
        G[u][v]["weight"] += 1


def merge_bipartite(G, users, domains):
    """Merge bipartite graph: for each pair of users that points the same domain add an edge between them"""
    print(" [*] Merging bipartite graph")
    for domain in tqdm(domains):
        linked_usrs = G[domain]
        for user1, user2 in itertools.combinations(linked_usrs, 2):
            update_edge(G, user1, user2)
        G.remove_node(domain)
    print(f"Merged graph has {len(G.nodes)} nodes and {len(G.edges)} links")
    return G


def add_links_retweet(G_final, all_tweets_itr):
    """Add links by retweet: link users in the final graph if one retweeted the other"""
    n_links_start = len(G_final.edges)
    print(" [*] Linking user by retweets")
    for tweet in all_tweets_itr:
        if "retweeted_status" in tweet:
            u, v = tweet["user"]["id"], tweet["retweeted_status"]["user"]["id"]
            update_edge(G_final, u, v)
    print(f"Retweeted links added {len(G_final.edges) - n_links_start} links")


def add_links_mentioning(G_final, map_usrname_usrid, all_tweets_itr):
    """Add links by mentioning"""
    n_links_start = len(G_final.edges)
    print(" [*] Linking user by mentioning")
    for tweet in all_tweets_itr:
        user = tweet["user"]["id"]
        mentions = tweet_parser_utils.extract_mentions(tweet)
        for mentioned_user in mentions:
            if mentioned_user in map_usrname_usrid:
                mentioned_userid = map_usrname_usrid[mentioned_user]
                update_edge(G_final, mentioned_userid, user)
    print(f"Mentioning links added {len(G_final.edges) - n_links_start} links")


def add_links_reply(G_final, map_twtid_usrid, all_tweets_itr):
    """Add links by reply"""
    n_links_start = len(G_final.edges)
    print(" [*] Linking user by reply")
    for tweet in all_tweets_itr:
        user = tweet["user"]["id"]
        replies = tweet_parser_utils.extract_replies(tweet)
        if replies is None:
            continue
        for reply in replies:
            if reply[1:] in map_twtid_usrid:     #reply[1:] for heading /
                replied_user = map_twtid_usrid[reply[1:]]
                update_edge(G_final, replied_user, user)
    print(f"Reply links added {len(G_final.edges) - n_links_start} links")


def remove_dead_nodes(G_final):
    """Trash nodes with no edges"""
    print(" [*] Removing dead end nodes")
    for node in tqdm(list(G_final.nodes)):
        if len(G_final[node]) < 1:
            G_final.remove_node(node)