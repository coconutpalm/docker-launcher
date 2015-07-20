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


import re
from launcher.ansible.util import spawn, exec_playbook

STRING = ('This is a test\n'
          'TASK: [no print]\n'
          'PLAY [this should get printed] *******\n'
          'msg: print this\n'
          'failed: no print\n'
          'fatal: print this\n'
          'FATAL print this\n'
          '...ignoring\n'
          'This should be ignored\n')

SHORT_STRING = ('PLAY [this should get printed]\n'
                'msg: print this\n'
                'fatal: print this\n'
                'FATAL print this\n')


def test_spawn_silent(capsys):
    assert spawn(['echo', '-n', STRING], 0) == 0
    out, err = capsys.readouterr()
    assert out == SHORT_STRING


def test_spawn_verbose(capsys):
    assert spawn(['echo', '-n', STRING], 1) == 0
    out, err = capsys.readouterr()
    assert out == STRING


def test_spawn_stderr(capsys):
    assert spawn(['/bin/sh', '-c', 'echo -n something 1>&2'], 0) == 0
    out, err = capsys.readouterr()
    assert err == 'something'


def test_spawn_error(capsys):
    assert spawn(['false'], 0) == 1
    out, err = capsys.readouterr()
    assert out == ''


def test_custom_regex(capsys):
    regex = re.compile('^print this')
    string = ('print this...\n'
              'not this\n')

    assert spawn(['echo', '-n', string], 0,
                 output_regex=regex,
                 stripped_chars=' .\n') == 0
    out, err = capsys.readouterr()
    assert out == 'print this\n'
