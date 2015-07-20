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


from launcher.util.stack_config import StackConf, apply_template
from launcher.util.configuration import LauncherConf
from launcher.ansible.executor import generate as playbook_generate
from StringIO import StringIO
import pytest
import yaml

CONF = """
reboot_strategy: 'off'
registry:
  user: atsjenkins
  email: jenkins@advancedtelematic.com
ec2:
  key: tauron
  image: ami-07fd8270
  region: eu-west-1
vars:
  name: something
  org: someone
"""

STACK = """
services:
  name: {{ name }}
  repo: {{ org }}/{{ name }}
"""

EXPECTED_STACK = """
services:
  name: something
  repo: someone/something"""

def test_apply_template():
    conf = LauncherConf(StringIO(CONF))
    stack = StringIO(STACK)

    assert apply_template(stack, conf).read() == EXPECTED_STACK
