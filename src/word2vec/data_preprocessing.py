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
    with open(path, 'r') as file:
        words = [int(line.split(' ')[1]) if len(line) > 0 for line in file]

    # build the direct and inverse mappings
    direct_map, inverse_map = dict(), dict()
    for i, word in enumerate(words):
        direct_map[word] = i
        inverse_map[i] = word

    return words, direct_map, inverse_map
