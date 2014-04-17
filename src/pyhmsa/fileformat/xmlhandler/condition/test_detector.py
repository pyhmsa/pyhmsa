#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.detector import \
    (DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS,
     PulseHeightAnalyser, Window)
from pyhmsa.spec.condition.calibration import CalibrationConstant
from pyhmsa.fileformat.xmlhandler.condition.detector import \
    (WindowXMLHandler,
     DetectorCameraXMLHandler,
     DetectorSpectrometerXMLHandler, DetectorSpectrometerCLXMLHandler,
     DetectorSpectrometerWDSXMLHandler, DetectorSpectrometerXEDSXMLHandler)

# Globals and constants variables.
from pyhmsa.spec.condition.detector import \
    (PHA_MODE_DIFFERENTIAL, SIGNAL_TYPE_ELS, COLLECTION_MODE_PARALLEL,
     XEDS_TECHNOLOGY_SILI)

class TestWindowXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = WindowXMLHandler(1.0)

        self.obj = Window()
        self.obj.append_layer('Al', 1.0)

        source = '<Window><Layer Material="Al" Unit="um" DataType="float">1.</Layer></Window>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(1, len(obj.layers))
        self.assertEqual('Al', obj.layers[0].material)
        self.assertAlmostEqual(1.0, obj.layers[0].thickness, 4)
        self.assertEqual('um', obj.layers[0].thickness.unit, 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Window', element.tag)
        self.assertEqual(1, len(element.findall('Layer')))
        self.assertEqual('Al', element.findall('Layer')[0].get('Material'))
        self.assertEqual('1.0', element.findall('Layer')[0].text)

class TestDetectorCameraXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = DetectorCameraXMLHandler(1.0)

        self.obj = DetectorCamera(512, 400, 200.0, 4.5, 80.0,
                                  SIGNAL_TYPE_ELS, 'Example Inc.', 'Example Model 123',
                                  '12345-abc-67890', 'counts', 45.0, 0.0, 50.0,
                                  20.0, 1.0, 3.4, -20.0)

        source = '<Detector Class="Camera"><SignalType>ELS</SignalType><Manufacturer>Example Inc.</Manufacturer><Model>Example Model 123</Model><SerialNumber>12345-abc-67890</SerialNumber><MeasurementUnit>counts</MeasurementUnit><Elevation Unit="degrees" DataType = "float">45.</Elevation><Azimuth Unit="degrees" DataType = "float">0.</Azimuth><Distance Unit="mm" DataType = "float">50</Distance><Area Unit="mm2" DataType = "float">20</Area><SolidAngle Unit="sr" DataType = "float">1.</SolidAngle><SemiAngle Unit="mrad" DataType = "float">3.4</SemiAngle><Temperature Unit="degreesC" DataType="float">-20.0</Temperature><UPixelCount DataType="uint32">512</UPixelCount><ExposureTime Unit="ms" DataType="float">200.</ExposureTime><Magnification DataType="float">4.5</Magnification><FocalLength Unit="mm" DataType="float">80.</FocalLength><VPixelCount DataType="uint32">400</VPixelCount></Detector>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Detector')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)

        self.assertEqual('Example Inc.', obj.manufacturer)
        self.assertEqual('Example Model 123', obj.model)
        self.assertEqual('12345-abc-67890', obj.serial_number)
        self.assertEqual('counts', obj.measurement_unit)
        self.assertAlmostEqual(45.0, obj.elevation, 4)
        self.assertEqual('degrees', obj.elevation.unit)
        self.assertAlmostEqual(0.0, obj.azimuth, 4)
        self.assertEqual('degrees', obj.azimuth.unit)
        self.assertAlmostEqual(50.0, obj.distance, 4)
        self.assertEqual('mm', obj.distance.unit)
        self.assertAlmostEqual(20.0, obj.area, 4)
        self.assertEqual('mm2', obj.area.unit)
        self.assertAlmostEqual(1.0, obj.solid_angle, 4)
        self.assertEqual('sr', obj.solid_angle.unit)
        self.assertAlmostEqual(3.4, obj.semi_angle, 4)
        self.assertEqual('mrad', obj.semi_angle.unit)
        self.assertAlmostEqual(-20.0, obj.temperature, 4)
        self.assertEqual('degreesC', obj.temperature.unit)

        self.assertEqual(512, obj.pixel_count_u)
        self.assertEqual(400, obj.pixel_count_v)
        self.assertAlmostEqual(200.0, obj.exposure_time, 4)
        self.assertEqual('ms', obj.exposure_time.unit)
        self.assertAlmostEqual(4.5, obj.magnification, 4)
        self.assertAlmostEqual(80.0, obj.focal_length, 4)
        self.assertEqual('mm', obj.focal_length.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Detector', element.tag)
        self.assertEqual('Camera', element.get('Class'))

        self.assertEqual('ELS', element.find('SignalType').text)
        self.assertEqual('Example Inc.', element.find('Manufacturer').text)
        self.assertEqual('Example Model 123', element.find('Model').text)
        self.assertEqual('12345-abc-67890', element.find('SerialNumber').text)
        self.assertEqual('counts', element.find('MeasurementUnit').text)
        self.assertEqual('45.0', element.find('Elevation').text)
        self.assertEqual('0.0', element.find('Azimuth').text)
        self.assertEqual('50.0', element.find('Distance').text)
        self.assertEqual('20.0', element.find('Area').text)
        self.assertEqual('1.0', element.find('SolidAngle').text)
        self.assertEqual('3.4', element.find('SemiAngle').text)
        self.assertEqual('-20.0', element.find('Temperature').text)

        self.assertEqual('512', element.find('UPixelCount').text)
        self.assertEqual('400', element.find('VPixelCount').text)
        self.assertEqual('200.0', element.find('ExposureTime').text)
        self.assertEqual('4.5', element.find('Magnification').text)
        self.assertEqual('80.0', element.find('FocalLength').text)

class TestDetectorSpectrometerXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = DetectorSpectrometerXMLHandler(1.0)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.obj = DetectorSpectrometer(4096, calibration, COLLECTION_MODE_PARALLEL)

        source = '<Detector Class="Spectrometer"><ChannelCount DataType="uint32">4096</ChannelCount><Calibration Class="Constant"><Quantity>Energy</Quantity><Unit>eV</Unit><Value DataType="float">-237.098251</Value></Calibration><CollectionMode>Parallel</CollectionMode></Detector>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Detector')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(4096, obj.channel_count)
        self.assertEqual('Energy', obj.calibration.quantity)
        self.assertEqual('eV', obj.calibration.unit)
        self.assertAlmostEqual(-237.098251, obj.calibration.value, 4)
        self.assertEqual(COLLECTION_MODE_PARALLEL, obj.collection_mode)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Detector', element.tag)
        self.assertEqual('Spectrometer', element.get('Class'))
        self.assertEqual('4096', element.find('ChannelCount').text)
        self.assertEqual(1, len(element.findall('Calibration')))
        self.assertEqual('Energy', element.find('Calibration/Quantity').text)
        self.assertEqual('eV', element.find('Calibration/Unit').text)
        self.assertEqual('-237.098251', element.find('Calibration/Value').text)
        self.assertEqual(COLLECTION_MODE_PARALLEL, element.find('CollectionMode').text)

class TestDetectorSpectrometerCLXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = DetectorSpectrometerCLXMLHandler(1.0)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.obj = DetectorSpectrometerCL(4096, calibration, 800.0)

        source = '<Detector Class="Spectrometer/CL"><ChannelCount DataType="uint32">4096</ChannelCount><Calibration Class="Constant"><Quantity>Energy</Quantity><Unit>eV</Unit><Value DataType="float">-237.098251</Value></Calibration><Grating-d Unit="mm-1" DataType="float">800</Grating-d></Detector>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Detector')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertAlmostEqual(800.0, obj.grating_d, 4)
        self.assertEqual('mm-1', obj.grating_d.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Detector', element.tag)
        self.assertEqual('Spectrometer/CL', element.get('Class'))
        self.assertEqual('800.0', element.find('Grating-d').text)

class TestDetectorSpectrometerWDSXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = DetectorSpectrometerWDSXMLHandler(1.0)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        pha = PulseHeightAnalyser(1750, 32, 0.5, 4.5, PHA_MODE_DIFFERENTIAL)
        self.obj = DetectorSpectrometerWDS(4096, calibration, COLLECTION_MODE_PARALLEL,
                                           'TAP', 8.742, 140.0, pha)
        self.obj.window.append_layer('Al', 1.0)

        source = u'<Detector Class="Spectrometer/WDS"><ChannelCount DataType="uint32">4096</ChannelCount><Calibration Class="Constant"><Quantity>Energy</Quantity><Unit>eV</Unit><Value DataType="float">-237.098251</Value></Calibration><DispersionElement>TAP</DispersionElement><Crystal-2d Unit="\u00c5" DataType="float">8.742</Crystal-2d><RowlandCircleDiameter Unit="mm" DataType="float">140.</RowlandCircleDiameter><PulseHeightAnalyser><Bias Unit="V" DataType="float">1700.</Bias><Gain DataType="float">16.</Gain><BaseLevel Unit="V" DataType="float">0.7</BaseLevel><Window Unit="V" DataType="float">9.3</Window><Mode>Differential</Mode></PulseHeightAnalyser><Window><Layer Material="Al" Unit="um" DataType="float">1.</Layer></Window></Detector>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Detector')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('TAP', obj.dispersion_element)
        self.assertAlmostEqual(8.742, obj.crystal_2d, 4)
        self.assertEqual(u'\u00c5', obj.crystal_2d.unit)
        self.assertAlmostEqual(140.0, obj.rowland_circle_diameter, 4)
        self.assertEqual('mm', obj.rowland_circle_diameter.unit)
        self.assertAlmostEqual(1700, obj.pulse_height_analyser.bias, 4)
        self.assertEqual('V', obj.pulse_height_analyser.bias.unit, 4)
        self.assertAlmostEqual(16, obj.pulse_height_analyser.gain, 4)
        self.assertAlmostEqual(0.7, obj.pulse_height_analyser.base_level, 4)
        self.assertEqual('V', obj.pulse_height_analyser.base_level.unit, 4)
        self.assertAlmostEqual(9.3, obj.pulse_height_analyser.window, 4)
        self.assertEqual('V', obj.pulse_height_analyser.window.unit, 4)
        self.assertEqual(PHA_MODE_DIFFERENTIAL, obj.pulse_height_analyser.mode)
        self.assertEqual(1, len(obj.window.layers))
        self.assertAlmostEqual(1.0, obj.window.layers[0].thickness, 4)
        self.assertEqual('um', obj.window.layers[0].thickness.unit)
        self.assertEqual('Al', obj.window.layers[0].material)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Detector', element.tag)
        self.assertEqual('Spectrometer/WDS', element.get('Class'))
        self.assertEqual('TAP', element.find('DispersionElement').text)
        self.assertEqual('8.742', element.find('Crystal-2d').text)
        self.assertEqual('1750', element.find('PulseHeightAnalyser/Bias').text)
        self.assertEqual('32', element.find('PulseHeightAnalyser/Gain').text)
        self.assertEqual('0.5', element.find('PulseHeightAnalyser/BaseLevel').text)
        self.assertEqual('4.5', element.find('PulseHeightAnalyser/Window').text)
        self.assertEqual(PHA_MODE_DIFFERENTIAL, element.find('PulseHeightAnalyser/Mode').text)
        self.assertEqual('Al', element.find('Window/Layer').get('Material'))
        self.assertEqual('1.0', element.find('Window/Layer').text)

class TestDetectorSpectrometerXEDSXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = DetectorSpectrometerXEDSXMLHandler(1.0)

        calibration = CalibrationConstant('Energy', 'eV', -237.098251)
        self.obj = DetectorSpectrometerXEDS(4096, calibration, COLLECTION_MODE_PARALLEL,
                                            XEDS_TECHNOLOGY_SILI, 180000.0, 11.1, 2000.0)
        self.obj.window.append_layer('Al', 1.0)

        source = '<Detector Class="Spectrometer/XEDS"><ChannelCount DataType="uint32">4096</ChannelCount><Calibration Class="Constant"><Quantity>Energy</Quantity><Unit>eV</Unit><Value DataType="float">-237.098251</Value></Calibration><Technology>SiLi</Technology><NominalThroughput Unit="counts" DataType="float">180000.</NominalThroughput><TimeConstant Unit="us" DataType="float">11.1</TimeConstant><StrobeRate Unit="Hz" DataType="float">2000</StrobeRate><Window><Layer Material="Al" Unit="um" DataType="float">1.</Layer></Window></Detector>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Detector')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(1, len(obj.window.layers))
        self.assertEqual(XEDS_TECHNOLOGY_SILI, obj.technology)
        self.assertAlmostEqual(180000.0, obj.nominal_throughput, 4)
        self.assertEqual('counts', obj.nominal_throughput.unit)
        self.assertAlmostEqual(11.1, obj.time_constant, 4)
        self.assertEqual('us', obj.time_constant.unit)
        self.assertAlmostEqual(2000, obj.strobe_rate, 4)
        self.assertEqual('Hz', obj.strobe_rate.unit)
        self.assertAlmostEqual(1.0, obj.window.layers[0].thickness, 4)
        self.assertEqual('um', obj.window.layers[0].thickness.unit)
        self.assertEqual('Al', obj.window.layers[0].material)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Detector', element.tag)
        self.assertEqual('Spectrometer/XEDS', element.get('Class'))
        self.assertEqual(XEDS_TECHNOLOGY_SILI, element.find('Technology').text)
        self.assertEqual('180000.0', element.find('NominalThroughput').text)
        self.assertEqual('11.1', element.find('TimeConstant').text)
        self.assertEqual('2000.0', element.find('StrobeRate').text)
        self.assertEqual('Al', element.find('Window/Layer').get('Material'))
        self.assertEqual('1.0', element.find('Window/Layer').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
