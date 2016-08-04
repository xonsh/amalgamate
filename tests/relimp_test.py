"""Relative import tests"""
import os

import pytest

import amalgamate

LINES = None

def setup_module():
    global LINES
    amalgamate.main(['amal', 'relimp'])
    with open(os.path.join('relimp', '__amalgam__.py')) as f:
        raw = f.read()
    LINES = raw.splitlines()


@pytest.mark.parametrize('mod,pkg,level,exp', [
    ('x', 'x', 0, True),
    ('x', 'y', 0, False),
    (None, 'x', 1, True),
    ('x', 'y', 1, False),
    ('x', 'x', 2, False),
    ])
def test_module_is_package(mod, pkg, level, exp):
    assert exp is amalgamate.module_is_package(mod, pkg, level)


@pytest.mark.parametrize('mod,pkg,level,exp', [
    ('x.a', 'x', 0, True),
    ('x.a', 'y', 0, False),
    (None, 'x', 1, True),
    ('a', 'y', 1, True),
    ('a', 'x', 2, False),
    ])
def test_module_from_package(mod, pkg, level, exp):
    assert exp is amalgamate.module_from_package(mod, pkg, level)


@pytest.mark.parametrize('mod,pkg,level,default,exp', [
    # all of the following in package x
    # from x.a import ---
    ('x.a', 'x', 0, None, ('x', 'a')),
    # from x.y.a import ---
    ('x.y.a', 'x.y', 0, None, ('x.y', 'a')),
    # from . import ---
    (None, 'x', 1, 'a', ('x', 'a')),
    (None, 'x.y', 1, 'a', ('x.y', 'a')),
    # from .. import ---
    (None, 'y', 2, 'a', (None, None)),
    # from .y import ---
    ('y', 'x', 1, 'a', ('x', 'y')),
    ('y', 'x', 1, None, ('x', 'y')),
    ])
def test_resolve_package_module(mod, pkg, level, default, exp):
    assert exp == amalgamate.resolve_package_module(mod, pkg, level,
                                                    default=default)


def test_from_dot_import_a():
    assert 'from . import a' in LINES


def test_not_from_dotx_import_b():
    assert 'from .x import b' not in LINES

