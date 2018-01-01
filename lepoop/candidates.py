"""Candidates for pip uninstallation utilities."""

from lepoop.utils import get_pip_history
from lepoop.utils import get_package_groups
from pipdeptree import build_dist_index
from pipdeptree import construct_tree
from pipdeptree import reverse_tree
from pipdeptree import find_tree_root
import pip
from itertools import chain


def get_most_recent_packages_by_creation_time():
    """Get most recent packages as determined by module source create time."""
    package_groups = get_package_groups()
    time, packages = package_groups[0]
    packages = [pkg.split()[0] for pkg in packages]
    return set(packages)


def get_most_recent_packages_by_pip_history():
    """Get most recent packages as determined by pip history."""
    pip_history = get_pip_history()
    # TODO: add support for command in chain of commands e.g., <cmd>;pip ...
    pip_install_history = [command for command in pip_history
                           if command.strip().split()[1] == 'install']
    packages = pip_install_history[0].split()[2:]
    return set(packages)


flatten = chain.from_iterable


def get_uninstall_candidates():
    """Find candidates for uninstallation.

    1. Find recent modules by creation time and history. Merge the two.
    2. Find all dependencies for these packages.
    3. Determine which dependencies:
       a. are not needed by any other package and
       b. have a "recent" creation date.
    """

    # Find packages that were recently installed.
    packages_by_module = get_most_recent_packages_by_creation_time()
    packages_by_history = get_most_recent_packages_by_pip_history()
    if not packages_by_module & packages_by_history:
        pass  # TODO: disjoint sets, prompt user for which one to use
        package_keys = packages_by_module.union(packages_by_history)
    else:
        package_keys = packages_by_history

    # 2. Find all dependencies of these packages.
    all_packages = pip.get_installed_distributions()
    dist_index = build_dist_index(all_packages)
    packages = set(dist_index[package_key] for package_key in package_keys)
    dependencies = flatten([package.requires() for package in packages])

    # 3. Determine unneeded dependencies that were installed at roughly the
    #    same time.
    candidates = []
    rtree = reverse_tree(construct_tree(dist_index))
    for dep in dependencies:
        node = find_tree_root(rtree, dep.key)
        leftover = {d.key for d in rtree[node] if d.key not in package_keys}
        if not leftover:
            candidates.append(dep.key)
    return candidates