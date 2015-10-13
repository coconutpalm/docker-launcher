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


from test_library import run_playbook_test, run_schema_error_test
from launcher.util.stack_config import StackConf
from launcher.util.dict_wrapper import SchemaError
import pytest

def test_minimal_stack_conf():
    """Test that the minimal stack conf is valid"""
    run_playbook_test("tests/stack-confs/volumes_from.yml",
                      "tests/target-playbooks/volumes_from.yml")
