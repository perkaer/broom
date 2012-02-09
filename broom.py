#!/usr/bin/env python

import itertools as it
from collections import OrderedDict as odict
import numpy as np

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
            res_shape = [len(x) for x in self.sweep_dict.values()]
            nan_array = np.zeros(res_shape).astype(object)
            nan_array[:] = np.nan

            self.results = {}
            for name in result_names:
                self.results.update({name: nan_array})

    def _loop_generator(self):
        for p in it.product(*self.sweep_dict.values()):
            yield dict(zip(self.sweep_dict.keys(), p))


if __name__ == '__main__':

    # define the dict keys and values to loop over like this. the order they
    # are added determines at which level they are in the nested for loop
    sw = Sweeper({'a': [1, 2]},
                 {'b': range(66, 69)},
                 {'stringjoe': ['l33t', 'haxx0r']})

    # dicts containing default parameters
    default_params1 = {'a': 5,
                       'c': 66,
                       'stringjoe': 'a string!'}

    default_params2 = {'b': 2,
                       's': 22,
                       'stringjoe': 'another string!'}

    print 'default_params1', default_params1
    print 'default_params2', default_params2

    # the self.looper attribute is to be looped over
    for params in sw.looper:
        # update default parameter dicts
        update_dict_if_key_exists(default_params1, params)
        update_dict_if_key_exists(default_params2, params)

        print 'updated default_params1', default_params1
        print 'updated default_params2', default_params2
        print '*' * 5

        # pass dicts to whatever and save results
