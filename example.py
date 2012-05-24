#!/usr/bin/env python

import broom
import numpy as np

# define the dict keys and values to loop over like this. the order they
# are added determines at which level they are in the nested for loop
dicts_list = [
    {'a': np.arange(1, 6) * 1e8 * 1.1},
    {'b': np.arange(3, 10) * 1e-6 * 3.2},
    {'c': np.arange(0, 3) * 3.2}]

sw = broom.Sweeper(dicts_list, result_names=['res1', 'res2'])

# dicts containing default parameters
default_params1 = {'a': 5,
                   'b': 2,
                   'c': 5,
                   'stringjoe': 'a string!'}

default_params2 = {'a': 1,
                   'b': 2,
                   'c': 6,
                   'stringjoe': 'another string!'}

# set default parameters dicts to updated
sw.default_params(default_params1, default_params2)


def calculate_stuff1(a=1, b=2, c=4, stringjoe='joe'):
    return (a + c) * b


def calculate_stuff2(a=7, b=2, c=5, stringjoe='moe'):
    return (b + c) * a


# the self.looper attribute is to be looped over
for how_far, params in sw.looper:
    # print 'how far:', how_far, ', with params', params

    # calculate results, the default param dicts are updated automagically
    res1 = calculate_stuff1(**default_params1)
    res2 = calculate_stuff2(**default_params2)

    # append results
    sw.append('res1', res1)
    sw.append('res2', res2)

    sw.save_to_disk('saveme.sweep')

print sw.results
sw.plot_results(filename='all_results', results_to_plot='all', b='x-axis')
sw.plot_results(filename='res1', results_to_plot='res1', b='x-axis')
