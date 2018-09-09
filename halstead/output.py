import halstead.process as process
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


def plot_function_length_pairs(results, axis, name=None):
    """TODO: Docstring for plot_function_length_pairs.

    :results: TODO
    :returns: TODO

    """
    ns, n_hats = process.get_function_length_pairs(results)
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(ns, n_hats)

    line = np.poly1d([slope, intercept])

    s = " ({})".format(name) if name else ""
    axis.plot(ns, line(ns), label="line of best fit{}".format(s))
    axis.scatter(ns, n_hats, alpha=0.90)
    axis.set_xlabel("Program length (distinct operators + distinct operands)")
    axis.set_ylabel("Calculated program length")


def plot_multiple_repository_function_pairs(repo_results, join=False):
    """TODO: Docstring for multiple_repository_function_pairs.

    :repo_results: TODO
    :returns: TODO

    """
    if join:
        fig = plt.figure()
        ax = fig.gca()

        for name, result in repo_results:
            plot_function_length_pairs(result, ax, name)
        ax.legend()

    else:
        for name, result in repo_results:
            fig = plt.figure()
            ax = fig.gca()
            plot_function_length_pairs(result, ax, name)
            ax.legend()
