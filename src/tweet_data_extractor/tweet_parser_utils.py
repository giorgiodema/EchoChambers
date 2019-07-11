
import re
import os
import json
from tqdm import tqdm


def tweets_iter(dir_path):
    """Iterator on tweets in .json format inside 'dir_path' directory"""
    for filename in tqdm(sorted(os.listdir(dir_path))):
        if filename.endswith(".json"): 
            with open(os.path.join(dir_path, filename), "r", encoding="utf-8") as json_file:
                tweets = json.load(json_file)
                for tweet in tweets:
                    yield tweet

def tweets_directories_iter(dir_path, dirs_prefix):
    """Iterator on all subfolders whose name starts with 'dirs_prefix' inside directory 'dir_path'. Does not recurse"""
    for dirname in os.listdir(dir_path):
        dirpath = os.path.join(dir_path, dirname)
        if os.path.isdir(dirpath) and dirname.startswith(dirs_prefix):
            print(f"Exploring {dirname}")
            all_tweets = tweets_iter(dirpath)
            for t in all_tweets:
                yield t
        else:
            print(f"Skipping {dirname}")



def extract_domain(link: str) -> str:
	"""Extract the domain of an url"""
	link_split = link.split('/')
	if link.startswith('http'):
		domain = link_split[2] if len(link_split)>=3 else None
	else:
		domain = None
	return domain


def extract_mentions(tweet):
    """Extract all mentions ['@foo', '@bar'] from a tweet"""
    if "retweeted_status" in tweet:
        text = tweet["text"].replace('@', '', 1)  #discard heading @ in retweeted text 'RT @...'
    else:
        text = tweet["text"]
    exp = re.compile(r"@\w+")
    return exp.findall(text)


def extract_replies(tweet):
    """Extract the ids of replied or cited tweets"""
    if "retweeted_status" in tweet:
        return None
    exp = re.compile(r"\/[0-9]{4,}")
    urls = [url["expanded_url"] for url in tweet["entities"]["urls"]]
    urls = ' '.join(urls)
    return exp.findall(urls)


def get_mappings(all_tweets_itr):
    """Returns a tuple with two dictionaries. 
    The first is a mapping username -> userid, where username is the one @foo, with @.
    The second is a mapping tweetid -> userid of the creator"""
    map_usrname_usrid = {}
    map_twtid_usrid = {}
    print(" [*] Extracting user mappings")  
    for tweet in all_tweets_itr:
        map_usrname_usrid["@"+tweet["user"]["screen_name"]] = tweet["user"]["id"]
        map_twtid_usrid[tweet["id"]] = tweet["user"]["id"]
    return map_usrname_usrid, map_twtid_usrid