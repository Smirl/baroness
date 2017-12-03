"""Setup for baroness."""

from setuptools import setup, find_packages
from pkg_resources import parse_requirements


with open('./README.md') as f:
    long_description = f.read().strip()


with open('./requirements.txt') as f:
    requirements = map(str, parse_requirements(f.readlines()))


with open('./baroness/version.txt') as f:
    version = f.read().strip()


setup(
    name='baroness',
    packages=find_packages('.'),
    version=version,
    description='Toolkit for easy searching and manipulation of python source code using redbaron.',
    long_description=long_description,
    author='Alex Williams',
    url='https://github.com/smirl/baroness',
    tests_require=['pytest', 'pytest-mock', 'pytest-cov'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'baroness=baroness.cli:main',
        ]
    }
)
