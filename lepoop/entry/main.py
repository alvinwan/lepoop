"""Entry points manager for command line utility."""

from ..install import get_uninstall_candidates
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
    args = args.parse_args()

    if args.alias:
        print(poop_alias)
        return

    try:
        last_valid_pip_command = get_valid_pip_history()[0]
        last_valid_pip_action = last_valid_pip_command.split()[1]
        command = ''
        if last_valid_pip_action == 'install':
            command = 'pip uninstall -y {}'.format(get_uninstall_candidates())
        elif last_valid_pip_action == 'uninstall':
            command = 'pip install {}'.format(get_reinstall_candidates())
        elif last_valid_pip_action == 'download':
            command = 'rm {}'.format(get_file_candidates())
        assert command, 'Already pooped.'
        input(colored('`{}` [enter/ctrl+c]'.format(command)))
        event = Popen(command.split())
        _, error = event.communicate()
    except AssertionError as e:
        print(Fore.RED + str(e))
    except KeyboardInterrupt:
        print()
