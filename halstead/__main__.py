from .process import get_dir_halstead
from .output import plot_function_length_pairs


def parse_args():
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    import argparse
    import giturlparse
    import git

    parser = argparse.ArgumentParser(prog="halstead", description="Analyze the Halstead complexity metrics of a git repository.")
    parser.add_argument("repo", type=str, help="Valid path to git repo or user/project shorthand for GitHub repo")
    parser.add_argument("clone_path", type=str, nargs="?", help="Valid path to git repo or user/project shorthand for GitHub repo")

    args = parser.parse_args()

    git_url = giturlparse.parse(args.repo)

    if not git_url.valid:
        raise ValueError("invalid git url")

    if args.clone_path:
        clone_path = args.clone_path
    else:
        clone_path = git_url.repo

    try:
        repo = git.Repo.clone_from(git_url.urls["https"], clone_path)
    except git.exc.GitCommandError as e:
        if e.status == 128:
            raise IOError("clone path `{}` is non-empty".format(clone_path))

        raise e

    return clone_path


def main():
    clone_path = parse_args()
    results = get_dir_halstead(clone_path)
    plot_function_length_pairs(results)


if __name__ == "__main__":
    main()
