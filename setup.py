#######################################################################
# Copyright (c) 2022 Jordan Schaffrin                                 #
#                                                                     #
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################

from setuptools import setup

def read_file(filename: str) -> str:
    text_result = r''

    with open(filename, r'r') as the_file:
        text_result = the_file.read()

    return text_result

setup(
    name=r'mdbpg',
    version=r'0.1.0',    
    description=r'Handle both Postgres and MongoDB queries in an interchangable manner.',
    long_description=read_file(r'./README.md'),
    long_description_content_type=r'text/markdown',
    url=r'https://github.com/wuotes/mdbpg',
    download_url=r'https://pypi.org/project/mdbpg/',
    author=r'Jordan Schaffrin',
    author_email=r'mailbox@xrtuen.com',
    license=r'Mozilla Public License 2.0',
    python_requires=r'>=3.9',
    packages=[r'mdbpg'],
    install_requires=[r'mtoml>=1.1.2',
                      r'psycopg2>=2.9.3',
                      r'pymongo>=4.1.1',
                      r'dnspython>=2.2.1',
                      ],

    classifiers=[
        r'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        r'Programming Language :: Python :: 3.9',
        r'Programming Language :: Python :: 3.10',
        r'Programming Language :: Python :: 3.11',
        r'Programming Language :: Python :: 3.12',
        r'Operating System :: Microsoft :: Windows',
        r'Operating System :: POSIX :: Linux',
        r'Operating System :: MacOS',
    ],
)
