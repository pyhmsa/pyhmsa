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
from pyhmsa.type.numerical import convert_value, validate_dtype

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def validate_dtype(self):
        self.assertTrue(validate_dtype(np.uint8))
        self.assertTrue(validate_dtype(np.dtype(np.uint8)))
        self.assertTrue(validate_dtype(np.uint8(9)))

        self.assertRaises(ValueError, validate_dtype, 'abc')
        self.assertRaises(ValueError, validate_dtype, np.float128)

    def testconvert_value(self):
        # Numerical value
        x = convert_value(5.0, 's')
        self.assertAlmostEqual(5.0, x, 4)
        self.assertEqual('s', x.unit)

        x = convert_value(None, 'ms')
        self.assertIsNone(x)

        x = convert_value([5.0, 6.0, 7.0], 'A')
        self.assertEqual(3, len(x))
        self.assertAlmostEqual(5.0, x[0], 4)
        self.assertAlmostEqual(6.0, x[1], 4)
        self.assertAlmostEqual(7.0, x[2], 4)
        self.assertEqual('A', x.unit)

        x = convert_value(x)
        self.assertEqual(3, len(x))
        self.assertAlmostEqual(5.0, x[0], 4)
        self.assertAlmostEqual(6.0, x[1], 4)
        self.assertAlmostEqual(7.0, x[2], 4)
        self.assertEqual('A', x.unit)

        x = convert_value(x, 'nm')
        self.assertEqual(3, len(x))
        self.assertAlmostEqual(5.0, x[0], 4)
        self.assertAlmostEqual(6.0, x[1], 4)
        self.assertAlmostEqual(7.0, x[2], 4)
        self.assertEqual('A', x.unit)

        self.assertRaises(ValueError, convert_value, (5.0, 's', 'ms'), 'ks')

        # Numpy type
        x = convert_value(5.0)
        self.assertAlmostEqual(5.0, x, 4)
        self.assertTrue(hasattr(x, 'dtype'))

        x = convert_value(np.uint32(9))
        self.assertEqual(9, x)
        self.assertEqual(np.uint32, x.dtype.type)

        self.assertRaises(ValueError, convert_value, np.int8(5.0))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
