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
from pyhmsa.core.header import Header
from pyhmsa.io.xmlhandler.header import HeaderXMLHandler
from pyhmsa.type.checksum import Checksum

# Globals and constants variables.

class TestHeaderXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = HeaderXMLHandler(1.0)

        self.obj = Header(title='Beep Beep', author='Wyle E. Coyote',
                          owner='Acme Inc.', date='1985-10-26', time='20:04:00',
                          extra='Blah', checksum=Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD', 'SHA-1'))

        source = StringIO('<Header><Checksum Algorithm="SHA-1">53AAD59C05D59A40AD746D6928EA6D2D526865FD</Checksum><Title>Beep Beep</Title><Author>Wyle E. Coyote</Author><Owner>Acme Inc.</Owner><Date>1985-10-26</Date><Time>20:04:00</Time></Header>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testfrom_xml(self):
        obj = self.h.from_xml(self.element)
        self.assertEqual('53AAD59C05D59A40AD746D6928EA6D2D526865FD', obj.checksum.value)
        self.assertEqual('SHA-1', obj.checksum.algorithm)
        self.assertEqual('Beep Beep', obj.title)
        self.assertEqual('Wyle E. Coyote', obj.author)
        self.assertEqual('Acme Inc.', obj.owner)
        self.assertEqual(1985, obj.date.year)
        self.assertEqual(10, obj.date.month)
        self.assertEqual(26, obj.date.day)
        self.assertEqual(20, obj.time.hour)
        self.assertEqual(4, obj.time.minute)
        self.assertEqual(0, obj.time.second)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testto_xml(self):
        element = self.h.to_xml(self.obj)
        self.assertEqual('Header', element.tag)
        self.assertEqual('53AAD59C05D59A40AD746D6928EA6D2D526865FD', element.find('Checksum').text)
        self.assertEqual('SHA-1', element.find('Checksum').get('Algorithm'))
        self.assertEqual('Beep Beep', element.find('Title').text)
        self.assertEqual('Wyle E. Coyote', element.find('Author').text)
        self.assertEqual('Acme Inc.', element.find('Owner').text)
        self.assertEqual('1985-10-26', element.find('Date').text)
        self.assertEqual('20:04:00', element.find('Time').text)
        self.assertEqual('Blah', element.find('Extra').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
