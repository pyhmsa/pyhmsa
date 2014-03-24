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
from pyhmsa.util.element_properties import get_atomic_number, get_symbol

# Globals and constants variables.

class Test_ElementPropertiesDatabase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testsymbol(self):
        self.assertEqual('H', get_symbol(1))
        self.assertEqual('Uuo', get_symbol(118))

    def testatomic_number(self):
        self.assertEqual(1, get_atomic_number('H'))
        self.assertEqual(118, get_atomic_number('Uuo'))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
