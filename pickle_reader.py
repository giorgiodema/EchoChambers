import pickle

from pprint import pprint

data = pickle.load(open('domains_dump-3-LEVELS.pickle', 'rb'))

pprint(data)