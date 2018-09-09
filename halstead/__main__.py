from .process import get_dir_halstead
from .output import plot_function_length_pairs
DESCRIPTION = "Analyze the Halstead complexity metrics of a git repository."
REPO_HELP = "Valid path to git repo or user/project shorthand for GitHub repo."
CLONE_PATH_HELP = "Directory for cloned repo."


def parse_args():
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    import argparse
    import giturlparse
    import git

    parser = argparse.ArgumentParser(prog="halstead", description=DESCRIPTION)
    parser.add_argument("repo", type=str, help=REPO_HELP)
    parser.add_argument("clone_path", type=str, metavar="clone-path",
                        nargs="?", help=CLONE_PATH_HELP)

    args = parser.parse_args()

    git_url = giturlparse.parse(args.repo)

    if not git_url.valid:
        raise ValueError("invalid git url")

    if args.clone_path:
        clone_path = args.clone_path
    else:
        clone_path = git_url.repo

    pull_repo(git_url, clone_path)

    return clone_path


def main():
    clone_path = parse_args()

    from .process import get_dir_halstead
    from .output import plot_function_length_pairs

    results = get_dir_halstead(clone_path)
    plot_function_length_pairs(results)


if __name__ == "__main__":
    main()
