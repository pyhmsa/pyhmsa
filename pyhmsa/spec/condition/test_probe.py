#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.probe import _Probe, ProbeEM, ProbeTEM

# Globals and constants variables.
from pyhmsa.spec.condition.probe import GUN_TYPE_LAB6, LENS_MODE_IMAGE

class Test_Probe(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.probe = _Probe()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

class TestProbeEM(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.probe = ProbeEM(15.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testbeam_voltage(self):
        self.assertAlmostEqual(15.0, self.probe.beam_voltage, 4)
        self.assertEqual('kV', self.probe.beam_voltage.unit)
        self.assertRaises(ValueError, self.probe.set_beam_voltage, None)

    def testbeam_current(self):
        self.probe.beam_current = 47.59
        self.assertAlmostEqual(47.59, self.probe.beam_current, 4)
        self.assertEqual('nA', self.probe.beam_current.unit)

    def testgun_type(self):
        self.probe.gun_type = GUN_TYPE_LAB6
        self.assertEqual(GUN_TYPE_LAB6, self.probe.gun_type)
        self.assertRaises(ValueError, self.probe.set_gun_type, 'ABC')

    def testemission_current(self):
        self.probe.emission_current = 12345
        self.assertAlmostEqual(12345, self.probe.emission_current, 4)
        self.assertEqual('uA', self.probe.emission_current.unit)

    def testfilament_current(self):
        self.probe.filament_current = 1.234
        self.assertAlmostEqual(1.234, self.probe.filament_current, 4)
        self.assertEqual('A', self.probe.filament_current.unit)

    def testextractor_bias(self):
        self.probe.extractor_bias = 4200
        self.assertAlmostEqual(4200, self.probe.extractor_bias, 4)
        self.assertEqual('V', self.probe.extractor_bias.unit)

    def testbeam_diameter(self):
        self.probe.beam_diameter = 12345
        self.assertAlmostEqual(12345, self.probe.beam_diameter, 4)
        self.assertEqual('um', self.probe.beam_diameter.unit)

    def testchamber_pressure(self):
        self.probe.chamber_pressure = 3.14e-6
        self.assertAlmostEqual(3.14e-6, self.probe.chamber_pressure, 10)
        self.assertEqual('Pa', self.probe.chamber_pressure.unit)

    def testgun_pressure(self):
        self.probe.gun_pressure = 3.14e-10
        self.assertAlmostEqual(3.14e-10, self.probe.gun_pressure, 14)
        self.assertEqual('Pa', self.probe.gun_pressure.unit)

    def testscan_magnification(self):
        self.probe.scan_magnification = 2500
        self.assertAlmostEqual(2500, self.probe.scan_magnification, 4)

    def testworking_distance(self):
        self.probe.working_distance = 10.0
        self.assertAlmostEqual(10.0, self.probe.working_distance, 4)
        self.assertEqual('mm', self.probe.working_distance.unit)

    def testpickle(self):
        self.probe.beam_current = 47.59
        self.probe.gun_type = GUN_TYPE_LAB6
        self.probe.emission_current = 12345
        self.probe.filament_current = 1.234
        self.probe.extractor_bias = 4200
        self.probe.beam_diameter = 12345
        self.probe.chamber_pressure = 3.14e-6
        self.probe.gun_pressure = 3.14e-10
        self.probe.scan_magnification = 2500
        self.probe.working_distance = 10.0

        s = pickle.dumps(self.probe)
        probe = pickle.loads(s)

        self.assertAlmostEqual(15.0, probe.beam_voltage, 4)
        self.assertEqual('kV', probe.beam_voltage.unit)
        self.assertAlmostEqual(47.59, probe.beam_current, 4)
        self.assertEqual('nA', probe.beam_current.unit)
        self.assertEqual(GUN_TYPE_LAB6, probe.gun_type)
        self.assertAlmostEqual(12345, probe.emission_current, 4)
        self.assertEqual('uA', probe.emission_current.unit)
        self.assertAlmostEqual(1.234, probe.filament_current, 4)
        self.assertEqual('A', probe.filament_current.unit)
        self.assertAlmostEqual(4200, probe.extractor_bias, 4)
        self.assertEqual('V', probe.extractor_bias.unit)
        self.assertAlmostEqual(12345, probe.beam_diameter, 4)
        self.assertEqual('um', probe.beam_diameter.unit)
        self.assertAlmostEqual(3.14e-6, probe.chamber_pressure, 10)
        self.assertEqual('Pa', probe.chamber_pressure.unit)
        self.assertAlmostEqual(3.14e-10, probe.gun_pressure, 14)
        self.assertEqual('Pa', probe.gun_pressure.unit)
        self.assertAlmostEqual(2500, probe.scan_magnification, 4)
        self.assertAlmostEqual(10.0, probe.working_distance, 4)
        self.assertEqual('mm', probe.working_distance.unit)

class TestProbeTEM(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.probe = ProbeTEM(15.0, LENS_MODE_IMAGE)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testlens_mode(self):
        self.assertEqual(LENS_MODE_IMAGE, self.probe.lens_mode)
        self.assertRaises(ValueError, self.probe.set_lens_mode, None)
        self.assertRaises(ValueError, self.probe.set_lens_mode, 'ABC')

    def testcamera_magnification(self):
        self.probe.camera_magnification = 2
        self.assertAlmostEqual(2.0, self.probe.camera_magnification, 4)

    def testconvergence_angle(self):
        self.probe.convergence_angle = 1.5
        self.assertAlmostEqual(1.5, self.probe.convergence_angle, 4)
        self.assertEqual('mrad', self.probe.convergence_angle.unit)

    def testpickle(self):
        self.probe.camera_magnification = 2
        self.probe.convergence_angle = 1.5

        s = pickle.dumps(self.probe)
        probe = pickle.loads(s)

        self.assertEqual(LENS_MODE_IMAGE, probe.lens_mode)
        self.assertAlmostEqual(2.0, probe.camera_magnification, 4)
        self.assertAlmostEqual(1.5, probe.convergence_angle, 4)
        self.assertEqual('mrad', probe.convergence_angle.unit)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
