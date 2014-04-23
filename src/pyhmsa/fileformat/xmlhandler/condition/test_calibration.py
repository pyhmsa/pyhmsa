#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.calibration import \
    (CalibrationConstant, CalibrationLinear,
     CalibrationPolynomial, CalibrationExplicit)
from pyhmsa.fileformat.xmlhandler.condition.calibration import \
    (CalibrationConstantXMLHandler, CalibrationLinearXMLHandler,
     CalibrationPolynomialXMLHandler, CalibrationExplicitXMLHandler)

# Globals and constants variables.

class TestCalibrationConstantXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CalibrationConstantXMLHandler(1.0)

        self.obj = CalibrationConstant('Energy', 'eV', -237.098251)

        source = u'<Calibration Class="Constant"><Quantity>Energy</Quantity><Unit>eV</Unit><Value DataType="float">-237.098251</Value></Calibration>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Calibration')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Energy', obj.quantity)
        self.assertEqual('eV', obj.unit)
        self.assertAlmostEqual(-237.098251, obj.value, 6)
        self.assertAlmostEqual(-237.098251, obj(0), 4)
        self.assertAlmostEqual(-237.098251, obj(1), 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Calibration', element.tag)
        self.assertEqual('Constant', element.get('Class'))
        self.assertEqual('Energy', element.find('Quantity').text)
        self.assertEqual('eV', element.find('Unit').text)
        self.assertEqual('-237.098251', element.find('Value').text)

class TestCalibrationLinearXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CalibrationLinearXMLHandler(1.0)

        self.obj = CalibrationLinear('Energy', 'eV', 2.49985, -237.098251)

        source = u'<Calibration Class="Linear"><Quantity>Energy</Quantity><Unit>eV</Unit><Gain DataType="float">2.49985</Gain><Offset DataType="float">-237.098251</Offset></Calibration>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Calibration')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Energy', obj.quantity)
        self.assertEqual('eV', obj.unit)
        self.assertAlmostEqual(2.49985, obj.gain, 6)
        self.assertAlmostEqual(-237.098251, obj.offset, 6)
        self.assertAlmostEqual(-237.098251, obj(0), 4)
        self.assertAlmostEqual(-237.098251 + 2.49985, obj(1), 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Calibration', element.tag)
        self.assertEqual('Linear', element.get('Class'))
        self.assertEqual('Energy', element.find('Quantity').text)
        self.assertEqual('eV', element.find('Unit').text)
        self.assertEqual('2.49985', element.find('Gain').text)
        self.assertEqual('-237.098251', element.find('Offset').text)

class TestCalibrationPolynomialXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CalibrationPolynomialXMLHandler(1.0)

        self.obj = CalibrationPolynomial('Energy', 'eV', (-2.225, 0.677, 0.134, -0.018))

        source = u'<Calibration Class="Polynomial"><Quantity>Energy</Quantity><Unit>eV</Unit><Coefficients DataType="array:float" Count="4">-2.225, 0.677, 0.134, -0.018</Coefficients></Calibration>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Calibration')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Energy', obj.quantity)
        self.assertEqual('eV', obj.unit)
        self.assertEqual(4, len(obj.coefficients))
        self.assertAlmostEqual(-2.225, obj.coefficients[0], 4)
        self.assertAlmostEqual(0.677, obj.coefficients[1], 4)
        self.assertAlmostEqual(0.134, obj.coefficients[2], 4)
        self.assertAlmostEqual(-0.018, obj.coefficients[3], 4)
        self.assertAlmostEqual(-0.018, obj(0), 4)
        self.assertAlmostEqual(-1.432, obj(1), 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Calibration', element.tag)
        self.assertEqual('Polynomial', element.get('Class'))
        self.assertEqual('Energy', element.find('Quantity').text)
        self.assertEqual('eV', element.find('Unit').text)
        self.assertEqual('-2.225,0.677,0.134,-0.018', element.find('Coefficients').text)
        self.assertEqual('4', element.find('Coefficients').get('Count'))

class TestCalibrationExplicitXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CalibrationExplicitXMLHandler(1.0)

        self.obj = CalibrationExplicit('Energy', 'eV', (-2.225, 0.677, 0.134, -0.018))

        source = u'<Calibration Class="Explicit"><Quantity>Energy</Quantity><Unit>eV</Unit><Values DataType="array:float" Count="4">-2.225, 0.677, 0.134, -0.018</Values></Calibration>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Calibration')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Energy', obj.quantity)
        self.assertEqual('eV', obj.unit)
        self.assertEqual(4, len(obj.values))
        self.assertAlmostEqual(-2.225, obj.values[0], 4)
        self.assertAlmostEqual(0.677, obj.values[1], 4)
        self.assertAlmostEqual(0.134, obj.values[2], 4)
        self.assertAlmostEqual(-0.018, obj.values[3], 4)
        self.assertAlmostEqual(-2.225, obj(0), 4)
        self.assertAlmostEqual(0.677, obj(1), 4)
        self.assertAlmostEqual(0.134, obj(2), 4)
        self.assertAlmostEqual(-0.018, obj(3), 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Calibration', element.tag)
        self.assertEqual('Explicit', element.get('Class'))
        self.assertEqual('Energy', element.find('Quantity').text)
        self.assertEqual('eV', element.find('Unit').text)
        self.assertEqual('-2.225,0.677,0.134,-0.018', element.find('Values').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
