from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='paypal-python', version=version,
  author='Dylan Jay',
  author_email='asko.soukka@iki.fi',
  description="Repoze BFG Example.",
  long_description=open("README.md").read() ,
  license='GPL3',
  # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
  keywords="",
  classifiers=[
    "Programming Language :: Python",
  ],
  url='',
  packages=find_packages(),
  package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.zcml']
  },
  namespace_packages=[],
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'setuptools',
    'setuptools-git',
    # -*- Extra requirements: -*-
  ],
)