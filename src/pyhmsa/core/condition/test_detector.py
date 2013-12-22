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
from pyhmsa.core.condition.detector import \
    (PulseHeightAnalyser, WindowLayer, Window,
     _Detector, DetectorCamera, DetectorSpectrometer,
     DetectorSpectrometerCL, DetectorSpectrometerWDS, DetectorSpectrometerXEDS)
from pyhmsa.core.condition.calibration import CalibrationConstant

# Globals and constants variables.
from pyhmsa.core.condition.detector import \
    (PHA_MODE_DIFFERENTIAL, SIGNAL_TYPE_ELS, COLLECTION_MODE_PARALLEL,
     XEDS_TECHNOLOGY_SILI)

class TestPulseHeightAnalyser(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.pha = PulseHeightAnalyser(1750, 32, 0.5, 4.5, PHA_MODE_DIFFERENTIAL)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testbias(self):
        self.assertTrue(self.pha.bias)
        self.assertAlmostEqual(1750, self.pha.bias.value, 4)
        self.assertEqual('V', self.pha.bias.unit, 4)

    def testgain(self):
        self.assertTrue(self.pha.gain)
        self.assertAlmostEqual(32, self.pha.gain, 4)

    def testbase_level(self):
        self.assertTrue(self.pha.base_level)
        self.assertAlmostEqual(0.5, self.pha.base_level.value, 4)
        self.assertEqual('V', self.pha.base_level.unit, 4)

    def testwindow(self):
        self.assertTrue(self.pha.window)
        self.assertAlmostEqual(4.5, self.pha.window.value, 4)
        self.assertEqual('V', self.pha.window.unit, 4)

    def testmode(self):
        self.assertEqual(PHA_MODE_DIFFERENTIAL, self.pha.mode)

        self.assertRaises(ValueError, self.pha.set_mode, 'ABC')

class TestWindowLayer(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.layer = WindowLayer("Al", (100.0, 'nm'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testmaterial(self):
        self.assertEqual('Al', self.layer.material)

        self.assertRaises(ValueError, self.layer.set_material, None)

    def testthickness(self):
        self.assertAlmostEqual(100.0, self.layer.thickness.value, 4)
        self.assertEqual('nm', self.layer.thickness.unit)

        self.assertRaises(ValueError, self.layer.set_thickness, None)

class TestWindow(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.window = Window()
        self.window.append_layer('Al', 0.5)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testlayers(self):
        self.assertEqual(1, len(self.window.layers))
        self.assertEqual('Al', self.window.layers[0].material)
        self.assertAlmostEqual(0.5, self.window.layers[0].thickness.value, 4)
        self.assertEqual(u'\u00b5m', self.window.layers[0].thickness.unit, 4)

        self.window.layers.append(WindowLayer('Be', 0.3))
        self.assertEqual(2, len(self.window.layers))
        self.assertEqual('Be', self.window.layers[1].material)
        self.assertAlmostEqual(0.3, self.window.layers[1].thickness.value, 4)
        self.assertEqual(u'\u00b5m', self.window.layers[1].thickness.unit, 4)

class Test_Detector(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.det = _Detector()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
    
    def testsignal_type(self):
        self.det.signal_type = SIGNAL_TYPE_ELS
        self.assertEqual(SIGNAL_TYPE_ELS, self.det.signal_type)

        self.assertRaises(ValueError, self.det.set_signal_type, 'ABC')

    def testmanufacturer(self):
        self.det.manufacturer = 'Example Inc.'
        self.assertEqual('Example Inc.', self.det.manufacturer)

    def testmodel(self):
        self.det.model = 'Example Model 123'
        self.assertEqual('Example Model 123', self.det.model)

    def testserial_number(self):
        self.det.serial_number = '12345-abc-67890'
        self.assertEqual('12345-abc-67890', self.det.serial_number)

    def testmeasurement_unit(self):
        self.det.measurement_unit = None
        self.assertEqual('counts', self.det.measurement_unit)

        self.det.measurement_unit = 'A'
        self.assertEqual('A', self.det.measurement_unit)

    def testelevation(self):
        self.det.elevation = 45.0
        self.assertAlmostEqual(45.0, self.det.elevation.value, 4)
        self.assertEqual(u'\u00b0', self.det.elevation.unit)

    def testazimuth(self):
        self.det.azimuth = 0.0
        self.assertAlmostEqual(0.0, self.det.azimuth.value, 4)
        self.assertEqual(u'\u00b0', self.det.azimuth.unit)

    def testdistance(self):
        self.det.distance = 50.0
        self.assertAlmostEqual(50.0, self.det.distance.value, 4)
        self.assertEqual('mm', self.det.distance.unit)

    def testarea(self):
        self.det.area = 20.0
        self.assertAlmostEqual(20.0, self.det.area.value, 4)
        self.assertEqual('mm2', self.det.area.unit)

    def testsolid_angle(self):
        self.det.solid_angle = 1.0
        self.assertAlmostEqual(1.0, self.det.solid_angle.value, 4)
        self.assertEqual('sr', self.det.solid_angle.unit)

    def testsemi_angle(self):
        self.det.semi_angle = 3.4
        self.assertAlmostEqual(3.4, self.det.semi_angle.value, 4)
        self.assertEqual('mrad', self.det.semi_angle.unit)

    def testtemperature(self):
        self.det.temperature = -20.0
        self.assertAlmostEqual(-20.0, self.det.temperature.value, 4)
        self.assertEqual(u'\u00b0\u0043', self.det.temperature.unit)

class TestDetectorCamera(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.det = DetectorCamera(512, 400)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testpixel_count_u(self):
        self.assertEqual(512, self.det.pixel_count_u)

        self.assertRaises(ValueError, self.det.set_pixel_count_u, None)

    def testpixel_count_v(self):
        self.assertEqual(400, self.det.pixel_count_v)

        self.assertRaises(ValueError, self.det.set_pixel_count_v, None)

    def testexposure_time(self):
        self.det.exposure_time = 200.0
        self.assertAlmostEqual(200.0, self.det.exposure_time.value, 4)
        self.assertEqual('ms', self.det.exposure_time.unit)

    def testmagnification(self):
        self.det.magnification = 4.5
        self.assertAlmostEqual(4.5, self.det.magnification, 4)

    def testfocal_length(self):
        self.det.focal_length = 80.0
        self.assertAlmostEqual(80.0, self.det.focal_length.value, 4)
        self.assertEqual('mm', self.det.focal_length.unit)

class TestDetectorSpectrometer(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.det = DetectorSpectrometer(4096, calibration)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testchannel_count(self):
        self.assertEqual(4096, self.det.channel_count)

        self.assertRaises(ValueError, self.det.set_channel_count, None)

    def testcalibration(self):
        self.assertEqual('Energy', self.det.calibration.quantity)
        self.assertEqual('eV', self.det.calibration.unit)
        self.assertAlmostEqual(-237.098251, self.det.calibration.value, 4)

        self.assertRaises(ValueError, self.det.set_calibration, None)

    def testcollection_mode(self):
        self.det.collection_mode = COLLECTION_MODE_PARALLEL
        self.assertEqual(COLLECTION_MODE_PARALLEL, self.det.collection_mode)

        self.assertRaises(ValueError, self.det.set_collection_mode, 'ABC')

class TestDetectorSpectrometerCL(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.det = DetectorSpectrometerCL(4096, calibration)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testgrating_d(self):
        self.det.grating_d = 800.
        self.assertAlmostEqual(800.0, self.det.grating_d.value, 4)
        self.assertEqual('mm-1', self.det.grating_d.unit)

class TestDetectorSpectrometerWDS(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.det = DetectorSpectrometerWDS(4096, calibration)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testdispersion_element(self):
        self.det.dispersion_element = 'TAP'
        self.assertEqual('TAP', self.det.dispersion_element)

    def testcrystal_2d(self):
        self.det.crystal_2d = 8.742
        self.assertAlmostEqual(8.742, self.det.crystal_2d.value, 4)
        self.assertEqual(u'\u00c5', self.det.crystal_2d.unit)

    def testrowland_cricle_diameter(self):
        self.det.rowland_circle_diameter = 140.0
        self.assertAlmostEqual(140.0, self.det.rowland_circle_diameter.value, 4)
        self.assertEqual('mm', self.det.rowland_circle_diameter.unit)
    
    def testpulse_height_analyser(self):
        pha = PulseHeightAnalyser(1700.0, 16, 0.7, 9.3, PHA_MODE_DIFFERENTIAL)
        self.det.pulse_height_analyser = pha
        self.assertAlmostEqual(1700.0, self.det.pulse_height_analyser.bias.value, 4)
        self.assertAlmostEqual(16.0, self.det.pulse_height_analyser.gain, 4)
        self.assertAlmostEqual(0.7, self.det.pulse_height_analyser.base_level.value, 4)
        self.assertAlmostEqual(9.3, self.det.pulse_height_analyser.window.value, 4)
        self.assertEqual(PHA_MODE_DIFFERENTIAL, self.det.pulse_height_analyser.mode)

    def testwindow(self):
        window = Window()
        window.append_layer('Al', 1.0)
        self.det.window = window
        self.assertEqual('Al', self.det.window.layers[0].material)
        self.assertEqual(1.0, self.det.window.layers[0].thickness.value)

class TestDetectorSpectrometerXEDS(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.det = DetectorSpectrometerXEDS(4096, calibration)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testtechnology(self):
        self.det.technology = XEDS_TECHNOLOGY_SILI
        self.assertEqual(XEDS_TECHNOLOGY_SILI, self.det.technology)

        self.assertRaises(ValueError, self.det.set_technology, 'ABC')

    def testnominal_throughput(self):
        self.det.nominal_throughput = 180000
        self.assertAlmostEqual(180000, self.det.nominal_throughput.value, 4)
        self.assertEqual('counts', self.det.nominal_throughput.unit)

    def testtime_constant(self):
        self.det.time_constant = 11.1
        self.assertAlmostEqual(11.1, self.det.time_constant.value, 4)
        self.assertEqual(u'\u00b5s', self.det.time_constant.unit)

    def teststrobe_rate(self):
        self.det.strobe_rate = 2000
        self.assertAlmostEqual(2000, self.det.strobe_rate.value, 4)
        self.assertEqual('Hz', self.det.strobe_rate.unit)

    def testwindow(self):
        window = Window()
        window.append_layer('Al', 1.0)
        self.det.window = window
        self.assertEqual('Al', self.det.window.layers[0].material)
        self.assertEqual(1.0, self.det.window.layers[0].thickness.value)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
