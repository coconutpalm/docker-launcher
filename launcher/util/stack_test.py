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
A module to encapsulate stack test definitions
"""

from launcher.util.dict_wrapper import DictWrapper


class StackTest(DictWrapper):
    """ Class to encapsulate one test definition """

    def __init__(self, test):
        DictWrapper.__init__(self, test)

        if self.has('docker'):
            self.set('docker', StackTestDocker(self.get('docker')))

        if self.has('shell'):
            self.set('shell', StackTestShell(self.get('shell')))


class StackTestDocker(DictWrapper):
    """ Class to encapsulate a docker test """

    def __init__(self, docker):
        DictWrapper.__init__(self, docker)


class StackTestShell(DictWrapper):
    """ Class to encapsulate a shell test """

    def __init__(self, shell):
        DictWrapper.__init__(self, shell)
