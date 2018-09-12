from radon.metrics import h_visit, HalsteadReport, Halstead
from glob import glob
import multiprocessing as mp
import os.path


def fix_pool_results(results):
    """
    Because of pickle issues, our results are returned as raw tuples. This
    turns everything back into the nametuples that radon provides.
    """
    fixed = []
    for (total, functions) in results:
        function_results = []
        for (name, visitor) in functions:
            function_results.append((name, HalsteadReport(*visitor)))

        report = HalsteadReport(*total)

        fixed.append(Halstead(report, function_results))

    return fixed


def get_function_length_pairs(results):
    def flatten(list_of_lists):
        return [x for l in list_of_lists for x in l]

    function_results = flatten([res.functions for res in results if res.functions])
    function_results = [result for name, result in function_results]

    pairs = [(res.length, res.calculated_length) for res in function_results]
    ns, n_hats = zip(*pairs)

    return (ns, n_hats)


def pickle_func(name):
    with open(name) as f:
        # Return a tuple because pickle is fucking stupid.
        try:
            res = h_visit(f.read())
        except SyntaxError:
            print("Ign: Invalid syntax in '{}'".format(name))
            return None

        total = tuple(res.total)
        functions = [(name, tuple(report)) for (name, report) in res.functions]

        return (total, functions)


def get_dir_halstead(path):
    search_path = os.path.join(path, "**/*.py")
    names = glob(search_path, recursive=True)

    with mp.Pool() as pool:
        results = [res for res in pool.map(pickle_func, names) if res]

    fixed = fix_pool_results(results)

    # Remove all files that have zero length.
    pos_length = [hal for hal in fixed if hal.total.length > 0]
    compl = [hal for hal in fixed if hal.total.length == 0]
    pos_func = []

    # Remove all functions that have zero length.
    for hal in pos_length:
        funcs = [(name, func) for name, func in hal.functions if func.length > 0]
        if funcs:
            pos_func.append(Halstead(total=hal.total, functions=funcs))

    return pos_func
