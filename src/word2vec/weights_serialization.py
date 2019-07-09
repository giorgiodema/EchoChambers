def save_array(matrix, path):
    '''Saves a matrix as a text file in the specified path

    Parameters
    matrix: the 2D patrix to save
    path: the path to use to save the matrix
    '''

    with open(path, 'w', encoding='utf-8') as txt:
        for row in matrix:
            for j in range(len(row)):
                print(row[j], file=txt, end=' ')

def save_array(path):
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