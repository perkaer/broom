#!/usr/bin/env python

import broom

# define the dict keys and values to loop over like this. the order they
# are added determines at which level they are in the nested for loop
dicts = [{'a': [1, 2]},
         {'b': range(66, 69)},
         {'stringjoe': ['l33t', 'haxx0r']}]

sw = broom.Sweeper(dicts, result_names=['res1', 'res2'])

# dicts containing default parameters
default_params1 = {'a': 5,
                   'c': 66,
                   'stringjoe': 'a string!'}

default_params2 = {'b': 2,
                   's': 22,
                   'stringjoe': 'another string!'}

# save the original default parameters in sweeper object
# to self.default_params
sw.save_default_params(default_params1, default_params2)


def calculate_stuff1(a=1, c=4, stringjoe='joe'):
    return (a * c) ** 2


def calculate_stuff2(b=2, s=5, stringjoe='moe'):
    return (b * s) ** 2


# the self.looper attribute is to be looped over
for params in sw.looper:
    # update default parameter dicts
    broom.update_dict_if_key_exists(default_params1, params)
    broom.update_dict_if_key_exists(default_params2, params)

    # calculate and append to self.results
    sw.append('res1', calculate_stuff1(**default_params1))
    sw.append('res2', calculate_stuff2(**default_params2))
