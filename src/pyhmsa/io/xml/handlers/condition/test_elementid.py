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
from io import StringIO

# Third party modules.

# Local modules.
from pyhmsa.io.xml.handlers.condition.elementid import \
    ElementIDXMLHandler, ElementIDXrayXMLHandler
from pyhmsa.core.condition.elementid import ElementID, ElementIDXray

# Globals and constants variables.

class TestElementIDXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ElementIDXMLHandler()

        self.obj = ElementID(11)

        source = StringIO('<ElementID><Element DataType="uint32" Symbol="Na">11</Element></ElementID>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testfrom_xml(self):
        obj = self.h.from_xml(self.element)
        self.assertEqual(11, obj.z)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testto_xml(self):
        element = self.h.to_xml(self.obj)
        self.assertEqual('ElementID', element.tag)
        self.assertEqual('11', element.find('Element').text)

class TestElementIDXrayXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ElementIDXrayXMLHandler()

        self.obj = ElementIDXray(11, u'M\u03b1', 1234.0)

        source = StringIO('<ElementID Class="X-ray"><Element DataType="uint32" Symbol="Na">11</Element><Line>M\u03b1</Line><Energy Unit="eV" DataType="float">1234</Energy></ElementID>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('ElementID')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testfrom_xml(self):
        obj = self.h.from_xml(self.element)
        self.assertEqual(u'M\u03b1', obj.line)
        self.assertAlmostEqual(1234.0, obj.energy.value, 4)
        self.assertEqual('eV', obj.energy.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testto_xml(self):
        element = self.h.to_xml(self.obj)
        self.assertEqual('ElementID', element.tag)
        self.assertEqual(u'M\u03b1', element.find('Line').text)
        self.assertEqual('1234.0', element.find('Energy').text)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
