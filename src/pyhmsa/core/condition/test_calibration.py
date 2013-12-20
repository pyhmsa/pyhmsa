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
from pyhmsa.core.condition.calibration import \
    (_Calibration, CalibrationConstant, CalibrationLinear,
     CalibrationPolynomial, CalibrationExplicit)

# Globals and constants variables.

class Test_Calibration(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = _Calibration('Energy', 'eV')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('Energy', self.cal.quantity)
        self.assertEqual('eV', self.cal.unit)

        self.assertRaises(ValueError, _Calibration, None, 'eV')
        self.assertRaises(ValueError, _Calibration, 'Energy', None)

class TestCalibrationConstant(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationConstant('Energy', 'eV', -237.098251)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(-237.098251, self.cal.value, 4)

        self.assertRaises(ValueError, CalibrationConstant, 'Energy', 'eV', None)

class TestCalibrationLinear(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationLinear('Energy', 'eV', 2.49985, -237.098251)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(2.49985, self.cal.gain, 4)
        self.assertAlmostEqual(-237.098251, self.cal.offset, 4)

        self.assertRaises(ValueError, CalibrationLinear, 'Energy', 'eV', None, -237.098251)
        self.assertRaises(ValueError, CalibrationLinear, 'Energy', 'eV', 2.49985, None)

class TestCalibrationPolynomial(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationPolynomial('Energy', 'eV', (-2.255, 0.677, 0.134, -0.018))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(4, len(self.cal.coefficients))
        self.assertAlmostEqual(-2.255, self.cal.coefficients[0], 4)
        self.assertAlmostEqual(0.677, self.cal.coefficients[1], 4)
        self.assertAlmostEqual(0.134, self.cal.coefficients[2], 4)
        self.assertAlmostEqual(-0.018, self.cal.coefficients[3], 4)

        self.assertRaises(ValueError, CalibrationPolynomial, 'Energy', 'eV', None)
        self.assertRaises(ValueError, CalibrationPolynomial, 'Energy', 'eV', [])

class TestCalibrationExplicit(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationExplicit('Energy', 'eV', (-2.255, 0.677, 0.134, -0.018))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(4, len(self.cal.values))
        self.assertAlmostEqual(-2.255, self.cal.values[0], 4)
        self.assertAlmostEqual(0.677, self.cal.values[1], 4)
        self.assertAlmostEqual(0.134, self.cal.values[2], 4)
        self.assertAlmostEqual(-0.018, self.cal.values[3], 4)

        self.assertRaises(ValueError, CalibrationExplicit, 'Energy', 'eV', None)
        self.assertRaises(ValueError, CalibrationExplicit, 'Energy', 'eV', [])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
