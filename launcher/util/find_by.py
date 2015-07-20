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
Module for helper functions finding values in lists of DictWrapper objects.
"""


def find_by_attr(array, attr, value):
    """Find values for specific keys in a list of DictWrapper objects.

    :array: The list of DictWrapper objects
    :attr: The key to search in
    :value: The value to search for
    :return: The list items containing value in attr
    """
    return (item for item in array if item.get(attr) == value).next()
