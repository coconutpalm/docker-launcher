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


from launcher.util.stack_config import StackConf
from launcher.util.configuration import LauncherConf
from launcher.ansible.executor import generate as playbook_generate
import pytest
import yaml
CONFIG = "tests/test-config.yml"


def parse_yaml_config(path):
    """Parse a yaml file"""
    with open(path) as conf_stream:
        conf = yaml.safe_load(conf_stream)
    return conf


def test_scheduler_schema():
    stack = {
        'services': [{
            'name': 'test_service',
            'repo': 'test/repo',
            'schedule': [{
                'onboot': '2min',
                'schedule': '5min',
                'description': 'something'
            }]
        }]
    }
    with open(CONFIG, 'r') as configuration:
        config = LauncherConf(configuration)
        yaml.load(playbook_generate(StackConf(stack), config))
