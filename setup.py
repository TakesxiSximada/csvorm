#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import (
    setup,
    find_packages,
    )


src = 'src'
here = lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
get_requires = lambda path: open(here(path), 'rt').readlines()

readme_path = here('README.rst')
contributors_path = here('CONTRIBUTORS.rst')

requirements_txt = 'requirements/install.txt'
requires = get_requires(requirements_txt)
install_requires = requires
test_requirements = get_requires('requirements/test.txt')


long_description = open(readme_path, 'rt').read() + '\n\n' + open(contributors_path, 'rt').read()


def find_version():
    for root, dirs, files in os.walk(here(src)):
        for filename in files:
            if filename == 'version.txt':
                version_file = os.path.join(root, filename)
                with open(version_file, 'rt') as fp:
                    for line in fp:
                        line = line.strip()
                        if line:
                            return line
    raise ValueError('unkown version')

version = find_version()


setup(
    name='csvorm',
    version=version,
    url='https://github.com/TakesxiSximada/csvorm',
    download_url='https://github.com/TakesxiSximada/csvorm',
    license='See http://www.python.org/3.4/license.html',
    author='TakesxiSximada',
    author_email='takesxi.sximada@gmail.com',
    description='orm for csv',
    long_description=long_description,
    keywords='csv',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        ],
    platforms='any',
    packages=find_packages(src),
    package_dir={'': src},
    namespace_packages=[
        ],
    package_data={},
    include_package_data=True,
    install_requires=install_requires + test_requirements,
    tests_requires=test_requirements,
    entry_points='''
    [console_scripts]
    '''
    )
