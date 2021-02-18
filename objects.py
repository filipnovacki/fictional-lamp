from itertools import product, chain, repeat

import numpy as np


def draw_circle(segments=10, r=0.5, colors=False):
    segment_len = np.math.tau / segments
    array = np.array([], dtype=np.float32)

    if not colors:
        array = np.append(array, [0.0, 0.0])
    else:
        array = np.append(array, [0.0, 0.0, 0.0, 0.0, 0.5])
    for x in range(segments + 1):
        x_coord = np.cos(x * segment_len)
        y_coord = np.sin(x * segment_len)
        if colors:
            row = [r * x_coord, r * y_coord, x_coord, y_coord, 0.5]
        else:
            row = [r * x_coord, r * y_coord]

        print(row)
        array = np.append(array, row)
    return array


_RECTANGLE_INDICES = [0, 1, 3, 0, 2, 3]


def draw_rectangle(a=0.5, b=0.7, colors=True):
    """
    Returns points for drawing rectangle
    :param colors: Add colors to the array or not
    :param a: length of side a
    :param b: length of side b
    :return: dictionary of elements "vertices" and "indices" containing vertices and incides
    """

    if not colors:
        return_vertices = np.array(list(chain(*product([1, -1], repeat=2))), dtype=np.float32) * list(
            chain(*repeat([a, b], times=4)))
    else:
        return_vertices = np.array([], dtype=np.float32)
        for point in np.array(list((product([1, -1], repeat=2)))) * list((repeat([a, b], times=4))):
            return_vertices = np.append(return_vertices, np.append(point, [1.0, 0.8, 0.5, 1]))

    return {
        "vertices": return_vertices,
        "indices": _RECTANGLE_INDICES
    }


def draw_cube(side_a=0.5, side_b=0.6, side_c=0.7, colors=False):
    if not colors:
        return_vertices = np.array(list(chain(*product([1, -1], repeat=3))), dtype=np.float32)
    else:
        return_vertices = np.array([], dtype=np.float32)
        for point in np.array(list((product([1, -1], repeat=3)))) * list((repeat([side_a, side_b, side_c], times=8))):
            return_vertices = np.append(return_vertices, np.append(point, [np.random.random(), 0.299, 0.499]))
    return return_vertices


_CUBE_INDICES = [
    0, 1, 3, 0, 2, 3,  # desna strana
    5, 7, 6, 5, 4, 6,  # lijeva strana
    4, 0, 2, 4, 6, 2,  # prednja strana
    1, 3, 7, 1, 5, 7,  # straznja strana
    0, 1, 5, 0, 4, 5,  # gornja strana
    2, 3, 7, 2, 6, 7   # donja strana
]