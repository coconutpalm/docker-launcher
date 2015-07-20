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
A module to encapsulate nodes
"""

from jinja2 import Environment, PackageLoader
from launcher.util.dict_wrapper import DictWrapper


class StackNode(DictWrapper):
    """ Class to encapsulate a node """

    def __init__(self, node):
        DictWrapper.__init__(self, node)

    def get_aws_cloud_config(self, conf=None):
        """Generate a AWS cloud config for this node.

        :returns: the cloud config
        """
        env = Environment(loader=PackageLoader('launcher.util',
                                               'templates'))
        template = env.get_template('aws_cloud_config.yml')
        # pylint: disable=no-member
        # this is a template not a str
        return template.render(conf=conf, node=self)
