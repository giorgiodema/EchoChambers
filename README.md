# Mapping the echo-chambers on Twitter network

Community identification and word polarization.

_Slides_ available [here](https://docs.google.com/presentation/d/e/2PACX-1vRAW6A-_3HRHTB_rQj2nJ02R7WfD-ppgti8wvY0gZQP5xpYYvJ_HgBbTd5gXyLWN4IsJJkOfNsUh4ET/pub?start=false&loop=false&delayms=10000&slide=id.p)

## Introduction
Social networks are often blamed for facilitating the formation of communities of users that 
share the same ideology on some topic (e.g. politics) and have little exposure to alternative opinions. This renders the partecipating users prone to spreading misinformation, since the characterization of the network sustains the propagation of false rumors without barriers.
These communities are often oblivious to, or openly hostile towards, alternative perspectives.


## Our Work
What we wanted to do is:
 1. Programmatically find users' communities 
 2. Check whether or not they result to be polarized on a specific view for the "climate change" selected topic
 3. Apply [__Word2Vec__](https://it.wikipedia.org/wiki/Word2vec) to detect "deviated" words, which are words that are used in different context when switching from a community to the other. Some of them are reported in the second-last slide
 
## Steps

 - __Download dataset__ [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/5QCCUU) of tweets related to climate change topic

 - __Build user graph__, assigning a (undirected weighted) link between users following policies like number of retweets between them, comments, same links shared, etc...

 - __Programmatically find graph communities__ through [Louvain's method](https://en.wikipedia.org/wiki/Louvain_modularity)

 - __Check communities polarization__ by looking at the tweets by users partecipating in the communities. For comparison, some tweets are reported in the second-last slide

 - __Check word polarization between communities__ using Word2Vec

## References
This project was partially inspired by the paper "Mapping the echo-chamber: detecting and characterizing partisan networks on Twitter", by Armineh Nourbakhsh, Xiaomo Liu, Quanzhi Li, Sameema Shah.
