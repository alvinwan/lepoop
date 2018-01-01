import os
import datetime
import pip
import platform
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from collections import defaultdict
import re


def get_package_groups():
    """Get groups of packages installed at the same time.

    The list is ordered in reverse order, across time as (time, packages). Here,
    time is formatted as datetime objects.
    """
    mapping = defaultdict(lambda: [])
    for package_name_version, mod_time in get_packages_creation_times():
        mapping[mod_time].append(package_name_version)

    result = []
    for mod_time in sorted(mapping, reverse=True):
        pretty_mod_time = datetime.datetime.fromtimestamp(mod_time)
        result.append((pretty_mod_time, mapping[mod_time]))
    return result


def get_packages_creation_times():
    """Get all pip packages and their timestamps.

    Original function taken from StackOverflow:
    https://stackoverflow.com/a/44436961/4855984
    """
    packages = []
    for package in pip.get_installed_distributions():
        package_name_version = str(package)
        package_location = _get_module_dir(package)
        creation_time = creation_date(package_location)
        packages.append([
            package_name_version,
            creation_time,
        ])
    return packages


def get_bash_history():
    """Get bash history."""
    shell_command = 'bash -i -c "history -r; history"'
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    output, error = event.communicate()
    regex = r" +\d+ +(.*?)\\n"
    commands = [match.groups() for match in re.finditer(regex, str(output))]
    return commands


def _get_module_dir(package):
    """Get module directory from the module information.

    Original function taken from StackOverflow:
    https://stackoverflow.com/a/44436961/4855984
    """
    try:
        module_dir = next(package._get_metadata('top_level.txt'))
        package_location = os.path.join(package.location, module_dir)
        os.stat(package_location)
    except (StopIteration, OSError):
        pass
    package_location = os.path.join(package.location, package.key)
    if os.path.isdir(package_location):
        return package_location
    return package.location


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime