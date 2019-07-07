import os
import re

PATH = os.path.join("fake_news_dataset","fake.csv")

# Return the set of domains extracted by kaggle and a dictionary with
# the score of each domain
def load():
        with open(PATH, 'r', encoding='utf-8') as f:
                data = f.read()
                urls = re.findall('http[s]?://.[^/]*/',data)
                urls_set = set(urls)
                scores = {}
                for url in urls_set:
                        scores[url] = urls.count(url)
        return urls_set,scores