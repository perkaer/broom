#!/usr/bin/env python

import broom

sw = broom.Sweeper()

sw.load_from_disk('saveme.sweep')

print sw.results
sw.plot_results(filename='loaded_all_results',
    results_to_plot='all', plot_title='joe', b='x-axis')
sw.plot_results(filename='loaded_res1',
    results_to_plot='res1', b='x-axis')

sw.plot_results(filename='loaded_semilogx_all_results', plot_fct='loglog',
    results_to_plot='all', b='x-axis')
sw.plot_results(filename='loaded_semilogx_res1', plot_fct='loglog',
    results_to_plot='res1', b='x-axis')
