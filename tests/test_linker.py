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


import launcher.util.linker as linker
import pdb
from launcher.util.find_by import find_by_attr
from launcher.util.configuration import LauncherConf
from launcher.util.stack_config import StackConf

with open("tests/test-config.yml") as launcher_conf:
        config = LauncherConf(launcher_conf)


def test_link_via_env():
    stack_conf_file = "tests/stack-confs/auth-plus-linking-stack-conf.yml"
    with open(stack_conf_file) as stack_conf:
        stack_conf = StackConf(stack_conf)
    linked_services = linker.link_services(stack_conf.get('services'), "ec2")
    expected = {
        "CASSANDRA_PORT": 9042,
        "CASSANDRA_HOST": "{{ groups.haproxy[0] }}",
        "CASSANDRA_PORT_9042_TCP_ADDR": "{{ groups.haproxy[0] }}",
        "REDIS_PORT": 6379,
        "REDIS_HOST": "{{ groups.haproxy[0] }}",
        "REDIS_PORT_6379_TCP_ADDR": "{{ groups.haproxy[0] }}",
        "DEVICE_INFO_PORT": 9002,
        "DEVICE_INFO_HOST": "{{ groups.haproxy[0] }}",
        "DEVICE_INFO_PORT_9002_TCP_ADDR": "{{ groups.haproxy[0] }}"
    }
    auth_plus = find_by_attr(linked_services, 'name', 'auth-plus')
    assert auth_plus.get('env') == expected


def test_link_retains_env_variables():
    with open("tests/stack-confs/direct-linking-stack-conf.yml") as stack_conf:
        stack_conf = StackConf(stack_conf)
    linker.link_services(stack_conf.get('services'), "ec2")
    auth_plus = find_by_attr(stack_conf.get('services'), 'name', 'auth-plus')
    assert auth_plus.get('env')["ENV_VAR_THAT"] == "should_still_be_here"


def test_direct_linking():
    with open("tests/stack-confs/direct-linking-stack-conf.yml") as stack_conf:
        stack_conf = StackConf(stack_conf)
    linked_services = linker.link_services(stack_conf.get('services'), "ec2")
    auth_plus = find_by_attr(linked_services, 'name', 'auth-plus')
    assert auth_plus.get('env')["CASSANDRA_HOST"] == "{{ groups.cassandra[0] }}"
