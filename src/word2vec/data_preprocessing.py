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
    with open(path, 'r') as ls:
        words = [int(line.split(' ')[1]) for line in ls if len(line) > 0]

    # build the direct and inverse mappings
    direct_map, inverse_map = dict(), dict()
    for i, word in enumerate(words):
        direct_map[word] = i
        inverse_map[i] = word

    return words, direct_map, inverse_map

def load_dataset(path, min_size):
    '''Loads a dataset of sentences

    Parameters:
    path: the path of the dataset file to load
    min_size: the minimum number of words in loaded sentences

    Returns:
    dataset: a vector of sentences (vectors of indices)
    '''

    dataset = []
    with open(path, 'r') as ls:
        for line in ls:
            if (len(line) == 0) continue
            tokens = line.split(' ')
            if (len(tokens) < min_size) continue
            dataset += [[int(token) for token in tokens]]

    return dataset
