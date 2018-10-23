import numpy as np
import os
import shutil

def replace_array_with_map(arr, map_dict, new_type=object):
    if type(map_dict) == type([]):
        map_dict = dict(zip(range(0, len(map_dict)), map_dict))
    newArray = np.copy(arr).astype(new_type)
    for k, v in map_dict.items(): newArray[arr == k] = v
    return newArray


#         # Remap labels array
#         map_obj = self.calculate_angles() # a dictionary remapping
#         f = np.vectorize(lambda x: map_obj[x])
#         self.labels = f(self.labels)


import math

def integer_to_coordinates(_int, m=None, n=None, method="horizontal"):
    def get_k(_int):
        return int(1 / 2 * ((8 * _int + 1) ** .5 - 1))

    assert _int < m * n
    if method == "vertical":  # fill a column first
        j = int(_int / m)
        i = _int - j * m
        return i, j
    if method == "horizontal":
        i = int(_int / n)
        j = _int - i * n
        return i, j
    if method == "diagonal": # only works for squares
        reverse = False

        # Once we're passed the diagonal, we reverse coordinates
        middle_k = math.ceil(get_k(m * n / 2)) + 1
        if _int > middle_k * (middle_k + 1) / 2 - 1:
            reverse = True
            _int = m * n - _int - 1
        k = int(1 / 2 * ((8 * _int + 1) ** .5 - 1))
        i = _int - 1 / 2 * k * (k + 1)
        j = k - i
        if reverse:
            return int(m - i - 1), int(n - j - 1)
        else:
            return int(i), int(j)

def cartesian_product(arr1, arr2):
    return np.transpose([np.tile(arr1, len(arr2)), np.repeat(arr2, len(arr1))])

def random_argmax(arr):
    return np.random.choice(np.flatnonzero(arr == arr.max()))


def is_iterable(object, string_is_iterable=True):
    """Returns whether object is an iterable. Strings are considered iterables by default.
    Args:
        object (?): An object of unknown type
        string_is_iterable (bool): True (default) means strings will be treated as iterables
    Returns:
        bool: Whether object is an iterable
    """

    if not string_is_iterable and type(object) == type(""):
        return False
    try:
        iter(object)
    except TypeError as te:
        return False
    return True

def make_dir(paths, delete=False):
    if isinstance(paths, str) or not is_iterable(paths):
        paths = [paths]
    for p in paths:
        if os.path.isdir(p) and delete:
            try:
                shutil.rmtree(p)
            except:
                print("Could not delete folder")
        if not os.path.isdir(p):
            # make parent recursively
            (parent, child) = os.path.split(p)
            make_dir([parent])
            os.mkdir(p)
            return True
    return False

def normalize(arr, as_list=True):
    result = arr/np.sum(arr)
    if as_list:
        result = result.tolist()
    return result