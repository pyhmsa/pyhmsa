#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.probe import \
    ProbeEMXMLHandler, ProbeTEMXMLHandler
from pyhmsa.spec.condition.probe import ProbeEM, ProbeTEM

# Globals and constants variables.
from pyhmsa.spec.condition.probe import GUN_TYPE_LAB6, LENS_MODE_IMAGE

class TestProbeEMXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ProbeEMXMLHandler(1.0)

        self.obj = ProbeEM(15.0, 47.59, GUN_TYPE_LAB6, 12345.0, 1.234, 4200.0,
                           12345.0, 3.14e-6, 3.14e-10, 2500.0, 10.0)

        source = '<Probe Class="EM"><BeamVoltage DataType="float" Unit="kV">15.</BeamVoltage><BeamCurrent DataType="float" Unit="nA">47.59</BeamCurrent><GunType>LaB6</GunType><EmissionCurrent DataType="float" Unit="uA">12345</EmissionCurrent><FilamentCurrent DataType="float" Unit="A">1.234</FilamentCurrent><ExtractorBias DataType="float" Unit="V">4200</ExtractorBias><BeamDiameter DataType="float" Unit="nm">12345</BeamDiameter><ChamberPressure DataType="float" Unit="Pa">3.14E-6</ChamberPressure><GunPressure DataType="float" Unit="Pa">3.14E-10</GunPressure><ScanMagnification DataType="float">2500.</ScanMagnification><WorkingDistance DataType="float" Unit="mm">10</WorkingDistance></Probe>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Probe')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertAlmostEqual(15.0, obj.beam_voltage, 4)
        self.assertEqual('kV', obj.beam_voltage.unit)
        self.assertAlmostEqual(47.59, obj.beam_current, 4)
        self.assertEqual('nA', obj.beam_current.unit)
        self.assertEqual(GUN_TYPE_LAB6, obj.gun_type)
        self.assertAlmostEqual(12345.0, obj.emission_current, 4)
        self.assertEqual('uA', obj.emission_current.unit)
        self.assertAlmostEqual(1.234, obj.filament_current, 4)
        self.assertEqual('A', obj.filament_current.unit)
        self.assertAlmostEqual(4200.0, obj.extractor_bias, 4)
        self.assertEqual('V', obj.extractor_bias.unit)
        self.assertAlmostEqual(12345.0, obj.beam_diameter, 4)
        self.assertEqual('nm', obj.beam_diameter.unit)
        self.assertAlmostEqual(3.14e-6, obj.chamber_pressure, 10)
        self.assertEqual('Pa', obj.chamber_pressure.unit)
        self.assertAlmostEqual(3.14e-10, obj.gun_pressure, 14)
        self.assertEqual('Pa', obj.gun_pressure.unit)
        self.assertAlmostEqual(2500.0, obj.scan_magnification, 4)
        self.assertAlmostEqual(10.0, obj.working_distance, 4)
        self.assertEqual('mm', obj.working_distance.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Probe', element.tag)
        self.assertEqual('EM', element.get('Class'))
        self.assertEqual('15.0', element.find('BeamVoltage').text)
        self.assertEqual('47.59', element.find('BeamCurrent').text)
        self.assertEqual(GUN_TYPE_LAB6, element.find('GunType').text)
        self.assertEqual('12345.0', element.find('EmissionCurrent').text)
        self.assertEqual('1.234', element.find('FilamentCurrent').text)
        self.assertEqual('4200.0', element.find('ExtractorBias').text)
        self.assertEqual('12345.0', element.find('BeamDiameter').text)
        self.assertEqual('3.14e-06', element.find('ChamberPressure').text)
        self.assertEqual('3.14e-10', element.find('GunPressure').text)
        self.assertEqual('2500.0', element.find('ScanMagnification').text)
        self.assertEqual('10.0', element.find('WorkingDistance').text)

class TestProbeTEMXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ProbeTEMXMLHandler(1.0)

        self.obj = ProbeTEM(15.0, LENS_MODE_IMAGE,
                            camera_magnification=2.0, convergence_angle=1.5)

        source = '<Probe Class="TEM"><BeamVoltage DataType="float" Unit="kV">15.</BeamVoltage><LensMode>IMAGE</LensMode><CameraMagnification DataType="float">2</CameraMagnification><ConvergenceAngle Unit = "mrad" DataType="float">1.5</ConvergenceAngle></Probe>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Probe')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(LENS_MODE_IMAGE, obj.lens_mode)
        self.assertAlmostEqual(2.0, obj.camera_magnification, 4)
        self.assertAlmostEqual(1.5, obj.convergence_angle, 4)
        self.assertEqual('mrad', obj.convergence_angle.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Probe', element.tag)
        self.assertEqual('TEM', element.get('Class'))
        self.assertEqual(LENS_MODE_IMAGE, element.find('LensMode').text)
        self.assertEqual('2.0', element.find('CameraMagnification').text)
        self.assertEqual('1.5', element.find('ConvergenceAngle').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
