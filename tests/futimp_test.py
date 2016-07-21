"""from __future__ import tests"""
import os

import amalgamate

LINES = None

def setup_module():
    global LINES
    amalgamate.main(['amal', 'futimp'])
    with open(os.path.join('futimp', '__amalgam__.py')) as f:
        raw = f.read()
    LINES = raw.splitlines()


def test_only_one():
    assert 1 == len([l for l in LINES if l.startswith('from __future__ import ')])


def test_gets_both():
    line = [l for l in LINES if l.startswith('from __future__ import ')][0]
    assert 'from __future__ import print_function, unicode_literals' == line
