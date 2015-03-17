#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import (
    setup,
    find_packages,
    )


def find_package_data(target, package_root):
    return [
        os.path.relpath(os.path.join(root, filename), package_root)
        for root, dirs, files in os.walk(target)
        for filename in files
        ]

src = 'src'
requires = [
    'six',
    'unicodecsv',
    ]
install_requires = []
test_require = []
packages = find_packages(src)
package_dir = {'': src}
package_data = {}

long_description = 'This allows to use the CSV as ORM'
try:
    with open('README') as fp:
        long_description = fp.read()
except:
    pass


setup(
    name='csvorm',
    version='0.1.4',
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
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        ],
    platforms='any',
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    include_package_data=True,
    requires=requires,
    install_requires=install_requires,
    test_require=test_require,
    entry_points='''
    [console_scripts]
    '''
    )
