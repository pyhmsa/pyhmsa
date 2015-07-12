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
        self.assertAlmostEqual(-237.098251, self.cal.get_quantity(0), 4)
        self.assertAlmostEqual(-237.098251, self.cal.get_quantity(1), 4)
        self.assertEqual(0, self.cal.get_index(-237.098251))
        self.assertEqual(-1, self.cal.get_index(0))

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
        self.assertAlmostEqual(-237.098251, self.cal.get_quantity(0), 4)
        self.assertAlmostEqual(-237.098251 + 2.49985, self.cal.get_quantity(1), 4)
        self.assertEqual(0, self.cal.get_index(-237.098251))
        self.assertEqual(1, self.cal.get_index(-237.098251 + 2.49985))

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
        self.assertAlmostEqual(-0.018, self.cal.get_quantity(0), 4)
        self.assertAlmostEqual(-1.462, self.cal.get_quantity(1), 4)
        self.assertEqual(0, self.cal.get_index(-0.018))
        self.assertEqual(1, self.cal.get_index(-1.463))
        self.assertEqual(-1, self.cal.get_index(1000))

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

        self.cal = CalibrationExplicit('Energy', 'eV',
                                       (-2.255, -0.018, 0.134, 0.677),
                                       ('a', 'b', 'c', 'd'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(4, len(self.cal.values))
        self.assertEqual(4, len(self.cal.labels))
        self.assertAlmostEqual(-2.255, self.cal.values[0], 4)
        self.assertAlmostEqual(-0.018, self.cal.values[1], 4)
        self.assertAlmostEqual(0.134, self.cal.values[2], 4)
        self.assertAlmostEqual(0.677, self.cal.values[3], 4)
        self.assertEqual('a', self.cal.labels[0])
        self.assertEqual('b', self.cal.labels[1])
        self.assertEqual('c', self.cal.labels[2])
        self.assertEqual('d', self.cal.labels[3])
        self.assertAlmostEqual(-2.255, self.cal(0), 4)
        self.assertAlmostEqual(-0.018, self.cal(1), 4)
        self.assertAlmostEqual(0.134, self.cal(2), 4)
        self.assertAlmostEqual(0.677, self.cal(3), 4)
        self.assertAlmostEqual(-2.255, self.cal.get_quantity(0), 4)
        self.assertAlmostEqual(-0.018, self.cal.get_quantity(1), 4)
        self.assertAlmostEqual(0.134, self.cal.get_quantity(2), 4)
        self.assertAlmostEqual(0.677, self.cal.get_quantity(3), 4)
        self.assertEqual(0, self.cal.get_index(-2.255))
        self.assertEqual(1, self.cal.get_index(-0.018))
        self.assertEqual(2, self.cal.get_index(0.134))
        self.assertEqual(3, self.cal.get_index(0.677))
        self.assertEqual('a', self.cal.get_label(0))
        self.assertEqual('b', self.cal.get_label(1))
        self.assertEqual('c', self.cal.get_label(2))
        self.assertEqual('d', self.cal.get_label(3))

    def testpickle(self):
        s = pickle.dumps(self.cal)
        cal = pickle.loads(s)

        self.assertEqual('Energy', cal.quantity)
        self.assertEqual('eV', cal.unit)
        self.assertAlmostEqual(-2.255, cal.values[0], 4)
        self.assertAlmostEqual(-0.018, cal.values[1], 4)
        self.assertAlmostEqual(0.134, cal.values[2], 4)
        self.assertAlmostEqual(0.677, cal.values[3], 4)
        self.assertAlmostEqual(-2.255, cal(0), 4)
        self.assertAlmostEqual(-0.018, cal(1), 4)
        self.assertAlmostEqual(0.134, cal(2), 4)
        self.assertAlmostEqual(0.677, cal(3), 4)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
