#!/usr/bin/env python

import broom

# define the dict keys and values to loop over like this. the order they
# are added determines at which level they are in the nested for loop
dicts = [{'a': [1, 2]},
         {'b': range(3, 5)}]

sw = broom.Sweeper(dicts, result_names=['res1', 'res2'])

# dicts containing default parameters
default_params1 = {'a': 5,
                   'b': 2,
                   'c': 5,
                   'stringjoe': 'a string!'}

default_params2 = {'a': 1,
                   'b': 2,
                   's': 6,
                   'stringjoe': 'another string!'}

# save the original default parameters in sweeper object
# to self.default_params
sw.orig_default_params(default_params1, default_params2)
sw.default_params(default_params1, default_params2)


def calculate_stuff1(a=1, b=2, c=4, stringjoe='joe'):
    return (a * c) ** b


def calculate_stuff2(a=7, b=2, s=5, stringjoe='moe'):
    return (b * s) ** a


# the self.looper attribute is to be looped over
for params in sw.looper:
    # update default parameter dicts
    broom.update_dict_if_key_exists(default_params1, params)
    broom.update_dict_if_key_exists(default_params2, params)

    # calculate and append to self.results
    res1 = calculate_stuff1(**default_params1)
    res2 = calculate_stuff2(**default_params2)

    sw.append('res1', res1)
    sw.append('res2', res2)
