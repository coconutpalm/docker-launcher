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
Class to generate Ansible playbooks
"""

from launcher.util.linker import link_services
from launcher.util.find_by import find_by_attr
from launcher.ansible.util import apply_template
from launcher.util.stack_service import StackService
import copy
import yaml
import os


class Playbook(object):
    """ class to encapsulate a playbook """

    def __init__(self, stack, config):
        self.__stack = stack
        self.__config = config

        self.security_group = self.create_security_group()
        self.nodes = self.create_nodes()
        self.services = self.create_services()
        self.tests = self.create_tests()

        self.ansible_playbook = "\n".join([self.security_group,
                                           self.nodes,
                                           self.services,
                                           self.tests])

    @property
    def config(self):
        """ Immutable config. """
        return self.__config

    @property
    def stack(self):
        """ Immutable stack config. """
        return self.__stack

    @property
    def is_remote(self):
        """ Bool flag describing target of playbook """
        return self.stack.get('nodes') is not None

    def create_security_group(self):
        """ return security group tasks.

        :returns: string
        """
        tasks = ""
        if self.stack.get('security_groups') is None:
            return tasks

        for security_group in self.stack.get('security_groups'):
            tasks += apply_template('security_group.yml',
                                    security_group=security_group,
                                    conf=self.config)
        return tasks

    def create_nodes(self):
        """ return node tasks.

        :returns: string
        """
        nodes = copy.deepcopy(self.stack.get('nodes'))
        node_tasks = ""

        if nodes is None:
            return node_tasks

        if self.stack.get('logging') is True:
            add_logging_to_nodes(nodes)

        node_tasks += apply_template('ec2_header.yml')
        for node in nodes:
            node_tasks += apply_template('node.yml',
                                         node=node,
                                         conf=self.config)
        node_tasks += apply_template('ec2_wait.yml')
        node_tasks += apply_template('ec2_bootstrap.yml')
        node_tasks += apply_template('docker_login.yml', conf=self.config)
        return node_tasks

    def create_services(self):
        """ return service tasks.

        :returns: string
        """
        services = self.stack.get('services')
        if self.stack.get('logging') is True:
            services = add_logging_services(services, self.is_remote)

        target = 'ec2' if self.is_remote else 'local'
        linked_services = link_services(services, target)

        services_tasks = ""

        for service in linked_services:
            if service.get('migrations') is not None:
                services_tasks += self.create_migration(service)
            services_tasks += apply_template('service.yml',
                                             service=service,
                                             conf=self.config)
        return services_tasks

    def create_migration(self, service):
        """ return migration tasks.

        :service: a service object
        :returns: string
        """
        migrations = "\n"
        if service.get('migrations').get('cql', None) is not None:
            files = service.get('migrations')['cql']
            if service.get('links'):
                host = "local"
            else:
                host = find_by_attr(self.stack.data['services'],
                                    'name',
                                    'cassandra').get('host') + '[0]'
            migrations += apply_template('cql_migration.yml',
                                         service=service,
                                         files=files,
                                         host=host)
        return migrations

    def create_tests(self):
        """Apply the tests template and return the generated plays

        :returns: A string with the generated plays for inclusion in a playbook
        """
        tests = self.stack.get('tests')

        if tests is None:
            return ''

        test_play = ''

        for test in tests:
            if self.stack.get('nodes') is None:
                target = 'localhost'
            else:
                target = '{{{{ groups.{}[0] }}}}'.format(test.get('target'))

            test_play += apply_template('tests.yml',
                                        name=test.get('name'),
                                        docker=test.get('docker'),
                                        shell=test.get('shell'),
                                        target=target)

        return test_play


def add_logging_to_nodes(nodes):
    """ adds logging services to nodes

    :nodes: list of nodes
    :returns: None
    """
    logging_master = find_by_attr(nodes,
                                  'logging_master',
                                  True)

    master_logging_services = ['elasticsearch',
                               'logstash',
                               'logspout',
                               'kibana']
    for i in xrange(len(nodes)):
        if nodes[i] == logging_master:
            logging_services = master_logging_services
        else:
            logging_services = ['logspout']

        nodes[i].set('services',
                     prepend(nodes[i].get('services'), logging_services))


def add_logging_services(services, is_remote):
    """ returns services with ELK added

    :services: list of services
    :is_remote: bool representing deploy target
    :returns: None
    """
    relpath = '../util/stack_confs/logging-services.yml'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, relpath)
    with open(file_path, 'r') as logging_stack:
        parsed_services = yaml.safe_load(logging_stack)

    logging_services = []
    for service in parsed_services['services']:
        logging_services.append(StackService(service, is_remote))
    services = prepend(services, logging_services)
    return services


def prepend(items, new_items):
    """ prepends items to a list

    :items: list to append to
    :new_items: items to prepend
    :returns: new list with prepended items
    """
    return new_items + items
