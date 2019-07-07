import os
import re

PATH = os.path.join("src","domains_extractor","fake_news_dataset","fake.csv")

# Return the set of domains extracted by kaggle and a dictionary with
# the score of each domain
def load():
        with open(PATH, 'r', encoding='utf-8') as f:
                data = f.read()
                urls = re.findall(r'https?://.[^/\n \\"]*',data)
                urls_set = set(urls)
                scores = {}
                for url in urls_set:
                        scores[url] = urls.count(url)
                max_score = max(scores.values())
                avg_score = sum(scores.values())/len(scores.values())
                scores = {u:min(scores[u]/avg_score,1) for u in urls_set}
                
        return urls_set,scores