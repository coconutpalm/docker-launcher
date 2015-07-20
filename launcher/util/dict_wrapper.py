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
Module to provide a safer abstraction around dicts created from yaml files
"""

import yaml
# pylint: disable=import-error
# pylint can't import this for some reason
import pyrx


class SchemaError(Exception):
    """Exception to indicate a invalid yaml file"""
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class DictWrapper(object):
    """
    This is the parent class for all yaml encapsulating classes, providing ways
    to safely retrieve data from the parsed yaml.
    """

    def __init__(self, data, schema=None):
        try:
            self.data = yaml.safe_load(data)
        except AttributeError:
            self.data = data

        if schema is not None:
            self.validator = pyrx.Factory({"register_core_types": True})
            if isinstance(schema, dict):
                self.schema = schema
            else:
                self.schema = yaml.safe_load(schema)
            valid = self.validate()
            if not valid:
                # pylint: disable=no-member
                # it's a maybe bool, not a bool
                raise SchemaError("Could not parse " +
                                  self.__class__.__name__ +
                                  "\n" +
                                  valid.message)

    def validate(self):
        """Validates the provided data against the schema

        :returns: True if validation succeeded, Result object on failure
        """
        if self.schema is None:
            return True

        schema = self.validator.make_schema(self.schema)
        return schema.check(self.data)

    def get(self, key, default=None):
        """Safely retrieves a key out of the data dict

        :key: the key to retrieve
        :default: the value to return on key errors (defaults to None)
        :returns: the value of the key or default
        """
        try:
            return self.data[key]
        except KeyError:
            return default

    def has(self, key):
        """Checks whether a key exists in the data dict

        :key: the key to check
        :returns: true, if the value exists, false otherwise
        """
        # key can exist but be None
        try:
            if self.data[key]:
                return True
        except KeyError:
            pass

        return False

    def set(self, key, value):
        """Sets the value of a key

        :key: the key to update
        :value: the value to set on key
        """
        self.data[key] = value

    def update(self, key, data):
        """Updates a dict with the provided data.

        :key: the key to update
        :data: the dict to append
        """
        self.data[key].update(data)
