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
SAVE_HELP = "Save all plots."


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


def handle_urls(urls):
    """TODO: Docstring for handle_url.

    :git_url: TODO
    :returns: TODO

    """
    import giturlparse
    import re

    git_urls = []

    github_regex = re.compile("[^/]*/[^/]*")

    for url in urls:
        git_url = giturlparse.parse(url)
        if git_url.valid:
            git_urls.append(git_url)
            continue

        # The git URL is invalid.
        # Is it in the GitHub shorthand form 'owner/repo'?
        if not github_regex.match(url):
            # Nope.
            print("Ign: Invalid git url '{}'".format(url) +
                  ", also not in GitHub shortform 'owner/repo'")
            continue

        # Yes, so let's manually build the url.
        new_url = "https://github.com/" + url
        git_url = giturlparse.parse(new_url)

        if git_url.valid:
            git_urls.append(git_url)
            continue

        # Well, we tried.
        print("Ign: Could not git url '{}'".format(url) +
              " (it looks like GitHub shortform, but isn't valid)")

    return git_urls


def parse_args():
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    import argparse

    parser = argparse.ArgumentParser(prog="halstead", description=DESCRIPTION)
    parser.add_argument("repos", type=str, nargs="+", help=REPO_HELP)
    parser.add_argument("-j", "--join", dest="join", action="store_const",
                            const=True, default=False, help=JOIN_HELP)
    parser.add_argument("-s", "--save", dest="save", action="store_const",
                            const=True, default=False, help=SAVE_HELP)

    args = parser.parse_args()

    git_urls = handle_urls(args.repos)

    if not git_urls:
        exit("Exit: No valid git urls found")

    return (git_urls, args)


def main():
    git_urls, args = parse_args()

    from .process import get_dir_halstead
    from .output import plot_function_length_pairs
    import matplotlib.pyplot as plt

    # Clone the repos.
    for git_url in git_urls:
        pull_repo(git_url, git_url.repo)

    repo_results = [(url.repo, get_dir_halstead(url.repo)) for url in git_urls]

    plt.style.use("ggplot")
    plot_function_length_pairs(repo_results, args.join, args.save)

    plt.show()


if __name__ == "__main__":
    main()
