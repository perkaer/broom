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

    def __init__(self, dicts=None, result_names=None):

        if dicts is not None:
            # add input dicts to OrderedDict
            self.sweep_dict = odict()
            for a in dicts:
                self.sweep_dict.update(a)

            # generator object
            self.looper = self._loop_generator()

        self._create_results_dict(result_names)

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
            filename='results', plot_fct='plot',
            plot_marker=True,
            plot_title=None, **what_to_plot):
        """
        plot data contained in self.results

        input:
        results_to_plot: list of strings of results to include in plot.
        default is all

        filename: where to save plot

        plot_title: string with plot title
        default is self.default_params

        what_to_plot:
        kwarg of the form: param1='x-axis', param2=[n1, n2, ..]
        'x-axis': implies parameter on x-axis
        [n1, n2, ..]: slice selecting specific values

        plot_marker: plot marker or not

        if a sweeping parameter is not listed all values are plotted
        """

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

        if plot_marker:
            marker_str = 'osv'
        else:
            marker_str = ['']

        linestyler = it.cycle([''.join(n)
            for n in it.product(marker_str, ['-', '--', ':'], 'rbgcmk')])

        if results_to_plot == 'all':
            results_to_plot = self.results.keys()
        elif isinstance(results_to_plot, str):
            results_to_plot = [results_to_plot]

        fig = pl.figure(figsize=(10, 6))
        ax = fig.add_axes([0.085, 0.085, 0.65, 0.8])
        label_str_list = []
        x = self.sweep_dict[x_axis_param]
        markersize = 4

        for r_plot in results_to_plot:
            for idx_tuple in it.product(*what_to_plot_real.values()):
                label_str = r_plot
                y = self.results[r_plot][idx_tuple]
                # label string
                for n, k in enumerate(what_to_plot_real.iterkeys()):
                    i = idx_tuple[n]
                    if isinstance(i, int):
                        label_str += ',' + k + '=%5.3e' % self.sweep_dict[k][i]
                if plot_fct == 'plot':
                    ax.plot(
                        x, y,
                        linestyler.next(),
                        label=label_str,
                        markersize=markersize)
                elif plot_fct == 'semilogx':
                    ax.semilogx(
                        x, y,
                        linestyler.next(),
                        label=label_str,
                        markersize=markersize)
                elif plot_fct == 'semilogy':
                    ax.semilogy(
                        x, y,
                        linestyler.next(),
                        label=label_str,
                        markersize=markersize)
                elif plot_fct == 'loglog':
                    ax.loglog(
                        x, y,
                        linestyler.next(),
                        label=label_str,
                        markersize=markersize)
                else:
                    raise ValueError('plot_fct must a plot fct from pylab')

        if plot_fct == 'plot':
            ax.ticklabel_format(style='sci', useOffset=False, axis='both')
        elif plot_fct == 'semilogx':
            ax.ticklabel_format(style='sci', useOffset=False, axis='y')
        elif plot_fct == 'semilogy':
            ax.ticklabel_format(style='sci', useOffset=False, axis='x')

        ax.legend(loc=(1.01, 0.03), handlelength=2.5, prop=FontProperties(size=6))
        ax.grid()
        ax.set_xlabel(x_axis_param)
        ax.set_ylabel(', '.join(results_to_plot))
        if plot_title is None:
            plot_title = '\n'.join([str(defpar) for defpar in self.default_params])
        fig.text(0.5, 0.99, plot_title, ha='center', va='top', color='black', size=6)
        pl.savefig(filename + '.pdf', format='pdf')
        pl.close('all')

        return

    def plot3d_results(self, x_axis=None, y_axis=None, results_to_plot=None,
            filename='results', plot_title='joe', logplot=None,
            **what_to_plot):

        """plots data in self.results in a 3d plot

        input:

        x_axis: select sweep parameter for x-axis

        y_axis: see x_axis

        results_to_plot: string with result to plot

        logplot: take log on axes logplot, 'x', 'y', 'both'

        what_to_plot: keyword arguments of sweep parameters to plot.
        default is to plot all combinations
        example: ..., sweep1 = [0], sweep2 = [3, 7], ...

        """

        import matplotlib as mpl
        import sys
        from matplotlib.font_manager import FontProperties
        # this is for display-less stuff
        if sys.platform != 'darwin': mpl.use('Agg')
        import pylab as pl

        if x_axis is None or y_axis is None:
            raise ValueError('you must specify x_axis and y_axis')

        if (x_axis not in self.sweep_dict.keys() or
            y_axis not in self.sweep_dict.keys()):
            raise ValueError('invalid x_axis and y_axis')

        # build list containing all combinations of sweep params to plot
        uber_which_list = []

        if not what_to_plot:
            for k, v in self.sweep_dict.iteritems():
                if k == x_axis or k == y_axis:
                    uber_which_list.append([slice(0, len(v))])
                else:
                    uber_which_list.append(range(len(v)))
        else:
            raise NotImplementedError('not yet :)')

        if results_to_plot is None:
            raise ValueError('results_to_plot is None.. :)')
        else:

            xx_ax = self.sweep_dict[x_axis]
            yy_ax = self.sweep_dict[y_axis]

            xlabel = x_axis
            ylabel = y_axis

            if logplot == 'x':
                xx_ax = np.log(xx_ax)
                xlabel = 'log(' + x_axis + ')'
            elif logplot == 'y':
                yy_ax = np.log(yy_ax)
                ylabel = 'log(' + y_axis + ')'
            elif logplot == 'both':
                xx_ax = np.log(xx_ax)
                yy_ax = np.log(yy_ax)
                xlabel = 'log(' + x_axis + ')'
                ylabel = 'log(' + y_axis + ')'

            XX, YY = np.meshgrid(xx_ax, yy_ax)

            for n, which_list in enumerate(it.product(*uber_which_list)):

                sub_results_arr = self.results[results_to_plot][which_list]

                if not XX.shape == sub_results_arr.shape:
                    sub_results_arr = sub_results_arr.transpose()

                # handle nan's
                sub_results_arr = np.ma.masked_where(
                    np.isnan(sub_results_arr.astype(float)),
                    sub_results_arr.astype(float))

                now_params = ''
                for m, p in enumerate(which_list):
                    if not isinstance(p, slice):
                        now_params += \
                            self.sweep_dict.keys()[m] \
                            + ' : ' + \
                            str(self.sweep_dict[self.sweep_dict.keys()[m]][p]) \
                            + ', '

                # for subplot version, use pl.subplots ans iterate over
                # axes grid

                pl.pcolormesh(XX, YY, sub_results_arr)
                pl.xlabel(xlabel)
                pl.ylabel(ylabel)
                pl.colorbar()
                pl.axis('tight')
                pl.title(plot_title + '\n' + now_params, fontsize=6)
                pl.savefig(filename + '_' + str(n) + '.pdf')
                pl.close()

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

    def load_from_disk(self, fn='generic.sweep'):
        """
        loads important data from disk, these are:
        self.results
        self.default_params
        self.sweep_dict

        input:
        fn: filename of file to load

        note:
        you cannot pickle (save) or copy objects with generators in python
        hence this selection, else just saving self would be easier
        """

        f = open(fn, 'r')
        pickf = pickle.load(f)

        self.results = pickf['results']
        self.default_params = pickf['default_params']
        self.sweep_dict = pickf['sweep_dict']

        f.close()

    def _loop_generator(self):
        for n_loop, p in enumerate(it.product(*self.sweep_dict.values())):
            self._n_loop = n_loop
            kwargs = dict(zip(self.sweep_dict.keys(), p))
            # update default param dicts
            for d in self.default_params:
                update_dict_if_key_exists(d, kwargs)
            yield self._how_far(), kwargs
