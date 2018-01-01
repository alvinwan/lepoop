"""Entry points manager for command line utility."""

from ..uninstall import get_uninstall_candidates
from ..reinstall import get_reinstall_candidates
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
        if last_valid_pip_action == 'install':
            list_of_candidates = get_uninstall_candidates()
            candidates = ' '.join(list_of_candidates)
            proposed_command = 'pip uninstall {}'.format(candidates)
        elif last_valid_pip_action == 'uninstall':
            list_of_candidates = get_reinstall_candidates()
            candidates = ' '.join(list_of_candidates)
            proposed_command = 'pip install {}'.format(candidates)
        elif last_valid_pip_action == 'download':
            pass
        input(colored('`{}` [enter/ctrl+c]'.format(proposed_command)))
        event = Popen(proposed_command.split())
        _, error = event.communicate()
    except AssertionError as e:
        print(Fore.RED + str(e))
    except KeyboardInterrupt:
        print()
