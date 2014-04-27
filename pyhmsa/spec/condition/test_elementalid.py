#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.elementalid import ElementalID, ElementalIDXray

# Globals and constants variables.

class TestElementalID(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.element = ElementalID(11)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        element = ElementalID(symbol='Na')
        self.assertEqual(11, element.atomic_number)
        self.assertEqual('Na', element.symbol)

        self.assertRaises(ValueError, ElementalID)

    def testz(self):
        self.assertEqual(11, self.element.atomic_number)

        self.assertRaises(ValueError, self.element.set_atomic_number, -1)
        self.assertRaises(ValueError, self.element.set_atomic_number, 119)
        self.assertRaises(ValueError, self.element.set_atomic_number, None)

    def testsymbol(self):
        self.assertEqual('Na', self.element.symbol)

        self.element.set_symbol('Fe')
        self.assertEqual('Fe', self.element.symbol)
        self.assertEqual(26, self.element.atomic_number)

        self.assertRaises(ValueError, self.element.set_symbol, "Ab")

    def testpickle(self):
        s = pickle.dumps(self.element)
        element = pickle.loads(s)

        self.assertEqual(11, element.atomic_number)
        self.assertEqual('Na', element.symbol)

class TestElementalIDXray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.element = ElementalIDXray(11, 'Ma')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testline(self):
        self.assertEqual('Ma', self.element.line)
        self.assertRaises(ValueError, self.element.set_line, None)

    def testenergy(self):
        self.element.energy = 1234
        self.assertAlmostEqual(1234, self.element.energy, 4)
        self.assertEqual('eV', self.element.energy.unit)

    def testpickle(self):
        self.element.energy = 1234

        s = pickle.dumps(self.element)
        element = pickle.loads(s)

        self.assertEqual(11, element.atomic_number)
        self.assertEqual('Na', element.symbol)
        self.assertEqual('Ma', element.line)
        self.assertAlmostEqual(1234, element.energy, 4)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
