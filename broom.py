#!/usr/bin/env python

import itertools as it
from collections import OrderedDict as odict
import numpy as np
from copy import deepcopy

# inspiration from these sources:
# http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists


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


class Sweeper(object):
    """
    class for doing parameter investigations, by providing a convenient way
    of looping over nested loops
    """

    def __init__(self, dicts, result_names=None):
        # add input dicts to OrderedDict
        self.sweep_dict = odict()
        for a in dicts:
            self.sweep_dict.update(a)

        self._create_results_dict(result_names)

        # generator object
        self.looper = self._loop_generator()

    def _create_results_dict(self, result_names):
        if result_names is not None:
            # find results array shape
            self._sweep_shape = [len(x) for x in self.sweep_dict.values()]
            nan_array = np.zeros(self._sweep_shape).astype(object)
            nan_array[:] = np.nan

            self.results = {}
            for name in result_names:
                self.results.update({name: nan_array})

    def save_default_params(self, *dicts):
        self.default_params = []
        # do a copy of default params
        dicts = deepcopy(dicts)
        for d in dicts:
            self.default_params.append(d)

    def append(self, result_name, result):
        # append result to the correct entry in self.results and
        # use the for loop in _loop_gen get the multi ravel index
        if result_name not in self.results.keys():
            estr = 'result name' + result_name + ' is not found in result dict!'
            raise ValueError(estr)

        self._mult_idx = np.unravel_index(self._n_loop, self._sweep_shape)
        self.results[result_name][self._mult_idx] = result

    def _loop_generator(self):
        for n_loop, p in enumerate(it.product(*self.sweep_dict.values())):
            self._n_loop = n_loop
            yield dict(zip(self.sweep_dict.keys(), p))
