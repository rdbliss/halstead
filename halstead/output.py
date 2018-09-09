from .stats import line_of_best_fit
import halstead.process as process
import matplotlib.pyplot as plt
import brewer2mpl


def plot_function_length_pairs(repo_results, join=False):
    """TODO: Docstring for multiple_repository_function_pairs.

    :repo_results: TODO
    :returns: TODO

    """

    bmap = brewer2mpl.get_map('Dark2', 'qualitative', len(repo_results))
    colors = bmap.mpl_colors

    def plot_scatters(ns, n_hats, axis, name, color=None):
        if color:
            axis.scatter(ns, n_hats, alpha=0.90, label=name, color=color)
        else:
            axis.scatter(ns, n_hats, alpha=0.90, label=name)

        axis.set_xlabel("Program length")
        axis.set_ylabel("Expected program length")

    def plot_lines(ns, n_hats, axis, name, color=None):
        line, residuals = line_of_best_fit(ns, n_hats)

        s = " ({})".format(name) if name else ""
        if color:
            axis.plot(ns, line(ns), color=color)
        else:
            axis.plot(ns, line(ns))

    if join:
        fig = plt.figure()
        ax = fig.gca()
        ax.set_title("Halstead Metrics: Expected Length")

        for k, (name, result) in enumerate(repo_results):
            ns, n_hats = process.get_function_length_pairs(result)
            plot_scatters(ns, n_hats, ax, name, color=colors[k % len(colors)])
            plot_lines(ns, n_hats, ax, name, color=colors[k % len(colors)])

        ax.legend()

    else:
        for k, (name, result) in enumerate(repo_results):
            fig = plt.figure()
            ax = fig.gca()

            ax.set_title("Halstead Metrics: Expected Length")

            ns, n_hats = process.get_function_length_pairs(result)
            plot_scatters(ns, n_hats, ax, name, color=colors[k % len(colors)])
            plot_lines(ns, n_hats, ax, name, color=colors[k % len(colors)])
            ax.legend()
