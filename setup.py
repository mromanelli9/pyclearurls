#!/usr/bin/env python

import re
from setuptools import find_packages, setup

VERSION_FILE = "pyclearurls/__init__.py"
with open(VERSION_FILE) as version_file:
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                        version_file.read(), re.MULTILINE)

if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name='pyclearurls',
    version='0.1',
    description='ClearURLs in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Marco Romanelli',
    license='MIT',
    url='https://github.com/mromanelli9/pyclearurls',
    project_urls={
        "Issue Tracker": "https://github.com/mromanelli9/pyclearurls/issues",
        "Source Code": "https://github.com/mromanelli9/pyclearurls",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    package_data={'': ['package_data/data.min.json']},
)
