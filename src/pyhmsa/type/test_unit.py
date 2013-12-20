#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.unit import validate_unit, _UNITS, _PREFIXES

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testvalidate_unit(self):
        for unit in _UNITS:
            if unit in [u'\u00c5', 's', 'g']:
                self.assertTrue(validate_unit(unit))
            else:
                for prefix in _PREFIXES:
                    self.assertTrue(validate_unit(prefix + unit))

        self.assertRaises(ValueError, validate_unit, 'Wb')
        self.assertRaises(ValueError, validate_unit, 'Mg')
        self.assertRaises(ValueError, validate_unit, 'ks')
        self.assertRaises(ValueError, validate_unit, u'k\u00c5')
        self.assertRaises(ValueError, validate_unit, 'Km')

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
