#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.numerical import convert_value, validate_dtype, convert_unit

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

    def testconvert_unit(self):
        u = convert_value(5.0, 'km')
        v = convert_unit('m', u)
        self.assertAlmostEqual(5000.0, v, 4)
        self.assertEqual('m', v.unit)

        u = convert_value(5.0, 'km')
        v = convert_unit('km', u)
        self.assertAlmostEqual(5.0, v, 4)
        self.assertEqual('km', v.unit)

        v = convert_unit('m', 5.0, 'km')
        self.assertAlmostEqual(5000.0, v, 4)

class Testarrayunit(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.v = convert_value(5.0, 's')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testpickle(self):
        s = pickle.dumps(self.v)
        v = pickle.loads(s)

        self.assertAlmostEqual(5.0, v, 4)
        self.assertEqual('s', v.unit)

    def testformat(self):
        self.assertEqual('5.0', '{0:s}'.format(self.v))
        self.assertEqual('5.000', '{0:.3f}'.format(self.v))
        self.assertEqual('5.000 s', '{0:.3f} {0.unit:s}'.format(self.v))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
