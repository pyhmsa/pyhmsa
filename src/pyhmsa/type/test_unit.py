#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.unit import validate_unit, parse_unit, _UNITS, _PREFIXES

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

    def testparse_unit(self):
        p, b, e = parse_unit('km2')
        self.assertEqual('k', p)
        self.assertEqual('m', b)
        self.assertEqual(2.0, e)

        p, b, e = parse_unit('m')
        self.assertIsNone(p)
        self.assertEqual('m', b)
        self.assertEqual(1.0, e)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
