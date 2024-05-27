#!/usr/bin/env python3
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-colortag',
    version='2.4.3',
    description='Django tools for data tagging models',
    long_description=long_description,
    keywords='django models tagging',
    url='https://github.com/apluslms/django-colortag',
    author='Jaakko Kantojärvi',
    author_email='jaakko@n-1.fi',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data = True,

    install_requires=[
        'Django >=3.2.0, <5',
        'django-html5-colorfield >=2.0, <3',
        'js-jquery-toggle-django >=1.1.0, <2',
    ],
    dependency_links=[
        'git+https://github.com/apluslms/js-jquery-toggle.git@1.1.0#egg=js-jquery-toggle-django-1.1.0&subdirectory=django',
    ],
)
