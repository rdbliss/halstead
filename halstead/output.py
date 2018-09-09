import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import halstead.process as process


def plot_function_length_pairs(results):
    """TODO: Docstring for plot_function_length_pairs.

    :results: TODO
    :returns: TODO

    """
    ns, n_hats = process.get_function_length_pairs(results)
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(ns, n_hats)

    line = np.poly1d([slope, intercept])

    fig = plt.figure()

    plt.scatter(ns, n_hats)
    plt.plot(ns, line(ns), label="line of best fit")
    plt.plot(ns, ns, label="identity line")
    plt.xlabel("Program length (distinct operators + distinct operands)")
    plt.ylabel("Calculated program length")
