#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import validate_identifier

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testvalidate_identifier(self):
        self.assertTrue(validate_identifier('abc'))
        self.assertTrue(validate_identifier('abc_asda-|(sadfa)'))
        self.assertRaises(ValueError, validate_identifier, u'\u00b0C')

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
