import halstead.process as process
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


def plot_function_length_pairs(repo_results, join=False):
    """TODO: Docstring for multiple_repository_function_pairs.

    :repo_results: TODO
    :returns: TODO

    """

    def plot_scatters(ns, n_hats, axis, name, color=None):
        if color:
            axis.scatter(ns, n_hats, alpha=0.90, label=name, color=color)
        else:
            axis.scatter(ns, n_hats, alpha=0.90, label=name)

        axis.set_xlabel("Program length (distinct operators + distinct operands)")
        axis.set_ylabel("Calculated program length")

    def plot_lines(ns, n_hats, axis, name, color=None):
        slope, intercept, r_value, _, _ = scipy.stats.linregress(ns, n_hats)
        line = np.poly1d([slope, intercept])
        s = " ({})".format(name) if name else ""
        if color:
            axis.plot(ns, line(ns), color=color)
        else:
            axis.plot(ns, line(ns))

    if join:
        fig = plt.figure()
        ax = fig.gca()

        for name, result in repo_results:
            ns, n_hats = process.get_function_length_pairs(result)
            plot_scatters(ns, n_hats, ax, name)
            plot_lines(ns, n_hats, ax, name)

        ax.legend()

    else:
        for name, result in repo_results:
            fig = plt.figure()
            ax = fig.gca()

            ns, n_hats = process.get_function_length_pairs(result)
            plot_scatters(ns, n_hats, ax, name)
            plot_lines(ns, n_hats, ax, name)
            ax.legend()
