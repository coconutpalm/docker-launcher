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


def test_security_groups():
    run_playbook_test("tests/stack-confs/security-groups.yml",
                      "tests/target-playbooks/security-groups-playbook.yml",
                      [0, 1])


def test_name_is_required():
    run_schema_error_test({
        'security_groups': [{
            'description': 'A generated security group'
        }]
    })


def test_rules_are_not_required():
    run_playbook_test("tests/stack-confs/security-group-short.yml",
                      "tests/target-playbooks/security-group-short-playbook.yml",
                      [0])
