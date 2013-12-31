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
from pyhmsa.io.xmlhandler.condition.instrument import InstrumentXMLHandler
from pyhmsa.spec.condition.instrument import Instrument

# Globals and constants variables.

class TestInstrumentXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = InstrumentXMLHandler(1.0)

        self.obj = Instrument('Example Inc.', 'Example Model 123',
                              '12345-abc-67890')

        source = StringIO('<Instrument><Manufacturer>Example Inc.</Manufacturer><Model>Example Model 123</Model><SerialNumber>12345-abc-67890</SerialNumber></Instrument>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Example Inc.', obj.manufacturer)
        self.assertEqual('Example Model 123', obj.model)
        self.assertEqual('12345-abc-67890', obj.serial_number)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Instrument', element.tag)
        self.assertEqual('Example Inc.', element.find('Manufacturer').text)
        self.assertEqual('Example Model 123', element.find('Model').text)
        self.assertEqual('12345-abc-67890', element.find('SerialNumber').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
