"""Entry points manager for command line utility."""

from thepoop.utils import get_package_groups


def main():
    time, packages = get_package_groups()[1]  # in develop mode
    print('Uninstalling %s, installed at %s' % (' '.join(packages), time))