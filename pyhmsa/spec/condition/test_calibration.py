#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.calibration import \
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

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)

class TestCalibrationConstant(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationConstant('Energy', 'eV', -237.098251)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(-237.098251, self.cal.value, 4)
        self.assertAlmostEqual(-237.098251, self.cal(0), 4)
        self.assertAlmostEqual(-237.098251, self.cal(1), 4)

        self.assertRaises(ValueError, CalibrationConstant, 'Energy', 'eV', None)

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)
        self.assertAlmostEqual(-237.098251, cal.value, 4)
        self.assertAlmostEqual(-237.098251, cal(0), 4)
        self.assertAlmostEqual(-237.098251, cal(1), 4)

class TestCalibrationLinear(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.cal = CalibrationLinear('Energy', 'eV', 2.49985, -237.098251)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(2.49985, self.cal.gain, 4)
        self.assertAlmostEqual(-237.098251, self.cal.offset, 4)
        self.assertAlmostEqual(-237.098251, self.cal(0), 4)
        self.assertAlmostEqual(-237.098251 + 2.49985, self.cal(1), 4)

        self.assertRaises(ValueError, CalibrationLinear, 'Energy', 'eV', None, -237.098251)
        self.assertRaises(ValueError, CalibrationLinear, 'Energy', 'eV', 2.49985, None)

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)
        self.assertAlmostEqual(2.49985, self.cal.gain, 4)
        self.assertAlmostEqual(-237.098251, self.cal.offset, 4)
        self.assertAlmostEqual(-237.098251, cal(0), 4)
        self.assertAlmostEqual(-237.098251 + 2.49985, cal(1), 4)

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
        self.assertAlmostEqual(-0.018, self.cal(0), 4)
        self.assertAlmostEqual(-1.462, self.cal(1), 4)

        self.assertRaises(ValueError, CalibrationPolynomial, 'Energy', 'eV', None)

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)
        self.assertAlmostEqual(-2.255, cal.coefficients[0], 4)
        self.assertAlmostEqual(0.677, cal.coefficients[1], 4)
        self.assertAlmostEqual(0.134, cal.coefficients[2], 4)
        self.assertAlmostEqual(-0.018, cal.coefficients[3], 4)
        self.assertAlmostEqual(-0.018, cal(0), 4)
        self.assertAlmostEqual(-1.462, cal(1), 4)

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
        self.assertAlmostEqual(-2.255, self.cal(0), 4)
        self.assertAlmostEqual(0.677, self.cal(1), 4)
        self.assertAlmostEqual(0.134, self.cal(2), 4)
        self.assertAlmostEqual(-0.018, self.cal(3), 4)

        self.assertRaises(ValueError, CalibrationExplicit, 'Energy', 'eV', None)

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)
        self.assertAlmostEqual(-2.255, cal.values[0], 4)
        self.assertAlmostEqual(0.677, cal.values[1], 4)
        self.assertAlmostEqual(0.134, cal.values[2], 4)
        self.assertAlmostEqual(-0.018, cal.values[3], 4)
        self.assertAlmostEqual(-2.255, cal(0), 4)
        self.assertAlmostEqual(0.677, cal(1), 4)
        self.assertAlmostEqual(0.134, cal(2), 4)
        self.assertAlmostEqual(-0.018, cal(3), 4)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
