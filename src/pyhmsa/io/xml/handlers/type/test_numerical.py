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
import xml.etree.ElementTree as etree

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.numerical import NumericalValue
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class TestNumericalXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = NumericalXMLHandler()

        self.obj1 = NumericalValue(np.float32(9.0), 'm')

        self.obj2 = np.uint8(45)

        self.obj3 = np.array([4, 3, 2], dtype=np.int32)

        self.element1 = etree.Element('NumericalValue')
        self.element1.attrib['Unit'] = 'm'
        self.element1.attrib['DataType'] = 'float'
        self.element1.text = str(9.0)

        self.element2 = etree.Element('NumericalValue')
        self.element2.attrib['DataType'] = 'byte'
        self.element2.text = str(45)

        self.element3 = etree.Element('NumericalValue')
        self.element3.attrib['DataType'] = 'array:int32'
        self.element3.attrib['Count'] = str(3)
        self.element3.text = '4,3,2'

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element1))
        self.assertTrue(self.h.can_parse(self.element2))
        self.assertTrue(self.h.can_parse(self.element3))
        self.assertFalse(self.h.can_parse(etree.Element('NumericalValue')))

    def testfrom_xml(self):
        obj1 = self.h.from_xml(self.element1)
        self.assertAlmostEqual(9.0, obj1.value, 4)
        self.assertIs(np.float32, obj1.value.dtype.type)
        self.assertEqual('m', obj1.unit)

        obj2 = self.h.from_xml(self.element2)
        self.assertEqual(45, obj2, 4)
        self.assertIs(np.uint8, obj2.dtype.type)

        obj3 = self.h.from_xml(self.element3)
        self.assertEqual(3, len(obj3))
        self.assertEqual(4, obj3[0], 4)
        self.assertEqual(3, obj3[1], 4)
        self.assertEqual(2, obj3[2], 4)
        self.assertIs(np.int32, obj3.dtype.type)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj1))
        self.assertTrue(self.h.can_convert(self.obj2))
        self.assertTrue(self.h.can_convert(self.obj3))
        self.assertFalse(self.h.can_convert(object()))

    def testto_xml(self):
        element1 = self.h.to_xml(self.obj1)
        self.assertEqual('9.0', element1.text)
        self.assertEqual('m', element1.attrib['Unit'])
        self.assertEqual('float', element1.attrib['DataType'])

        element2 = self.h.to_xml(self.obj2)
        self.assertEqual('45', element2.text)
        self.assertEqual('byte', element2.attrib['DataType'])

        element3 = self.h.to_xml(self.obj3)
        self.assertEqual('4,3,2', element3.text)
        self.assertEqual('array:int32', element3.attrib['DataType'])
        self.assertEqual('3', element3.attrib['Count'])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
