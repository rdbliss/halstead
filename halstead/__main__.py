from git import Repo
from git.exc import GitCommandError
from .process import get_dir_halstead
from .output import plot_function_length_pairs
import giturlparse
import argparse
import matplotlib.pyplot as plt


def parse_args():
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    parser = argparse.ArgumentParser(prog="halstead", description="Analyze the Halstead complexity metrics of a git repository.")
    parser.add_argument("repo", type=str, help="Valid path to git repo or user/project shorthand for GitHub repo")
    parser.add_argument("clone_path", type=str, nargs="?", help="Valid path to git repo or user/project shorthand for GitHub repo")

    return parser.parse_args()


def main():
    args = parse_args()
    git_url = giturlparse.parse(args.repo)

    if not git_url.valid:
        raise ValueError("invalid git url")

    if args.clone_path:
        clone_path = args.clone_path
    else:
        clone_path = git_url.repo

    try:
        repo = Repo.clone_from(git_url.urls["https"], clone_path)
    except GitCommandError as e:
        if e.status == 128:
            raise IOError("clone path `{}` is non-empty".format(clone_path))

        raise e

    results = get_dir_halstead(clone_path)

    plt.style.use("ggplot")
    plot_function_length_pairs(results)

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
