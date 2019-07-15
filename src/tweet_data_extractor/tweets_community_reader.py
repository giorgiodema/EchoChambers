
from tweet_parser_utils import tweets_iter, tweets_directories_iter
from collections import Counter, defaultdict
import pickle
import os

COMM_FILE = os.path.join("raw", "communities.pickle")
TWEETS_DIR = os.path.join("raw", "climate")
TWEETS_DUMP_FILE_PREFIX = os.path.join("raw", "tweets_")

with open("raw/communities.pickle", "rb") as f:
    communities = pickle.load(f)

counter = Counter()

for node in communities:
    counter[communities[node]] += 1

communities_list = []
for com, tot in counter.items():
    communities_list.append((com, tot))

communities_list.sort(key=lambda x: x[1], reverse=True)



# Now communities_list contains tuples (community, size) in descending order






all_tweets = tweets_directories_iter("raw", "climate_id.")

tweets_by_com = {}  # tweets_by_com[community] ---> list of tweets of that community

for tweet in all_tweets:
    user = tweet["user"]["id"]
    if not user in communities:
        continue
    community = communities[user]
    if not community in tweets_by_com:
        tweets_by_com[community] = []
    tweets_by_com[community].append(tweet["text"])



N_LARGEST_COMM = 15
print(communities_list[:N_LARGEST_COMM])
i = 0
for large_comm, large_comm_size in communities_list[:N_LARGEST_COMM]:
    i += 1
    if not large_comm in tweets_by_com:
        print('skipping')
        continue
    tweets = tweets_by_com[large_comm]
    with open(f"raw\\community_{i}.txt", "w", encoding="utf-8") as f:
        for t in tweets:
            print(t, file=f)
            print("\n",end="",file=f)
    print('found')


