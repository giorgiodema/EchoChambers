
import re
import json
import pickle
import networkx as nx
import itertools
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict
import os

FLUSH_ALWAYS = True

BASE_PATH = os.path.join("src", "tweet_data_extractor")
#JSON_PATH = os.path.join("raw", "tweets_json")  #json directory path
JSON_PATH = os.path.join("raw")  #json directory path
CACHE_FILE = os.path.join("raw", "graph.pickle")


def _extract_domain(link: str) -> str:
	"""Extract the domain of an url"""
	link_split = link.split('/')
	if link.startswith('http'):
		domain = link_split[2] if len(link_split)>=3 else None
	else:
		domain = None
	return domain

def extract_mentions(tweet):
    if "retweeted_status" in tweet:
        text = tweet["text"].replace('@', '', 1)  #discard heading @ in retweeted text 'RT @...'
    else:
        text = tweet["text"]
    exp = re.compile(r"@\w+")
    return exp.findall(text)


def extract_replies(tweet):
    if "retweeted_status" in tweet:
        return None
    exp = re.compile(r"\/[0-9]{4,}")
    urls = [url["expanded_url"] for url in tweet["entities"]["urls"]]
    urls = ' '.join(urls)
    return exp.findall(urls)
    

def tweets_iter(dir_path):
    for filename in tqdm(sorted(os.listdir(dir_path))):
        if filename.endswith(".json"): 
            with open(os.path.join(dir_path, filename), "r", encoding="utf-8") as json_file:
                tweets = json.load(json_file)
                for tweet in tweets:
                    yield tweet


def get_mappings():
    """Returns a tuple with two dictionaries. 
    The first is a mapping username -> userid, where username is the one @foo, with @.
    The second is a mapping tweetid -> userid of the creator"""
    map_usrname_usrid = {}
    map_twtid_usrid = {}
    all_tweets = tweets_iter(JSON_PATH)
    print(" [*] Extracting user mappings")  
    for tweet in all_tweets:
        map_usrname_usrid["@"+tweet["user"]["screen_name"]] = tweet["user"]["id"]
        map_twtid_usrid[tweet["id"]] = tweet["user"]["id"]
    return map_usrname_usrid, map_twtid_usrid


def get_user_graph():
    if os.path.isfile(CACHE_FILE) and not FLUSH_ALWAYS:
        print(" [-] Pickled data found, loading...")
        with open(CACHE_FILE, "rb") as file_in:
            return pickle.load(file_in)

    print(" [-] Creating user data from tweets...")

    G = nx.Graph()
    users, domains = set(), set()


    all_tweets = tweets_iter(JSON_PATH)

    # Create bipartite graph   < users - domains >
    print(" [*] Creating bipartite graph < users - domains >")                 
    for tweet in all_tweets:
        urls = tweet["entities"]["urls"]
        user = tweet["user"]["id"]
        rtw_user = tweet["retweeted_status"]["user"]["id"] if "retweeted_status" in tweet else None

        # create user key in users
        if not user in users:
            users.add(user)
            G.add_node(user)

        if not rtw_user is None and not rtw_user in users:
            users.add(rtw_user)
            G.add_node(rtw_user)

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
                G.add_node(domain)
            
            # if edge does not exist create it with weigth 1
            if not G.has_edge(user, domain):
                G.add_edge(user, domain, weight=1)
            else:
                G[user][domain]["weight"] += 1


    def update_edge(G, u, v):
        """If <u,v> edge does not exists create it, otherwise increment its weight by 1"""
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=1)
        else:
            G[u][v]["weight"] += 1

    # Merge bipartite graph: for each pair of users that points the same domain add an edge between them
    G_result = nx.Graph()
    G_result.add_nodes_from(users)
    print(" [*] Merging bipartite graph")
    for domain in tqdm(domains):
        linked_usrs = G[domain]
        for user1, user2 in itertools.combinations(linked_usrs, 2):
            update_edge(G_result, user1, user2)



    # Add links by retweet: link users in the final graph if one retweeted the other
    all_tweets = tweets_iter(JSON_PATH)
    print(" [*] Linking user by retweets")
    for tweet in all_tweets:
        if "retweeted_status" in tweet:
            u, v = tweet["user"]["id"], tweet["retweeted_status"]["user"]["id"]
            update_edge(G_result, u, v)


    # Add links by mentioning
    map_usrname_usrid, map_twtid_usrid = get_mappings()
    all_tweets = tweets_iter(JSON_PATH)
    print(" [*] Linking user by mentioning")
    for tweet in all_tweets:
        user = tweet["user"]["id"]
        mentions = extract_mentions(tweet)
        for mentioned_user in mentions:
            if mentioned_user in map_usrname_usrid:
                mentioned_userid = map_usrname_usrid[mentioned_user]
                update_edge(G_result, mentioned_userid, user)


    # Add links by reply
    all_tweets = tweets_iter(JSON_PATH)
    print(" [*] Linking user by reply")
    for tweet in all_tweets:
        user = tweet["user"]["id"]
        replies = extract_replies(tweet)
        if replies is None:
            continue
        for reply in replies:
            if reply[1:] in map_twtid_usrid:     #reply[1:] for heading /
                replied_user = map_twtid_usrid[reply[1:]]
                update_edge(G_result, replied_user, user)


    # Optimization: trash nodes with no edges
    print(" [*] Removing dead end nodes")
    for node in tqdm(list(G_result.nodes)):
        if len(G_result[node]) < 1:
            G_result.remove_node(node)


    print(f" [-] Graph construction finished, users {len(G_result.nodes)}, links {len(G_result.edges)}")
    pickle.dump(G_result, open(CACHE_FILE, "wb"))

    return G_result


if __name__ == "__main__":
	get_user_graph()