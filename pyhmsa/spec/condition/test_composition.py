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
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.composition import CompositionElemental

# Globals and constants variables.

class TestCompositionElemental(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.comp = CompositionElemental('atoms', {11: 3})
        self.comp[13] = 1
        self.comp.update({9: 6})

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('atoms', self.comp.unit)
        self.assertAlmostEqual(3, self.comp[11], 4)
        self.assertAlmostEqual(1, self.comp[13], 4)
        self.assertAlmostEqual(6, self.comp[9], 4)

        self.assertRaises(ValueError, CompositionElemental, 'A')

    def test__setitem__(self):
        self.assertRaises(ValueError, self.comp.__setitem__, -1, 1)
        self.assertRaises(ValueError, self.comp.__setitem__, 119, 1)

        self.comp['Al'] = 4
        self.assertEqual(4, self.comp['Al'])
        self.assertEqual(4, self.comp[13])

    def testpickle(self):
        s = pickle.dumps(self.comp)
        comp = pickle.loads(s)

        self.assertEqual('atoms', comp.unit)
        self.assertAlmostEqual(3, comp[11], 4)
        self.assertAlmostEqual(1, comp[13], 4)
        self.assertAlmostEqual(6, comp[9], 4)


if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
