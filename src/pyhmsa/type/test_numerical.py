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
import numpy as np

# Local modules.
from pyhmsa.type.numerical import NumericalValue

# Globals and constants variables.

class TestNumericalValue(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.v1 = NumericalValue(5.0, 'm')
        self.v2 = NumericalValue(6, 's')
        self.v3 = NumericalValue([5.0, 6.0, 7.0], 'A')
        self.v4 = NumericalValue(None, 's')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(5.0, self.v1.value, 4)
        self.assertAlmostEqual(5.0, self.v1[0], 4)
        self.assertEqual('m', self.v1.unit)
        self.assertEqual('m', self.v1[1])
        self.assertEqual(np.array([5.0])[0].dtype, self.v1.value.dtype)

        self.assertEqual(6, self.v2.value, 4)
        self.assertEqual(6, self.v2[0], 4)
        self.assertEqual('s', self.v2.unit)
        self.assertEqual('s', self.v2[1])
        self.assertEqual(np.array([6])[0].dtype, self.v2.value.dtype)

        self.assertEqual(3, len(self.v3.value))
        self.assertAlmostEqual(5.0, self.v3.value[0], 4)
        self.assertAlmostEqual(6.0, self.v3.value[1], 4)
        self.assertAlmostEqual(7.0, self.v3.value[2], 4)
        self.assertEqual('A', self.v3.unit)
        self.assertEqual(np.array([5.0])[0].dtype, self.v3.value.dtype)

        self.assertIsNone(self.v4.value)
        self.assertEqual('s', self.v4.unit)
        self.assertFalse(bool(self.v4))

        self.assertTrue(bool(NumericalValue(0.0, 's')))

        self.assertRaises(ValueError, NumericalValue, 5.0, 'Wb')
        self.assertRaises(ValueError, NumericalValue, np.float16(4.0), 'm')

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
