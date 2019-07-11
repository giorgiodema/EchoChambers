
import os
import pickle
from collections import Counter
from matplotlib  import pyplot as plt


from tweet_parser_utils import tweets_directories_iter

TWEET_COUNTER_PATH = open(os.path.join("raw", "tweet_counter.pickle"))

if not os.path.isfile(TWEET_COUNTER_PATH):
    tweet_counter = Counter()
    all_tweets = tweets_directories_iter("raw", "climate_id")
    for tweet in all_tweets:
        userid = tweet["user"]["id"]
        tweet_counter[userid] += 1

    with open("tweet_counter.pickle", "wb") as f:
        pickle.dump(tweet_counter, f)

else:
    with open("tweet_counter.pickle", "rb") as f:
        tweet_counter = pickle.load(f)



plt.rcParams.update({'font.size': 18.3})
plt.rc('legend', fontsize=10)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

values = tweet_counter.values()

n_tweets = Counter()
for val in values:
    n_tweets[val] += 1

X, Y = [], []
threshold = 0.9
found_threshold = False
s = 0
tot = sum(n_tweets.values())

for x in range(max(values)):
    X.append(x)
    Y.append(n_tweets[x])
    if x<10:
        print(f"#{x} {n_tweets[x]}")
    s += n_tweets[x]
    if not found_threshold and s/tot > threshold:
        found_threshold = True
        print(f"{threshold*100}% of nodes tweeted less than {x} tweets")

print(f"tot {tot}")

plt.xlim((-10,250))
plt.ylim((0,200))

plt.xlabel("# Tweets")
plt.ylabel("# Users")

plt.gcf().subplots_adjust(bottom=0.15, left=0.15)

plt.plot(X,Y, color="goldenrod", lw=1.6)
#plt.savefig("dataset_visualization.png", dpi=300)
plt.show()

