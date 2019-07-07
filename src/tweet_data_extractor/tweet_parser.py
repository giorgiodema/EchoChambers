import json
import pickle
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict
import os


def get_user_data():
    JSON_PATH = "tweets_json"  #json directory path
    CACHE_FILE = "user_data_cached.pickle"

    if os.path.isfile(CACHE_FILE):
        print(" [*] Pickled data found, loading...")
        with open(CACHE_FILE, "rb") as file_in:
            return pickle.load(file_in)

    print(" [*] Creating user data from tweets...")

    users_data = defaultdict(lambda: (list(), list()))  #users_data[user] = (domains list, retweet list)

    for filename in tqdm(os.listdir(JSON_PATH)):
        if filename.endswith(".json"): 
            with open(os.path.join(JSON_PATH, filename)) as json_file:
                tweets = json.load(json_file)
                
                for tweet in tweets:
                    # urls
                    urls = tweet["entities"]["urls"]
                    user = tweet["user"]["id"]
                    for url in urls:
                        users_data[user][0].append(url["expanded_url"])

                    # retweets
                    if "retweeted_status" in tweet and not tweet["retweeted_status"] is None:
                        user_id = tweet["retweeted_status"]["user"]["id"]
                        users_data[user][1].append(user_id)

    result = {}
    for user, data in users_data.items():
        result[user] = {"domains":data[0], "retweets":data[1]}

    pickle.dump(result, open(CACHE_FILE, "wb"))

    return result


if __name__ == "__main__"
	get_user_data()