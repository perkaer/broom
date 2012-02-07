#!/usr/bin/env python

import itertools as it
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


def how_does_dict_pass(*args):
    for a in args:
        print a


class Sweeper(object):
    """
    class for doing parameter investigations, by providing a convenient way
    of looping over nested loops
    """

    def __init__(self, *args):
        self.sweep_dict = odict()
        for a in args:
            self.sweep_dict.update(a)

        self.looper = self.loop_generator()

    def loop_generator(self):
        for p in it.product(*self.sweep_dict.values()):
            yield dict(zip(self.sweep_dict.keys(), p))


if __name__ == '__main__':

    # define the dict keys and values to loop over like this. the order they
    # are added determines at which level they are in the nested for loop
    sw = Sweeper({'a': [1, 2, 2]},
                 {'b': range(6)},
                 {'stringjoe': ['per', 'er', 'l33t', 'haxx0r']})

    # dicts containing default parameters
    default_params1 = {'a': 5,
                       'c': 66,
                       'stringjoe': 'a string!'}

    default_params2 = {'b': 2,
                       's': 66,
                       'stringjoe': 'a string!'}

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
