#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class TestConditions(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cnds = Conditions()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__setitem__(self):
        cnd = _Condition()
        self.cnds['Condition1'] = cnd
        self.assertEqual(1, len(self.cnds))
        self.assertIs(cnd, self.cnds['Condition1'])

        self.assertRaises(ValueError, self.cnds.__setitem__, u'\u00b0', cnd)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
