def save_array(matrix, path):
    '''Saves a matrix as a text file in the specified path

    Parameters
    matrix: the 2D matrix to save
    path: the path to use to save the matrix
    '''

    with open(path, 'w', encoding='utf-8') as txt:
        for row in matrix:
            for j in range(len(row)):
                print(row[j], file=txt, end=' ')

def load_array(path):
    '''Loads a matrix from the specified file

    Parameters:
    path: the path of the file with the matrix to load
    '''

    with open(path, 'r', encoding='utf-8') as txt:
        matrix = []
        for line in txt:
            row = [float(n) for n in line.strip().split(' ')]
            matrix += [row]
        return matrix

def save_vector(vector, path):
    '''Saves a vector as a text file in the specified path

    Parameters
    vector: the vector to save
    path: the path to use to save the matrix
    '''

    with open(path, 'w', encoding='utf-8') as txt:
        for value in vector:
            print(value, file=txt)

def load_vector(path):
    '''Loads a vector from the specified file

    Parameters:
    path: the path of the file with the vector to load
    '''

    with open(path, 'r', encoding='utf-8') as txt:
        return [
            float(line.strip())
            for line in txt
            if len(line) > 1
        ]
