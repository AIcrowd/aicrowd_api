#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['requests>=2.18.4', 'redis']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="S.P. Mohanty",
    author_email='mohanty@aicrowd.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Python api for interacting with AIcrowd Grading infrastructure",
    entry_points={
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='aicrowd_api aicrowd crowdai_api crowdai',
    name='aicrowd_api',
    packages=find_packages(include=['aicrowd_api']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AIcrowd/aicrowd_api',
    version='0.1.23',
    zip_safe=False,
)
