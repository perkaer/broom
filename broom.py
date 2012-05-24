#!/usr/bin/env python

import itertools as it
from collections import OrderedDict as odict
import numpy as np
from copy import deepcopy
import pickle

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
    updatee.update({k: v
        for k, v in updater.iteritems()
        if k in updatee.keys()})


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
            self._sweep_shape = \
            np.array([len(x) for x in self.sweep_dict.values()])
            nan_array = np.zeros(self._sweep_shape).astype(object)
            nan_array[:] = np.nan

            self.results = {}
            for name in result_names:
                self.results.update({name: nan_array.copy()})

    def default_params(self, *dicts):
        self.default_params = []
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

    def _how_far(self):
        where_now = \
        np.array(np.unravel_index(self._n_loop, self._sweep_shape), dtype=float)
        how_far = list(100 * (1 + where_now) / self._sweep_shape)
        return ' '.join([str(x) + '%' for x in how_far])

    def plot_results(self, results_to_plot='all',
            filename='results', **what_to_plot):
        """
        plot data contained in self.results

        input:
        results_to_plot: list of strings of results to include in plot.
        default is all

        filename: where to save plot

        what_to_plot:
        kwarg of the form: param1='x-axis', param2=[n1, n2, ..]
        'x-axis': implies parameter on x-axis
        [n1, n2, ..]: slice selecting specific values

        if a sweeping parameter is not listed all values are plotted
        """

# In [12]: ixgrid = np.ix_([01,],[0,1,2],[1])

# In [13]: ixgrid = np.ix_([0,1],[0,1,2],[1])

# In [14]: YY[ixgrid]
# Out[14]:
# array([[[41.28],
#         [55.04],
#         [68.8]],

#        [[51.84],
#         [69.12],
#         [86.4]]], dtype=object)

# In [15]: YY[ixgrid].shape
# Out[15]: (2, 3, 1)

# In [16]: YY[ixgrid].squeeze
# Out[16]: <function squeeze>

# In [17]: YY[ixgrid].squeeze()
# Out[17]:
# array([[41.28, 55.04, 68.8],
#        [51.84, 69.12, 86.4]], dtype=object)

# In [18]: YY
# Out[18]:

        import matplotlib as mpl
        import sys
        from matplotlib.font_manager import FontProperties
        # this is for display-less stuff
        if sys.platform != 'darwin': mpl.use('Agg')
        import pylab as pl

        if 'x-axis' not in what_to_plot.values():
            raise ValueError('must specify parameter for x-axis')

        # fill out what_to_plot dict with whats missing
        what_to_plot_real = odict()
        for k, v in self.sweep_dict.iteritems():
            if k not in what_to_plot.keys():
                what_to_plot_real.update({k: range(len(v))})
            else:
                what_to_plot_real.update({k: what_to_plot[k]})

        # get indexes for x-axis parameter
        xtmp = [(k, range(len(self.sweep_dict[k])))
            for k, v in what_to_plot.iteritems()
            if v == 'x-axis'][0]
        x_axis_param, x_axis_idx = xtmp

        num_plots = np.prod([len(v)
            for v in what_to_plot_real.itervalues()
            if v != 'x-axis'])

        # update x_axis param values
        what_to_plot_real[x_axis_param] = [x_axis_idx]

        if results_to_plot == 'all':
            results_to_plot = self.results.keys()
        elif isinstance(results_to_plot, str):
            results_to_plot = [results_to_plot]

        fig = pl.figure(figsize=(10, 6))
        ax = fig.add_axes([0.075, 0.085, 0.65, 0.86])
        label_str_list = []
        x = self.sweep_dict[x_axis_param]
        for r_plot in results_to_plot:
            for idx_tuple in it.product(*what_to_plot_real.values()):
                label_str = r_plot
                y = self.results[r_plot][idx_tuple]
                # label string
                for n, k in enumerate(what_to_plot_real.iterkeys()):
                    i = idx_tuple[n]
                    if isinstance(i, int):
                        label_str += ',' + k + '=%5.3e' % self.sweep_dict[k][i]
                ax.plot(x, y, '.', label=label_str)
        ax.legend(loc=(1.01, 0.03), prop=FontProperties(size=6))
        # pl.legend(loc='best', prop=FontProperties(size=5))
        ax.set_xlabel(x_axis_param)
        ax.set_ylabel(', '.join(results_to_plot))
        pl.savefig(filename + '.pdf', format='pdf')
        pl.close('all')

        return

    def save_to_disk(self, fn='generic.sweep'):
        """
        saves important data to disk, these are:
        self.results
        self.default_params
        self.sweep_dict

        input:
        fn: filename of saved file

        note:
        you cannot pickle (save) or copy objects with generators in python
        hence this selection, else just saving self would be easier
        """
        to_save = {}
        to_save['results'] = self.results
        to_save['default_params'] = self.default_params
        to_save['sweep_dict'] = self.sweep_dict
        f = open(fn, 'w')
        pickle.dump(to_save, f)
        f.close()

    def _loop_generator(self):
        for n_loop, p in enumerate(it.product(*self.sweep_dict.values())):
            self._n_loop = n_loop
            kwargs = dict(zip(self.sweep_dict.keys(), p))
            # update default param dicts
            for d in self.default_params:
                update_dict_if_key_exists(d, kwargs)
            yield self._how_far(), kwargs
