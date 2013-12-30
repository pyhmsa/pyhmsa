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
from pyhmsa.spec.condition.elementid import ElementID, ElementIDXray

# Globals and constants variables.

class TestElementID(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.element = ElementID(11)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testz(self):
        self.assertEqual(11, self.element.atomic_number)

        self.assertRaises(ValueError, self.element.set_atomic_number, -1)
        self.assertRaises(ValueError, self.element.set_atomic_number, 119)
        self.assertRaises(ValueError, self.element.set_atomic_number, None)

    def testsymbol(self):
        self.assertEqual('Na', self.element.symbol)

class TestElementIDXray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.element = ElementIDXray(11, u'M\u03b1')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testline(self):
        self.assertEqual(u'M\u03b1', self.element.line)
        self.assertRaises(ValueError, self.element.set_line, None)

    def testenergy(self):
        self.element.energy = 1234
        self.assertAlmostEqual(1234, self.element.energy, 4)
        self.assertEqual('eV', self.element.energy.unit)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
