# encoding: utf-8

#
# Copyright © 2015 ATS Advanced Telematic Systems GmbH
#
# This file is part of Docker Launcher.
#
# Docker Launcher is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Docker Launcher is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Docker Launcher. If not, see <http://www.gnu.org/licenses/>.
#

"""
Module for generic Ansible functions
"""
from __future__ import print_function

import os
import sys
import re
from jinja2 import Environment, PackageLoader
from subprocess import Popen, PIPE
import launcher.ansible.variables as ansible_vars
ANSIBLE_REGEX = re.compile(r'^(PLAY \[|msg:|fatal:|FATAL)')
ANSIBLE_CHARS = '* \t\n'


def apply_template(template, **kwargs):
    """Return a applied template.

    :template: The template file to load
    :**kwargs: The arguments to the template
    """
    env = Environment(loader=PackageLoader('launcher.ansible', 'templates'))
    template = env.get_template(template)
    return template.render(kwargs)


def spawn(command, verbosity,
          output_regex=ANSIBLE_REGEX,
          stripped_chars=ANSIBLE_CHARS):
    """Runs a command with STDOUT and STDERR attached.

    :command: The command to run as a list.
    :verbosity: how to mangle the output
    :output_regex: when verbosity < 1, only lines matching this regex get
                   printed
    :stripped_chars: string of characters, that will be rstripped
    :return: The exit code of command
    """
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    for line in iter(process.stdout.readline, b''):
        if verbosity > 0:
            print(line.rstrip())
        elif output_regex.match(line):
            print(line.rstrip(stripped_chars))
    for line in iter(process.stderr.readline, b''):
        sys.stderr.write(line.rstrip())

    return process.wait()


def exec_playbook(inventory, playbook, verbosity):
    """Execute ansible-playbook on playbook with inventory as inventory file

    :inventory: The inventory to use
    :playbook: The playbook to run
    """
    with open(ansible_vars.PLAYBOOK_LOCATION, 'w') as tmp_playbook:
        tmp_playbook.write(playbook)

    with open(ansible_vars.INVENTORY_LOCATION, 'w') as tmp_inventory:
        tmp_inventory.write(inventory)

    if verbosity > 1:
        ansible_return = spawn(ansible_vars.ANSIBLE_VERBOSE_CLI,
                               verbosity)
    else:
        ansible_return = spawn(ansible_vars.ANSIBLE_CLI, verbosity)

    if ansible_return == 0:
        os.remove(ansible_vars.PLAYBOOK_LOCATION)
        os.remove(ansible_vars.INVENTORY_LOCATION)

    return ansible_return
