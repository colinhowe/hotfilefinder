from setuptools import setup

import os

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'
long_desc = open(root_dir + '/README.md').read()

setup(
    name='hotfilefinder',
    version='0.2',
    description='Finds the hottest files in a git repo',
    url='https://github.com/colinhowe/hotfilefinder',
    author='Colin Howe',
    author_email='colin@colinhowe.co.uk',
    packages=['hotfilefinder'],
    entry_points={
        'console_scripts': [
            'hotfilefinder = hotfilefinder:_main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='Apache 2.0',
    long_description=long_desc,
)
