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


from launcher.util.cli_args import *
from launcher.util.configuration import LauncherConf
from launcher.util.stack_config import StackConf
import pytest
import argparse
CONFIG_TEST_CLI = ['-c',
                   'tests/test-config-full.yml',
                   'tests/stack-confs/minimal.yml']


@pytest.fixture(scope="function")
def parser():
    return argparse.ArgumentParser()


def test_get_args():
    args = get_args([
        '-c',
        'tests/test-config.yml',
        'tests/stack-confs/security-group-short.yml'
    ])
    assert isinstance(vars(args)["stack"], StackConf) is True


def test_verbose_arg(parser):
    add_verbose_arg(parser)
    args = parser.parse_args(['-v'])
    assert vars(args)["verbose"] == 1


def test_config_arg(parser):
    add_config_arg(parser)
    args = parser.parse_args(['-c', 'tests/test-config.yml'])
    assert isinstance(vars(args)["config"], LauncherConf) is True


def test_config_verbosity(parser):
    args = get_args(CONFIG_TEST_CLI)
    assert args.verbose == 1


def test_config_verbosity_override(parser):
    args = get_args(['-vvv'] + CONFIG_TEST_CLI)
    assert args.verbose == 3


def test_config_python(parser):
    args = get_args(CONFIG_TEST_CLI)
    assert args.python == 'python2'


def test_config_python_override(parser):
    args = get_args(['--python=python'] + CONFIG_TEST_CLI)
    assert args.python == 'python'


def test_default_config(tmpdir, parser):
    temp = tmpdir.mkdir('configuration')
    configfile = '{dir}/non-existant.yml'.format(dir=temp)

    # create default config
    try:
        add_config_arg(parser)
        parser.parse_args(['-c', configfile])
    except SystemExit as error:
        assert error.code == 2


def test_missing_stack(parser):
    add_stack_arg(parser)
    try:
        parser.parse_args(['non-existant-conf.yml'])
    except SystemExit as error:
        assert error.code == 2


def test_python_arg(parser):
    add_python_arg(parser)
    args = parser.parse_args(['--python', 'python3'])
    assert vars(args)["python"] == 'python3'


def test_version_arg(parser):
    add_version_arg(parser)
    try:
        args = parser.parse_args(['--version'])
    except SystemExit as e:
        assert e.code == 0
