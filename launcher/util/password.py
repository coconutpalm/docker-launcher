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

"""Module for password management"""

import os
import getpass


def export_password(conf):
    """Ask for docker password if we can't find it in the environment"""
    try:
        os.environ['DOCKER_PASSWORD']
    except KeyError:
        question = "Please specify the DockerHub password for {user}\n"
        question = question.format(user=conf.get('registry')['user'])
        docker_password = getpass.getpass(question)
        os.environ['DOCKER_PASSWORD'] = docker_password
