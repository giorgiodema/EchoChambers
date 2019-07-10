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
