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
A module to encapsulate the docker launcher configuration into a class
"""

import os
from launcher.util.dict_wrapper import DictWrapper
SCHEMA = os.path.join(os.path.dirname(__file__), 'schema/configuration.yml')


class LauncherConf(DictWrapper):
    """Class to encapsulate configuration for docker-launcher"""

    def __init__(self, config_file):
        with open(SCHEMA) as schema:
            DictWrapper.__init__(self, config_file, schema)
