import os
import re

PATH = os.path.join("fake-news-dataset","fake.csv")

# Return a set of domains extracted from kaggle dataset
def load():
        with open(PATH, 'r', encoding='utf-8') as f:
                data = f.read()
                urls = set(re.findall('http[s]?://.[^/]*/',data))
        return urls