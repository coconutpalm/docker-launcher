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
A module to encapsulate the stack configuration into a class
"""

import os
from launcher.util.stack_service import StackService
from launcher.util.stack_security_group import StackSecurityGroup
from launcher.util.stack_node import StackNode
from launcher.util.stack_test import StackTest
from launcher.util.dict_wrapper import DictWrapper
from jinja2 import Template
from StringIO import StringIO
SCHEMA = os.path.join(os.path.dirname(__file__), 'schema/stack_conf.yml')


def apply_template(stack, conf):
    """Apply the vars in conf to the according template sections in stack.

    :stack: The stack to expand as a open file
    :conf: The parsed configuration, to apply to the stack
    :returns: A stack as an open file with all template strings expanded"""
    if conf == "":
        return stack
    if not conf.has('vars'):
        return stack

    template = Template(stack.read())
    new_stack = template.render(**conf.get('vars'))
    return StringIO(new_stack)


class StackConf(DictWrapper):
    """ Class to encapsulate a stack """

    def __init__(self, stack, conf=""):
        # apply template
        stack = apply_template(stack, conf)

        with open(SCHEMA) as stack_schema:
            DictWrapper.__init__(self, stack, stack_schema)

        self.set('services', self.parse_services())
        self.set('nodes', self.parse_nodes())
        self.set('security_groups',
                 self.parse_list('security_groups', StackSecurityGroup))
        self.set('tests', self.parse_list('tests', StackTest))

    def parse_list(self, name, cls):
        """Safely parses the name into the given cls objects.

        :returns: a list of cls objects
        """
        if self.has(name):
            objects = []
            for item in self.get(name):
                objects.append(cls(item))
            return objects
        else:
            return None

    def parse_nodes(self):
        """Safely parses the given nodes into StackNode objects.

        :nodes: The nodes to parse as a list of maps
        :returns: a list of StackNode objects
        """
        if self.has('nodes'):
            parsed_nodes = []
            for node in self.get('nodes'):
                parsed_nodes.append(StackNode(node))
            return parsed_nodes
        else:
            return None

    def parse_services(self):
        """Parses the given services into StackService objects.

        :services: The services to parse as a list of maps
        :returns: a list of StackService objects
        """
        parsed_services = []
        for service in self.get('services'):
            parsed_services.append(StackService(service,
                                                self.has('nodes')))

        return parsed_services
