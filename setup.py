from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Qobuz',
    version=get_version('mopidy_qobuz/__init__.py'),
    url='https://github.com/taschenb/mopidy-qobuz',
    license='Apache License, Version 2.0',
    author='taschenb',
    author_email='taschenb@posteo.de',
    description='Mopidy extension for playing music from Qobuz',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Mopidy >= 2.0',
        'Pykka >= 1.1',
        'qobuz >= 0.0.2',
        'qobuz_dl >= 0.9.7',
        'keyring >= 23.0.0',
        'setuptools',
    ],
    entry_points={
        'mopidy.ext': [
            'qobuz = mopidy_qobuz:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
