"""
halstead - Analyze the Halstead complexities of Python git repositories.
Copyright © 2018 Robert Dougherty-Bliss

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

DESCRIPTION = "Analyze the Halstead complexity metrics of a git repository."
REPO_HELP = "Valid path to git repo or user/project shorthand for GitHub repo."
CLONE_PATH_HELP = "Directory for cloned repo."
JOIN_HELP = "Merge plots for multiple repositories together."


def pull_repo(git_url, clone_path):
    import git
    print("cloning '{}' into '{}'".format(git_url.url, clone_path))

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

        # Yes; is it tracking the same thing that we are?
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
    parser.add_argument("repos", type=str, nargs="+", help=REPO_HELP)
    parser.add_argument("-j", "--join", dest="join", action="store_const",
                            const=True, default=False, help=JOIN_HELP)

    args = parser.parse_args()

    git_urls = []

    for url in args.repos:
        git_url = giturlparse.parse(url)

        if not git_url.valid:
            print("Ign: Invalid git url '{}'".format(url))
            continue

        git_urls.append(git_url)

    return (git_urls, args.join)


def main():
    git_urls, join = parse_args()

    from .process import get_dir_halstead
    from .output import plot_multiple_repository_function_pairs
    import matplotlib.pyplot as plt

    # Clone the repos.
    for git_url in git_urls:
        pull_repo(git_url, git_url.repo)

    repo_results = [(url.repo, get_dir_halstead(url.repo)) for url in git_urls]

    plt.style.use("ggplot")
    plot_multiple_repository_function_pairs(repo_results, join)

    plt.show()


if __name__ == "__main__":
    main()
