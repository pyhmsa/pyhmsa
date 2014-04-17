#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree
from io import StringIO

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler
from pyhmsa.util.parameter import \
    Parameter, NumericalAttribute, TextAttribute, XRayLineAttribute
from pyhmsa.type.language import langstr
from pyhmsa.type.xrayline import xrayline

# Globals and constants variables.
from pyhmsa.type.xrayline import NOTATION_IUPAC, NOTATION_SIEGBAHN

class MockParameter(Parameter):

    value1 = NumericalAttribute('s', True, 'Value1')
    value2 = NumericalAttribute('m', False, 'Value2')
    value3 = TextAttribute(False, 'Value3')
    value4 = XRayLineAttribute(NOTATION_SIEGBAHN, False, 'Value4')

    def __init__(self, value1, value2=None, value3=None, value4=None):
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4

class Test_XMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = _XMLHandler(1.0)
        self.obj = MockParameter(2.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_parse_parameter_value1(self):
        source = StringIO(u'<Mock><Value1 DataType="double" Unit="s">2.0</Value1></Mock>')
        element = etree.parse(source)
        obj = self.h._parse_parameter(element, MockParameter)
        self.assertAlmostEqual(2.0, obj.value1, 2)
        self.assertEqual('s', obj.value1.unit)
        self.assertIsNone(obj.value2)

    def test_parse_parameter_value2(self):
        source = StringIO(u'<Mock><Value1 DataType="double" Unit="s">2.0</Value1><Value2 DataType="double" Unit="nm">4.0</Value2></Mock>')
        element = etree.parse(source)
        obj = self.h._parse_parameter(element, MockParameter)
        self.assertAlmostEqual(4.0, obj.value2, 2)
        self.assertEqual('nm', obj.value2.unit)

    def test_parse_parameter_value3(self):
        source = StringIO(u'<Mock><Value1 DataType="double" Unit="s">2.0</Value1><Value3>ABC</Value3></Mock>')
        element = etree.parse(source)
        obj = self.h._parse_parameter(element, MockParameter)
        self.assertEqual('ABC', obj.value3)

        source = StringIO(u'<Mock><Value1 DataType="double" Unit="s">2.0</Value1><Value3 alt-lang-en-US="abc" alt-lang-ru="def">ABC</Value3></Mock>')
        element = etree.parse(source)
        obj = self.h._parse_parameter(element, MockParameter)
        self.assertEqual('ABC', obj.value3)
        self.assertEqual('abc', obj.value3.alternatives['en-US'])
        self.assertEqual('def', obj.value3.alternatives['ru'])

    def test_parse_parameter_value4(self):
        source = StringIO(u'<Mock><Value1 DataType="double" Unit="s">2.0</Value1><Value4 Notation="IUPAC" alt-Siegbahn="Ma">M5-N6,7</Value4></Mock>')
        element = etree.parse(source)
        obj = self.h._parse_parameter(element, MockParameter)
        self.assertEqual('M5-N6,7', obj.value4)
        self.assertEqual(NOTATION_IUPAC, obj.value4.notation)
        self.assertEqual('Ma', obj.value4.alternative)
        self.assertEqual(NOTATION_SIEGBAHN, obj.value4.alternative.notation)

    def test_convert_parameter_value1(self):
        element = self.h._convert_parameter(self.obj, etree.Element('Mock'))
        self.assertEqual('2.0', element.find('Value1').text)
        self.assertEqual('s', element.find('Value1').get('Unit'))
        self.assertIsNone(element.find('Value2'))

    def test_convert_parameter_value2(self):
        self.obj.value2 = (4.0, 'nm')
        element = self.h._convert_parameter(self.obj, etree.Element('Mock'))
        self.assertEqual('4.0', element.find('Value2').text)
        self.assertEqual('nm', element.find('Value2').get('Unit'))

    def test_convert_parameter_value3(self):
        self.obj.value3 = langstr('ABC', {'en-US': 'abc', 'ru': 'def'})
        element = self.h._convert_parameter(self.obj, etree.Element('Mock'))
        self.assertEqual('ABC', element.find('Value3').text)
        self.assertEqual('abc', element.find('Value3').get('alt-lang-en-US'))
        self.assertEqual('def', element.find('Value3').get('alt-lang-ru'))

    def test_convert_parameter_value4(self):
        self.obj.value4 = xrayline('M5-N6,7', NOTATION_IUPAC, 'Ma')
        element = self.h._convert_parameter(self.obj, etree.Element('Mock'))
        self.assertEqual('M5-N6,7', element.find('Value4').text)
        self.assertEqual('IUPAC', element.find('Value4').get('Notation'))
        self.assertEqual('Ma', element.find('Value4').get('alt-Siegbahn'))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
