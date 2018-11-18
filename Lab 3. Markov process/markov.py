import numpy
from numpy.linalg.linalg import LinAlgError

def build_coeff_matrix(matrix):
    matrix = numpy.array(matrix)
    count = len(matrix)
    res = numpy.zeros((count, count))
    for state in range(count - 1):
        for col in range(count):
            res[state, state] -= matrix[state, col]
        for row in range(count):
            res[state, row] += matrix[row, state]

    for state in range(count):
        res[count - 1, state] = 1
    return res

def build_augmentation_matrix(count):
    res = [0 for i in range(count)]
    res[count - 1] = 1
    return numpy.array(res)

def get_system_times(matrix):
    try:
        res = numpy.linalg.solve(build_coeff_matrix(matrix), build_augmentation_matrix(len(matrix)))
    except LinAlgError:
        res = []
    return res