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
A module to encapsulate services
"""

import re
from launcher.util.dict_wrapper import DictWrapper


class StackService(DictWrapper):
    """ Class to encapsulate a service """

    def __init__(self, service, is_remote=True):
        DictWrapper.__init__(self, service)

        self.set_host(is_remote)
        self.set_ports()
        self.set_exposed_ports()
        self.set_advertised_ports()

    def set_host(self, is_remote):
        """Set the correct host specifier, either 'local' or 'service-name'."""
        if is_remote:
            self.set('host', self.get('name'))
        else:
            self.set('host', 'local')

    def set_ports(self):
        """Transforms ports into the public:private mapping, for docker."""
        if self.has('ports'):
            new_ports = []

            for port in self.get('ports'):
                if isinstance(port, int):
                    new_ports.append('{port}:{port}'.format(port=port))
                else:
                    new_ports.append(port)

            self.set('ports', new_ports)

    def set_exposed_ports(self):
        """Expose all ports"""
        if self.has('ports'):
            exposed_ports = get_docker_ports(self.get('ports'))
            if self.has('expose'):
                exposed_ports += self.get('expose')
            self.set('expose', exposed_ports)

    def set_advertised_ports(self):
        """Advertise first port if none are give in stack config."""
        if self.has('ports') and not self.has('advertised_port'):
            self.set('advertised_port',
                     int(self.get('ports')[0].split(':')[0]))


def get_docker_ports(ports):
    """Retrieve the container side ports from a docker --publish declaration.

    :ports: A list of docker --publish declarations
    :returns: A list of ports
    """
    ports_re = re.compile(r':(\d*)')
    exposed = []

    for port in ports:
        matched = ports_re.search(port)
        exposed.append(matched.group(1))

    return exposed
