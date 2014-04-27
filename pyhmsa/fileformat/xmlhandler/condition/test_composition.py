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
from pyhmsa.fileformat.xmlhandler.condition.composition import CompositionElementalXMLHandler
from pyhmsa.spec.condition.composition import CompositionElemental

# Globals and constants variables.

class TestCompositionXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CompositionElementalXMLHandler(1.0)

        self.obj = CompositionElemental('atoms')
        self.obj[11] = 3
        self.obj[13] = 1
        self.obj[9] = 6

        source = u'<Composition Class="Elemental"><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="atoms" DataType="float">1.</Element><Element Z="9" Unit="atoms" DataType="float">6.</Element></Composition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('atoms', obj.unit)
        self.assertEqual(3, len(obj))
        self.assertAlmostEqual(3.0, obj[11], 4)
        self.assertAlmostEqual(1.0, obj[13], 4)
        self.assertAlmostEqual(6.0, obj[9], 4)

        source = u'<Composition></Composition>'
        element = etree.fromstring(source.encode('utf-8'))
        obj = self.h.parse(element)
        self.assertIsNone(obj)

        source = u'<Composition><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="wt%" DataType="float">1.</Element></Composition>'
        element = etree.fromstring(source.encode('utf-8'))
        self.assertRaises(ValueError, self.h.parse, element)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Composition', element.tag)
        self.assertEqual(3, len(element.findall('Element')))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
