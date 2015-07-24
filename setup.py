from setuptools import setup, find_packages
from launcher import VERSION

with open('README.md') as readme:
    README = readme.read()

setup(name='docker-launcher',
      version=VERSION,

      description=('Deploy multi-node, multi-container clusters '
                   'from simple configuration files'),
      long_description=README,

      author='ATS Advanced Telematic Systems GmbH',

      packages=find_packages(),
      include_package_data=True,

      install_requires=['pyyaml', 'jinja2', 'boto', 'pyrx-ats', 'ansible', 'docker-py==1.2.3'],
      extras_require={'dev': ['pytest', 'pytest-cov', 'pylint']},

      scripts=['bin/docker-launcher'])
