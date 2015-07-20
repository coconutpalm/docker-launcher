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


@pytest.fixture(scope="function")
def valid_service():
    return {
        'services': [{
            'name': 'test_service',
            'repo': 'test/repo'
        }]
    }


@pytest.fixture(scope="function")
def valid_security_group():
    return {
        'security_group': [{
            'name': 'test_sec_group',
            'description': 'A description of the group'
        }]
    }


def test_minimal_stack_conf():
    """Test that the minimal stack conf is valid"""
    run_playbook_test("tests/stack-confs/minimal.yml",
                      "tests/target-playbooks/minimal.yml")


def test_services_is_required():
    """Test, that a stack conf without services is invalid"""
    run_schema_error_test({
        'nodes': [{
            'name': 'one',
            'group': 'default',
            'services': ['one'],
            'size': 't2.micro',
            'count': 1,
        }]
    })


def test_name_is_required(valid_service):
    with pytest.raises(SchemaError):
        conf = {
            'security_groups': [{
                'description': 'A generated security group'
            }]}
        StackConf(merge_dicts(conf, valid_service))


def test_name_is_a_str(valid_security_group):
    with pytest.raises(SchemaError):
        conf = {
            'services': [{
                'repo': 'test'
            }]}
        StackConf(merge_dicts(conf, valid_security_group))


def merge_dicts(dict1, dict2):
    return dict(dict1.items() + dict2.items())
