DESCRIPTION = "Analyze the Halstead complexity metrics of a git repository."
REPO_HELP = "Valid path to git repo or user/project shorthand for GitHub repo."
CLONE_PATH_HELP = "Directory for cloned repo."


def pull_repo(git_url, clone_path):
    import git
    try:
        repo = git.Repo.clone_from(git_url.urls["https"], clone_path)
    except git.exc.GitCommandError as e:
        if e.status != 128:
            raise e

        # The directory already exists.
        # Is it a git repository?
        try:
            repo = git.Repo(clone_path)
        except git.InvalidGitRepositoryError:
            raise IOError("clone-path `{}`".format(clone_path) +
                       " is non-empty and not a git repository")

        # Is the repo tracking the same thing that we are?
        for remote in repo.remotes:
            for url in git_url.urls.values():
                if url in remote.urls:
                    # Yes, so pull it.
                    remote.pull()
                    return

        raise IOError("clone-path `{}`".format(clone_path) +
                      "is a git repository distinct from the given url")


def parse_args():
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    import argparse
    import giturlparse

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
