#!/usr/bin/env python

import broom
import numpy as np


# define the dict keys and values to loop over like this. the order they
# are added determines at which level they are in the nested for loop
sw = broom.Sweeper({'a': [1, 2]},
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
    broom.update_dict_if_key_exists(default_params1, params)
    broom.update_dict_if_key_exists(default_params2, params)

    print 'updated default_params1', default_params1
    print 'updated default_params2', default_params2
    print '*' * 5

    # pass dicts to whatever and save results
