from radon.metrics import h_visit, HalsteadReport, Halstead
from glob import glob
import multiprocessing as mp
import scipy.stats
import numpy as np


def fix_pool_results(results):
    fixed = []
    for (total, functions) in results:
        function_results = []
        for (name, visitor) in functions:
            function_results.append((name, HalsteadReport(*visitor)))

        report = HalsteadReport(*total)

        fixed.append(Halstead(report, function_results))

    return fixed


if __name__ == "__main__":
    names = glob("/home/rwb/Dropbox/sympy/sympy/**/*.py", recursive=True)

    def func(name):
        with open(name) as f:
            # Return a tuple because pickle is fucking stupid.
            res = h_visit(f.read())
            total = tuple(res.total)
            functions = [(name, tuple(report)) for (name, report) in res.functions]

            return (total, functions)

    with mp.Pool() as pool:
        results = pool.map(func, names)

    def flatten(list_of_lists):
        return [x for l in list_of_lists for x in l]

    results = fix_pool_results(results)
    function_results = flatten([res.functions for res in results if res.functions])
    function_results = [pair[-1] for pair in function_results]

    pairs = [(res.length, res.calculated_length) for res in function_results]
    ns, n_hats = zip(*pairs)

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(ns, n_hats)

    line = np.poly1d([slope, intercept])
