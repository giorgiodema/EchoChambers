def load_dictionary(path):
    '''Loads a dictionary and builds the words vector and mappings

    Parameters:
    path: the path of the dictionary file to load

    Returns:
    words: the vector of words in the dictionary
    direct_map: a mapping of words to their dictionary index
    inverse_map: a mapping of indices to words in the dictionary
    '''

    # load the words vector
    words = []
    with open(path, 'r', encoding='utf-8') as ls:
        for line in ls:
            if len(line) <= 1: continue
            words += [line.rstrip().split(' ')[1]]

    # build the direct and inverse mappings
    direct_map, inverse_map = dict(), dict()
    for i, word in enumerate(words):
        direct_map[word] = i
        inverse_map[i] = word

    return words, direct_map, inverse_map

def load_dataset(path, min_size):
    '''Loads a dataset of tweets

    Parameters:
    path: the path of the dataset file to load
    min_size: the minimum number of words in loaded tweets

    Returns:
    dataset: a vector of tweets (vectors of indices)
    '''

    dataset = []
    with open(path, 'r', encoding='utf-8') as ls:
        for line in ls:
            if len(line) <= 1: continue
            tokens = line.rstrip().split(' ')
            if len(tokens) < min_size: continue
            dataset += [[int(token) for token in tokens]]

    return dataset

def generate_batches(dataset, window_size, batch_size):
    '''Enumerates an infinite number of batches from the given dataset

    Parameters:
    dataset: the list of tweets in the dataset
    window_size: the size of the sliding window in each tweet
    batch_size: the size of each training batch
    '''

    # Use a generator to loop over the whole dataset and return new
    # batches without having to manually return to the previous position
    # every time a new batch is requested: the generator will keep track of this
    samples, labels = [], []
    k = 0
    sample_tokens = window_size * 2 + 1
    while True:
        for tweet in dataset:
            for i in range(sample_tokens - 5):
                samples += [tweet[window_size]] # center token
                targets = []
                for j in range(i, sample_tokens + i):
                    if j != i + window_size:
                        targets += [tweet[j]]
                labels += [targets]
            
            k += 1
            if k == batch_size:

                # debug
                assert len(samples) == batch_size, 'The samples size doesn\'t match the batch size'
                assert len(labels) == batch_size, 'The labels size doesn\'t match the batch size'

                yield samples, labels
                samples, labels = [], []
                k = 0
