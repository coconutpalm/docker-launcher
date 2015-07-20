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

"""Provides functions for linking docker containers with different methods"""

from launcher.util.find_by import find_by_attr
import copy


def link_services(services, target="local"):
    """Inplace update the services' links/env values

    :services: array of Service objects
    :target: target to run playbook against, 'local', 'ec2'
    :returns: List of services
    """
    linked_services = copy.deepcopy(services)
    for service in linked_services:
        if target != "local" and service.get('links') is not None:
            new_env = link_via_haproxy(service, services)
            service.set('links', None)
            if service.get('env') is not None:
                service.update('env', new_env)
            else:
                service.set('env', new_env)
    return linked_services


def link_via_haproxy(service, services):
    """ creates a dict of env vars for haproxy linking

    :service: a Service object
    :service: array of Service objects
    :returns: Dict
    """
    new_env = {}
    for link in service.get('links'):
        parsed_link_name = link.split("[direct]")

        direct = True if len(parsed_link_name) > 1 else False
        link_name = parsed_link_name[0]
        linked_service = find_by_attr(services, 'name', link_name)
        linked_port = linked_service.get('advertised_port')

        new_env.update(generate_env_vars(link_name, linked_port, direct))

    return new_env


def generate_env_vars(link, port, direct):
    """ creates a dict of env vars to link to a service

    :link: name of the linked service
    :port: port of the linked service
    :direct: True links directly to the service, False links via haproxy
    :returns: Dict
    """
    group_host = "{{{{ groups.{name}[0] }}}}"
    name = link if direct is True else "haproxy"

    return {
        "{link}_PORT".format(link=link.upper()): port,
        "{link}_HOST".format(link=link.upper()):
            group_host.format(name=name),
        "{link}_PORT_{port}_TCP_ADDR".format(link=link.upper(), port=port):
            group_host.format(name=name)
    }
