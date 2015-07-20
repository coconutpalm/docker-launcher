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
Module to deploy Ansible playbooks
"""

from launcher.ansible.playbook import Playbook
import launcher.ansible.variables as ansible_vars
from launcher.ansible.util import apply_template, spawn, exec_playbook


def generate(stack, conf):
    """Generate a Ansible playbook from the stack config file.

    :stack: stack configuration
    :conf: configuration variables from config file
    :returns: a Ansible playbook
    """
    playbook = Playbook(stack, conf)

    return playbook.ansible_playbook


def run(conf, stack, verbosity=0, python=None):
    """Generate all needed files, run them and remove them again

    :conf: the launcher configuration to use
    :stack: the stack conf to use
    :verbosity: control the amount of output
    :python: the python executable to use locally
    """
    inventory = apply_template('inventory', python=python)
    playbook = generate(stack, conf)

    spawn(ansible_vars.GALAXY_INSTALL, verbosity)
    ansible_return = exec_playbook(inventory, playbook, verbosity)

    if ansible_return == 0:
        spawn(ansible_vars.GALAXY_REMOVE, verbosity)
        spawn(["rmdir", "roles"], 0)

    return ansible_return
