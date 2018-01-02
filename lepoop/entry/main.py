"""Entry points manager for command line utility."""

from ..install import get_uninstall_candidates
from ..install import get_uninstall_dependencies_for
from ..install import get_installed_package_keys
from ..uninstall import get_reinstall_candidates
from ..download import get_file_candidates
from ..utils import colored
from ..utils import get_valid_pip_history
from .alias import poop_alias
from colorama import Fore
from subprocess import Popen
import argparse


def main():
    args = argparse.ArgumentParser('Le Poop')
    args.add_argument('-a', '--alias', action='store_true',
                      help='Alias to `poop`')
    args.add_argument('package', nargs='*', help='packages to uninstall')
    args = args.parse_args()

    if args.alias:
        print(poop_alias)
        return

    try:
        if args.package:
            command = create_command_using_packages(args.package)
        else:
            command = create_command_using_pip_action()
        input(colored('`{}` [enter/ctrl+c]'.format(command)))
        event = Popen(command.split())
        _, error = event.communicate()
    except AssertionError as e:
        print(Fore.RED + 'Already pooped. (%s)' % str(e))
    except KeyboardInterrupt:
        print()


def create_command_using_pip_action():
    """Create commands using latest pip action."""
    last_valid_pip_command = get_valid_pip_history()[0]
    last_valid_pip_action = last_valid_pip_command.split()[1]
    command = ''
    if last_valid_pip_action == 'install':
        command = 'pip uninstall -y {}'.format(get_uninstall_candidates())
    elif last_valid_pip_action == 'uninstall':
        command = 'pip install {}'.format(get_reinstall_candidates())
    elif last_valid_pip_action == 'download':
        command = 'rm {}'.format(get_file_candidates())
    assert command, 'Already pooped. (No undoable pip commands.)'
    return command


def create_command_using_packages(packages):
    """Create comands using a list of packages."""
    all_packages = set(get_installed_package_keys())
    not_installed = [p for p in packages if p not in all_packages]
    installed = [p for p in packages if p in all_packages]
    assert installed, ('None of these packages are installed: %s' %
                       ', '.join(not_installed))
    packages = get_uninstall_dependencies_for(installed)
    if not_installed:
        print(colored('Packages `%s` are not installed. I\'m ignoring '
                      'them.' % ', '.join(not_installed)))
    return 'pip uninstall {}'.format(packages)