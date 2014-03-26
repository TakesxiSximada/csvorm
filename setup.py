from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='csvorm',
      version=version,
      description="orm for csv",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='csv',
      author='TakesxiSximada',
      url='https://bitbucket.org/takesxi_sximada/csvorm',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
