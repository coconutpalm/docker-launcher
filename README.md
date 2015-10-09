[![Circle CI](https://circleci.com/gh/advancedtelematic/docker-launcher.svg?style=svg)](https://circleci.com/gh/advancedtelematic/docker-launcher)

# Docker Launcher

Launches Docker container stacks on EC2 or localhost.

## Installing

To build and install `docker-launcher`:

```sh
cd docker-launcher
python setup.py sdist
sudo pip install dist/docker-launcher-0.1.tar.gz
```

**Note:** You can install both packages with `pip install --user PACKAGE_NAME`
to install to `~/.local/bin` and avoid installing with root rights.

### Installing on ArchLinux

You need to have `python2` and `python2-pip` installed.

```sh
cd docker-launcher
python2 setup.py sdist
sudo pip2 install dist/docker-launcher-0.1.tar.gz
# OR
pip2 install --user dist/docker-launcher-0.1.tar.gz
```

On ArchLinux you will also need to configure `docker-launcher` to use `python2`
for `ansible`. See Section **Configuration** on how to do that.

## Running

```sh
> docker-launcher -h

usage: docker-launcher [-h] [-c CONFIG] [-v] [--python EXEC] [--version]
                       [--teardown] [--jenkins NUM]
                       STACK

positional arguments:
  STACK                 The stack configuration to use

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The launcher configuration to use
  -v, --verbose         Level of verbosity (specify multiple times)
  --python EXEC         The local python version to use (defaults to python)
  --version             show program's version number and exit
  --teardown            Stop and teardown the STACK
  --jenkins NUM         Deploy the STACK, run the test suite and tear it down
                        again. Try NUM times to deploy before failing.


> bin/docker-launcher auth-plus.yml
...deploys auth-plus.yml...
```

`docker-launcher` will create a temporary playbook and inventory file. If the
deployment fails for some reason, these will not get cleaned up, so you can dig
into what went wrong. You should always be able to run them with
`ansible-playbook -i tmp-inventory tmp-playbook`.

## Configuration

Docker Launcher reads a configuration in either
`$XDG_CONFIG_HOME/docker-launcher/default.yml` or
`$HOME/.config/docker-launcher/default.yml`, whichever it finds first, unless
you specify one explicitly on the command line. If the specified configuration
file doesn't exist, `docker-launcher` will write a default configuration file at
the specified path. You will need to edit it to match your setup.

An example configuration can be found in `tests/test-config.yml`. The following
keys are mandatory:

```yaml
---
reboot_strategy: 'off'         # CoreOS update strategy (quotes are needed)
registry:                      # login credentials for DockerHub
  user: atsjenkins
  email: jenkins@advancedtelematic.com
ec2:                           # default settings for EC2
  key: integration_tests       # SSH key to be used
  image: ami-07fd8270          # ami to be deployed
  region: eu-west-1            # EC2 region to deploy to
```

Optionally you can include the following keys:

```yaml
verbosity: 3                   # default level of verbosity
                               # can be raised by -v flags
python: python2                # local python executable to be used by ansible,
                               # this is needed on ArchLinux for example
                               # can be overwritten by --python flag
vars:                          # a map of keys, that get expanded to value in the stack configuration
  key: value
```

## Stack Config

The setup of a Docker container stack is defined in stack config files, which
are yaml files in the following form:

```yaml
---
security_groups:                  # list of security groups to create (optional)
  - name:                         # name of the security group
    description:                  # description of the security group
    rules:                        # list of security group rules
      - proto: tcp                # The syntax is the same as the ansible
        from_port: 80             # ec2_group module
        to_port: 80               # http://docs.ansible.com/ec2_group_module.html
        cidr_ip: 0.0.0.0/0
    rules_egress:                 # the security group outbound rules
      - proto: all                # syntax same as ec2_group module
        cidr_ip: 0.0.0.0/0

logging: true                     # adds logspout, logstash, elasticsearch and kibana 

nodes:                            # list of different node types, that are required
  - name: node-name               # name for this kind of node
    group: security-group-name    # EC2 security group
    services:                     # services to run on this kind of node
      - one
      - two
    size: t2.medium               # EC2 size
    count: 1                      # amount of nodes to be created
    logging_master: true          # When set, logstash, elasticsearch and kibana are
                                  # added to this host. Kibana is available on 
                                  # port 5454
    volumes:                      # EBS volumes to create, attach, format and mount
      - dev: /dev/xvda1
        size: 30                  # in GB
        fs: btrfs
        mountpoint: /mnt
  - name: another-node
    group: default
    services:
      - three
    size: t2.medium
    count: 3

services:                         # definition of services
  - name: one                     # service name (same as in nodes)
    version: 0.1                  # version of the application (e.g. Docker tag)
    repo: some-repo/on-dockerhub  # repo on DockerHub
    command: /bin/true            # change the command that gets run
    wait:                         # this service needs some time to start
      post: 9042                  # wait for it on this port
      delay: 30                   # for that many seconds
    env:
      SOME_ENV: "some value"      # manipulates the environment of the container
      ANOTHER: "{{ key }}"        # You can use jinja2 to expand keys from the var section in the configuration
    advertised_port: 3000         # This port gets advertised to services linking to this service
                                  # if not provided, defaults to left # side of first value in ports (eg. 3000)
    ports:                        # ports to be exposed and published
      - 3000:3001
      - 4000                      # you can give one int here, the other one is set to the same value
    expose:                       # ports to be exposed
      - 5000/udp
      - 6000
    links:                        # connections to other services
      - one                       # links via docker --link on localhost and via HAProxy on EC2
      - two
      - three[direct]             # Adding [direct] links straight to host, not through proxy,
                                  # only use if you really need to.
    volumes:                      # volumes to be attached to the container
      - /some/path                # same semantic as in docker --volume (this defines a volume)
      - /some/path:/another/path  # same semantic as in docker --volume (this mounts a volume to the host at '/some/path')
    volumes_from:                 # attach all defined volumes from container 'one'
      - one
    files:                        # files that need to be uploaded to the node
      - some/local/file:/some/absolute/remote/path
    migrations:
      cql:                        # Requires a cassandra container to be linked
        - schema.cql              # Array of cql files that will be executed
        - default-data.cql        # against the linked cassandra
    restart_policy: always        # Container restart policy, defaults to 'always'
                                  # Available options are 'no', 'on-failure', 'always'
    attach: True                  # Run container with an open tty, you can jump into it by running `docker attach`
    pull: False                   # Disables unconditional pull, useful if your images are not on DockerHub, or you want to bypass those
  - name: cronjob
    repo: some-repo/cronjob
    schedule:                     # you can run containers periodically with schedule
      onboot: 3min                # cronjob will run 3min after boot and then every 2 hours
      schedule: 2h                # see systemd.time(7) for details on the time format
      description: "a simple cronjob"


# The tests are considered successful, if all tests exit cleanly (with a return value of 0).
tests:
  - name: integration
    target: haproxy               # You can use the IP of this service with the %TARGET variable
                                  # %TARGET is expanded in the values of env:, command: and args:
    docker:
      name: integration-test
      version: latest
      repo: some/integration-test
      command: /run.sh --host %TARGET
      env:
        SOME_ENV: "some value"
        HOST: %TARGET

  - name: load
    target: haproxy
    shell:
      name: ./some_script.sh
      args: --host %TARGET
```

Some values are required, `docker-launcher` will refuse to run, if you leave
them out. The smallest possible stack config is:

```yaml
services:
  - name: one
    repo: someone/something
```

Which spawns `someone/something:latest` as `one` on `localhost`. The smallest
possible stack config, that sets up nodes on EC2 is:

```yaml
nodes:
  - name: one
    group: default
    services:
      - one
    size: t2.micro
    count: 1
services:
  - name: one
    repo: someone/something
security_groups:
  - name: example-grp
    description: "This cannot be left blank"
    rules:           #need this so ansible can connect to the node
      - proto: tcp
        from_port: 22
        to_port: 22
        cidr_ip: 0.0.0.0/0
    rules_egress:     #need this so the instance can connect out to dockerhub
      - proto: all
        cidr_ip: 0.0.0.0/0
```

See the example directory for more examples. You can also take a look at the Rx
schema for stack config in `launcher/util/schema/stack_conf.yml`, have a look
at [the Rx documentation](http://rx.codesimply.com/coretypes.html) to understand
the syntax.

### **Example**: data container

This is example starts a database with its data being stored in another
container (data-only container). We need to specify a restart policy, as restart
is the default since version `0.1.5`, which would lead to the data container
being restarted over and over again.

```yaml
---
services:
  - name: mysql-data
    restart_policy: "on-failure"
    repo: busybox
    volumes:
      - /var/lib/mysql
    command: "true"

  - name: mysql
    repo: mysql
    ports:
      - 3306
    env:
      MYSQL_ROOT_PASSWORD: "super-secret"
      MYSQL_USER: "test"
      MYSQL_PASSWORD: "super-secret"
    volumes_from:
      - mysql-data
```

## Problems/Known Bugs

- migrations will run every time
- no sanity checks on the cloud config (no HAProxy etc)
- services connect via public IPs
- suboptimal type checking (Rx types) on yaml files
- support more scheduling techniques/schedules
- insufficient documentation on jinja2 usage in stack configurations

### SSH Errors

If you get an error like the following when deploying to EC2:

`SSH Error: data could not be sent to the remote host. Make sure this host can
be reached over ssh`

Put the content below into `~/.ansible.cfg` (create it if it doesn't exist):

```
[defaults]
# disable SSH key host checking
host_key_checking = False
timeout = 30
transport = paramiko
[paramiko_connection]
# do not record new host keys
record_host_keys = False
```

## Development Virtualenv

The steps for installing the requirements in a virtualenv for developing on
`docker-launcher` are as follows:

```sh
virtualenv venv
. venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## Tests

The tests require py.test. Install it with:

```sh
pip install pytest
```

They can be run with:

```sh
py.test tests/
```

For code coverage run:

```sh
py.test --cov launcher tests/
```

## Examples of docker-launcher in production

To get a picture of how docker-launcher is used in the real world, you can take a look at the ATS-developed [GENIVI SOTA project](http://advancedtelematic.github.io/rvi_sota_server/). It uses docker-launcher to deploy both the server and client, as well as the RVI communication nodes.

## Copyright

Copyright © 2015 ATS Advanced Telematic Systems GmbH

This file is part of Docker Launcher.

Docker Launcher is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Docker Launcher is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Docker Launcher. If not, see <http://www.gnu.org/licenses/>.

