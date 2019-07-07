import json
import pickle
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


def get_user_data():
    JSON_PATH = "tweets_json"  #json directory path
    CACHE_FILE = "user_data_cached.pickle"

    if os.path.isfile(CACHE_FILE):
        print(" [*] Pickled data found, loading...")
        with open(CACHE_FILE, "rb") as file_in:
            return pickle.load(file_in)

    print(" [*] Creating user data from tweets...")

    users_data = {}    #users_data[user] = (domains list, retweet list)

    for filename in tqdm(os.listdir(JSON_PATH)):
        if filename.endswith(".json"): 
            with open(os.path.join(JSON_PATH, filename)) as json_file:
                tweets = json.load(json_file)
                
                for tweet in tweets:
                    urls = tweet["entities"]["urls"]
                    user = tweet["user"]["id"]

                    # create user key in users_data
                    if not user in users_data:
                    	users_data[user] = (list(), list())

                    # retrieve urls
                    for url in urls:
                    	url = url["expanded_url"]
                    	# if the url is internal in twitter return it all
                    	if "twitter" in url[:20]:
                        	users_data[user][0].append(url)
                        # else if the url is not internal in twitter then take only its domain
                        else:
                        	domain = _extract_domain(url)
                        	if domain is None:
                        		continue
                        	else:
                        		users_data[user][0].append(domain)
                        		

                    # retrieve retweets
                    if "retweeted_status" in tweet and not tweet["retweeted_status"] is None:
                        user_rtw = tweet["retweeted_status"]["user"]["id"]
                        users_data[user][1].append(user_rtw)

    result = {}
    for user, data in users_data.items():
        result[user] = {"domains":data[0], "retweets":data[1]}

    pickle.dump(result, open(CACHE_FILE, "wb"))

    return result


if __name__ == "__main__":
	get_user_data()