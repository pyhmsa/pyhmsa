#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.elementalid import \
    ElementalIDXMLHandler, ElementalIDXrayXMLHandler
from pyhmsa.spec.condition.elementalid import ElementalID, ElementalIDXray

# Globals and constants variables.

class TestElementalIDXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ElementalIDXMLHandler(1.0)

        self.obj = ElementalID(11)

        source = u'<ElementalID><Element DataType="uint32" Symbol="Na">11</Element></ElementalID>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(11, obj.atomic_number)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('ElementalID', element.tag)
        self.assertEqual('11', element.find('Element').text)
        self.assertEqual('Na', element.find('Element').get('Symbol'))

class TestElementalIDXrayXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = ElementalIDXrayXMLHandler(1.0)

        self.obj = ElementalIDXray(11, u'M\u03b1', 1234.0)

        source = u'<ElementalID Class="X-ray"><Element DataType="uint32" Symbol="Na">11</Element><Line>M\u03b1</Line><Energy Unit="eV" DataType="float">1234</Energy></ElementalID>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('ElementalID')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(11, obj.atomic_number)
        self.assertEqual('Ma', obj.line)
        self.assertAlmostEqual(1234.0, obj.energy, 4)
        self.assertEqual('eV', obj.energy.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('ElementalID', element.tag)
        self.assertEqual('X-ray', element.get('Class'))
        self.assertEqual('11', element.find('Element').text)
        self.assertEqual('Na', element.find('Element').get('Symbol'))
        self.assertEqual('Ma', element.find('Line').text)
        self.assertEqual('1234.0', element.find('Energy').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
