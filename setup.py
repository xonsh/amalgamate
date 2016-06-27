#! /usr/bin/env python
import sys
try:
    from setuptools import setup
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAVE_SETUPTOOLS = False


VERSION = "0.1.1"

setup_kwargs = {
    "version": VERSION,
    "description": 'Collapses Python packages into a single module.',
    "license": 'BSD 3-clause',
    "author": 'The xonsh developers',
    "author_email": 'xonsh@googlegroups.com',
    "url": 'https://github.com/xonsh/amalgamate',
    "download_url": "https://github.com/xonsh/amalgamate/zipball/" + VERSION,
    "classifiers": [
        "License :: OSI Approved",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Utilities",
        ],
    "zip_safe": False,
    "scripts": ['amalgamate.py'],
    "data_files": [("", ['LICENSE', 'README.rst']),],
    }


if __name__ == '__main__':
    setup(
        name='amalgamate',
        py_modules=['amalgamate'],
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
