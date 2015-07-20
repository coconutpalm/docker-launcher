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


from launcher.ansible.executor import generate
from launcher.util.configuration import LauncherConf
from launcher.util.stack_config import StackConf
from test_library import run_playbook_test
import yaml

with open("tests/test-config.yml") as launcher_conf:
    config = LauncherConf(launcher_conf)


def test_generated_migration_playbook():
    run_playbook_test("tests/stack-confs/migrations-test-stack-conf.yml",
                      "tests/target-playbooks/migrations-test-playbook.yml")


def test_generated_migration_ec2_playbook():
    run_playbook_test("tests/stack-confs/migrations-ec2-stack-conf.yml",
                      "tests/target-playbooks/migrations-ec2-playbook.yml")


def parse_yaml_config(path):
    with open(path) as conf_stream:
        conf = yaml.safe_load(conf_stream)
    return conf
