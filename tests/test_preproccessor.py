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


from test_library import run_playbook_test


def test_generated_cassandra_playbook():
    run_playbook_test("tests/stack-confs/cassandra-stack-conf.yml",
                      "tests/target-playbooks/cassandra-playbook.yml")


def test_generated_auth_plus_playbook():
    run_playbook_test("tests/stack-confs/auth-plus-stack-conf.yml",
                      "tests/target-playbooks/auth-plus-playbook.yml")


def test_generated_auth_plus_linking_playbook():
    run_playbook_test("tests/stack-confs/auth-plus-linking-stack-conf.yml",
                      "tests/target-playbooks/auth-plus-linking-playbook.yml")


def test_generated_ec2_playbook():
    run_playbook_test("tests/stack-confs/ec2-test.yml",
                      "tests/target-playbooks/ec2-test.yml")
