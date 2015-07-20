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


import os
import string
import random
import launcher.util.password as pw
from launcher.util.configuration import LauncherConf


def random_pass(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test_export_password():
    """
    Test, that the password gets read by getpass, when it can't be found in the
    environment
    """
    try:
        del os.environ['DOCKER_PASSWORD']
    except:
        pass

    password = random_pass()

    pw.getpass.getpass = lambda _: password

    with open('tests/test-config.yml') as conf_file:
        conf = LauncherConf(conf_file)
    pw.export_password(conf)

    assert os.environ['DOCKER_PASSWORD'] == password


def test_exported_password():
    """
    Test, that the password will be left untouched, if it is already exported
    """
    password = random_pass()

    os.environ['DOCKER_PASSWORD'] = password

    pw.getpass.getpass = lambda _: 'not so random'

    with open('tests/test-config.yml') as conf_file:
        conf = LauncherConf(conf_file)
    pw.export_password(conf)

    assert os.environ['DOCKER_PASSWORD'] == password
    assert os.environ['DOCKER_PASSWORD'] != 'not so random'
