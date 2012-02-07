#!/usr/bin/env python

import itertools as it
import numpy as np
# from misctools import datestamp
from collections import OrderedDict as odict

# see: http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists


def update_dict_if_key_exists(updatee, updater):
    """
    wrapper for the update method for dictionaries, which only updates a key
    if it exists

    input:
    updatee: dict to be updated
    updater: dict containing the updates

    output:
    updatee is updated in-place, method style
    """
    updatee.update({k: v for k, v in updater.iteritems() if k in updatee.keys()})


# use odict to control the loop order of the entries
input_dict = odict()
input_dict['g'] = np.arange(8, 10)
input_dict['s'] = np.arange(11, 15)
input_dict['bs'] = np.arange(3, 5)

print input_dict

dict1 = {'s': 1,
         'as': 'sad'}

dict2 = {'g': 1,
         'as': 'sad'}

print dict1
print dict2

# update_dict_if_key_exists(dict1, input_dict)
# update_dict_if_key_exists(dict2, input_dict)

# print dict1
# print dict2

testdict = {}

results = []
for p in it.product(*input_dict.values()):
    kws = dict(zip(input_dict.keys(), p))
    print kws
    update_dict_if_key_exists(dict1, kws)
    update_dict_if_key_exists(dict2, kws)
    print dict1
    print dict2
    print '*' * 5
    # laser(dict1, dict2)
    # results.append(np.prod(p))
