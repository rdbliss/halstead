import numpy as np
import scipy.stats


def line_of_best_fit(ns, n_hats):
    slope, intercept, r_value, _, _ = scipy.stats.linregress(ns, n_hats)
    line = np.poly1d([slope, intercept])

    residuals = [line(n) - n_hat for (n, n_hat) in zip(ns, n_hats)]

    return line, residuals
