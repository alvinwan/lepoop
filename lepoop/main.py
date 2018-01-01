"""Entry points manager for command line utility."""

from lepoop.candidates import get_uninstall_candidates
from subprocess import Popen


def main():
    #TODO: configure bashrc for history (and maybe alias)
    list_of_candidates = get_uninstall_candidates()
    candidates = ' '.join(list_of_candidates)
    proposed_command = 'pip uninstall %s' % candidates
    input('%s [enter/ctrl+c]' % proposed_command)
    event = Popen(proposed_command.split())
    _, error = event.communicate()
