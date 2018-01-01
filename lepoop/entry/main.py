"""Entry points manager for command line utility."""

from ..candidates import get_uninstall_candidates
from ..utils import colored
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
        list_of_candidates = get_uninstall_candidates()
        candidates = ' '.join(list_of_candidates)
        proposed_command = 'pip uninstall {}'.format(candidates)
        input(colored('`{}` [enter/ctrl+c]'.format(proposed_command)))
        event = Popen(proposed_command.split())
        _, error = event.communicate()
    except AssertionError as e:
        print(Fore.RED + str(e))
    except KeyboardInterrupt:
        print()
