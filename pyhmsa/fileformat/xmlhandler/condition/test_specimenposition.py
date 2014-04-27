#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.specimenposition import SpecimenPositionXMLHandler
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.

class TestSpecimenPositionXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = SpecimenPositionXMLHandler(1.0)

        self.obj = SpecimenPosition(0.0, 0.0, 10.0, 90.0, 70.0)

        source = '<SpecimenPosition><X Unit="mm" DataType="float">0.0</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z><R Unit="degrees" DataType="float">90.0</R><T Unit="degrees" DataType="float">70.0</T></SpecimenPosition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertAlmostEqual(0.0, obj.x, 4)
        self.assertEqual('mm', obj.x.unit)
        self.assertAlmostEqual(0.0, obj.y, 4)
        self.assertEqual('mm', obj.y.unit)
        self.assertAlmostEqual(10.0, obj.z, 4)
        self.assertEqual('mm', obj.z.unit)
        self.assertAlmostEqual(90.0, obj.r, 4)
        self.assertEqual('degrees', obj.r.unit)
        self.assertAlmostEqual(70.0, obj.t, 4)
        self.assertEqual('degrees', obj.t.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('SpecimenPosition', element.tag)
        self.assertEqual('0.0', element.find('X').text)
        self.assertEqual('0.0', element.find('Y').text)
        self.assertEqual('10.0', element.find('Z').text)
        self.assertEqual('90.0', element.find('R').text)
        self.assertEqual('70.0', element.find('T').text)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
