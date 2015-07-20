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

"""Module to build up the cli interface"""

import sys
import argparse
import yaml
from launcher import VERSION
from launcher import CONFIGURATION
from launcher.util.configuration import LauncherConf
from launcher.util.stack_config import StackConf


def get_args(args=None):
    """Parses the CLI arguments with ArgumentParser
    :returns: the parsed arguments
    """
    parser = argparse.ArgumentParser()

    add_stack_arg(parser)
    add_config_arg(parser)
    add_verbose_arg(parser)
    add_python_arg(parser)
    add_version_arg(parser)
    add_teardown_arg(parser)
    add_jenkins_arg(parser)

    args = parser.parse_args(args)
    args = expand_stack(args)

    return apply_conf(args)


def add_verbose_arg(parser):
    """Defines the 'verbose' flag and adds it to the parser"""
    parser.add_argument('-v', '--verbose',
                        action='count',
                        help='Level of verbosity (specify multiple times)')


def add_config_arg(parser):
    """Defines the 'config' flag and adds it to the parser"""
    parser.add_argument('-c', '--config',
                        type=config_file,
                        dest='config',
                        default=CONFIGURATION + '/default.yml',
                        help='The launcher configuration to use')


def add_stack_arg(parser):
    """Defines the default argument and adds it to the parser"""
    parser.add_argument('stack',
                        metavar='STACK',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='The stack configuration to use')


def add_python_arg(parser):
    """Defines the 'python' flag and adds it to the parser"""
    parser.add_argument('--python',
                        metavar='EXEC',
                        dest='python',
                        default=None,
                        help=('The local python version to use '
                              '(defaults to python)'))


def add_version_arg(parser):
    """Defines the 'version' flag and adds it to the parser"""
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=VERSION))


def add_teardown_arg(parser):
    """Defines the 'teardown' flag and adds it to the parser"""
    parser.add_argument('--teardown',
                        action='store_true',
                        default=False,
                        help='Stop and teardown the STACK')


def add_jenkins_arg(parser):
    """Defines the 'jenkins' flag and adds it to the parser"""
    parser.add_argument('--jenkins',
                        metavar='NUM',
                        type=int,
                        default=0,
                        help=('Deploy the STACK, run the test suite '
                              'and tear it down again. Try NUM times to '
                              'deploy before failing.'))


def config_file(arg):
    """Opens the file on path arg, or creates a new configuration file

    :arg: a path
    :returns: a LauncherConf object
    """
    default_conf = yaml.dump({'reboot_strategy': 'off',
                              'registry': {'user': 'someone',
                                           'email': 'someone@somewhere'},
                              'ec2': {'key': 'ssh-key',
                                      'image': 'ami-07fd8270',
                                      'region': 'eu-west-1'}})

    try:
        with open(arg, 'r') as configuration:
            return LauncherConf(configuration)
    except IOError:
        msg = ('Could not read configuration file\n'
               'Please write your configuration to {conf}\n'
               'Example configuration:\n'
               '---\n'
               '{default}').format(conf=arg, default=default_conf)
        raise argparse.ArgumentTypeError(msg)


def apply_conf(args):
    """Load in defaults from the launcher configuration

    :return: The arguments, with the configuration values applied"""
    config = args.config

    if not args.python and config.has('python'):
        args.python = config.get('python')

    if config.has('verbosity') and args.verbose < config.get('verbosity'):
        args.verbose = config.get('verbosity')

    return args


def expand_stack(args):
    """Parse the stack file and expand it with the variables in the configuration

    :args: The argument array
    :return: The arguments, with a expanded and parsed stack"""
    args.stack = StackConf(args.stack, args.config)

    return args
