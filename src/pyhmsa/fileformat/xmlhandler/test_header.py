#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.header import Header
from pyhmsa.fileformat.xmlhandler.header import HeaderXMLHandler
from pyhmsa.type.checksum import Checksum

# Globals and constants variables.

class TestHeaderXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = HeaderXMLHandler(1.0)

        self.obj = Header(title='Beep Beep', author='Wyle E. Coyote',
                          owner='Acme Inc.', date='1985-10-26', time='20:04:00',
                          extra='Blah', checksum=Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD', 'SHA-1'))

        source = u'<Header><Checksum Algorithm="SHA-1">53AAD59C05D59A40AD746D6928EA6D2D526865FD</Checksum><Title>Beep Beep</Title><Author>Wyle E. Coyote</Author><Owner>Acme Inc.</Owner><Date>1985-10-26</Date><Time>20:04:00</Time></Header>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
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

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Header', element.tag)
        self.assertIsNone(element.find('Checksum')) # Checksum not saved
        self.assertEqual('Beep Beep', element.find('Title').text)
        self.assertEqual('Wyle E. Coyote', element.find('Author').text)
        self.assertEqual('Acme Inc.', element.find('Owner').text)
        self.assertEqual('1985-10-26', element.find('Date').text)
        self.assertEqual('20:04:00', element.find('Time').text)
        self.assertEqual('Blah', element.find('extra').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
