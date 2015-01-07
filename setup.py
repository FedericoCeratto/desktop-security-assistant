#!/usr/bin/env python

from setuptools import setup

__version__ = '0.0.7'

CLASSIFIERS = map(str.strip,
"""Environment :: Console
Environment :: X11 Applications :: GTK
License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)
Natural Language :: English
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 2.7
Topic :: Security
""".splitlines())

entry_points = {
    'console_scripts': [
        'security-assistant = desktop_security_assistant.main:main',
    ]
}

setup(
    name="desktop-security-assistant",
    version=__version__,
    author="Federico Ceratto",
    author_email="federico.ceratto@gmail.com",
    description="Desktop Security Assistant",
    license="AGPLv3+",
    url="https://github.com/FedericoCeratto/desktop-security-assistant",
    long_description="",
    classifiers=CLASSIFIERS,
    keywords="desktop security",
    install_requires=[
        'PyYAML',
        'setproctitle>=1.0.1',
    ],
    packages=['desktop_security_assistant'],
    package_dir={'desktop_security_assistant': 'desktop_security_assistant'},
    platforms=['Linux'],
    zip_safe=False,
    entry_points=entry_points,
    # Used by setup.py bdist to include files in the binary package
    package_data={'desktop_security_assistant': ['checks/*.yaml']},
)
