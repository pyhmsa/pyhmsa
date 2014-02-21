#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.region import RegionOfInterestXMLHandler
from pyhmsa.spec.condition.region import RegionOfInterest

# Globals and constants variables.

class TestRegionOfInterestXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = RegionOfInterestXMLHandler(1.0)

        self.obj = RegionOfInterest(556, 636)

        source = u'<RegionOfInterest><StartChannel DataType="uint32">556</StartChannel><EndChannel DataType="uint32">636</EndChannel></RegionOfInterest>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(556, obj.start_channel)
        self.assertEqual(636, obj.end_channel)

        source = u'<RegionOfInterest><EndChannel DataType="uint32">636</EndChannel></RegionOfInterest>'
        element = etree.fromstring(source.encode('utf-8'))
        self.assertRaises(ValueError, self.h.parse, element)

        source = u'<RegionOfInterest><StartChannel DataType="uint32">556</StartChannel></RegionOfInterest>'
        element = etree.fromstring(source.encode('utf-8'))
        self.assertRaises(ValueError, self.h.parse, element)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('RegionOfInterest', element.tag)
        self.assertEqual('556', element.find('StartChannel').text)
        self.assertEqual('636', element.find('EndChannel').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
