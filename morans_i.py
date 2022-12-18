import numpy as np


def morans_i(array: np.array):
    morans_i = np.zeros_like(array)
    avg = np.average(array)

    m2 = np.average((array - avg)**2)

    for x in range(morans_i.shape[0]):
        for y in range(morans_i.shape[1]):
            morans_i[x, y] = (array[x, y] - avg)/m2 * sum(get_rook_neighbors((x, y), array) - avg)

    return morans_i


def get_rook_neighbors(index: tuple, array: np.array):
    neighbors = []
    if index[0] - 1 >= 0:
        neighbors.append(array[index[0] - 1, index[1]])
    if index[0] + 1 < array.shape[0]:
        neighbors.append(array[index[0] + 1, index[1]])
    if index[1] - 1 >= 0:
        neighbors.append(array[index[0], index[1] - 1])
    if index[1] + 1 < array.shape[1]:
        neighbors.append(array[index[0], index[1] + 1])

    return neighbors

