import numpy as np
import os

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

def make_dir(paths):
    if isinstance(paths, str) or not is_iterable(paths):
        paths = [paths]
    for p in paths:
        if not os.path.isdir(p):
            # make parent recursively
            (parent, child) = os.path.split(p)
            make_dir([parent])
            os.mkdir(p)
            return True
    return False
