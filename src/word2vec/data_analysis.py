import os
import numpy as np

def find_closest(target, matrix, n):
    '''Returns a list of the closest vectors from a matrix and an input index

    Parameters:
    target: the index of the target vector
    matrix: the matrix of values to read from
    n: the number of values to return

    Returns:
    a sorted list of the closest vectors (their indices)
    '''

    # calculate the distance to all the matrix rows
    vector = matrix[target]
    distances = [
        (np.linalg.norm(vector - row), i)
        for i, row in enumerate(matrix)
        if i != 0 and i != target
    ]

    # sort the distances and return an iterator over the results
    distances.sort(key=lambda x: x[0])
    for i, item in enumerate(distances):
        if (i >= n): break
        yield item[1]

if __name__ == "__main__":
    from data_preprocessing import load_dictionary
    from weights_serialization import load_array

    # constants
    BASELINE_WEIGHTS_PATH = r'C:\Users\Sergio\Documents\WIR\tmp\tweets_all_978d3bfaa50a4e028d4c740ba39578df\978d3bfaa50a4e028d4c740ba39578df_word-embeddings.ls'
    COMMUNITY_WEIGHTS_PATH = r'C:\Users\Sergio\Documents\WIR\tmp\tweets_all_978d3bfaa50a4e028d4c740ba39578df_1\978d3bfaa50a4e028d4c740ba39578df_word-embeddings.ls'
    DICTIONARY_PATH = r'C:\Users\Sergio\Documents\WIR\dataset\978d3bfaa50a4e028d4c740ba39578df_words.ls'
    RESULTS_PATH = r'C:\Users\Sergio\Documents\WIR\distances'
    RESULTS_NAME = '978d3bfaa50a4e028d4c740ba39578df_1'
    EMBEDDING_SIZE = 200        # dimension of the embedding vector

    # load the dictionary
    dictionary, _, inverse_map = load_dictionary(DICTIONARY_PATH)
    DICTIONARY_SIZE = len(dictionary)   # size of the loaded dictionary

    # load the word embeddings
    base_embeddings = load_array(BASELINE_WEIGHTS_PATH, DICTIONARY_SIZE, EMBEDDING_SIZE)
    community_embeddings = load_array(COMMUNITY_WEIGHTS_PATH, DICTIONARY_SIZE, EMBEDDING_SIZE)

    # calculate the distances
    distances = [
        (inverse_map[i], np.linalg.norm(base_embeddings[i] - community_embeddings[i]))
        for i in range(DICTIONARY_SIZE)
    ]
    distances.sort(key=lambda x: x[1], reverse=True)

    # save the results
    with open(os.path.join(RESULTS_PATH, '{}.ls'.format(RESULTS_NAME)), 'w', encoding='utf-8') as txt:
        for item in distances:
            print('{}, {}'.format(item[0], item[1]), file=txt)
