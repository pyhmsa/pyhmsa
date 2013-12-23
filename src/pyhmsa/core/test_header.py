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

# Third party modules.

# Local modules.
from pyhmsa.core.header import Header
from pyhmsa.type.checksum import Checksum

# Globals and constants variables.

class TestHeader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.header = Header()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testtitle(self):
        self.header.title = 'Beep beep'
        self.assertEqual('Beep beep', self.header.title)
        self.assertEqual('Beep beep', self.header['Title'])

        self.header['title'] = 'test2'
        self.assertEqual('test2', self.header.title)

    def testauthor(self):
        self.header.author = 'Wyle E. Coyote'
        self.assertEqual('Wyle E. Coyote', self.header.author)
        self.assertEqual('Wyle E. Coyote', self.header['Author'])

        self.header['author'] = 'test2'
        self.assertEqual('test2', self.header.author)

    def testowner(self):
        self.header.owner = 'Acme Inc.'
        self.assertEqual('Acme Inc.', self.header.owner)
        self.assertEqual('Acme Inc.', self.header['Owner'])

        self.header['owner'] = 'test2'
        self.assertEqual('test2', self.header.owner)

    def testdate(self):
        self.header.date = '1985-10-26'
        self.assertEqual(1985, self.header.date.year)
        self.assertEqual(10, self.header.date.month)
        self.assertEqual(26, self.header.date.day)

        self.header['date'] = '2013-12-22'
        self.assertEqual(2013, self.header.date.year)
        self.assertEqual(12, self.header.date.month)
        self.assertEqual(22, self.header.date.day)

    def testtime(self):
        self.header.time = '20:04:00'
        self.assertEqual(20, self.header.time.hour)
        self.assertEqual(4, self.header.time.minute)
        self.assertEqual(0, self.header.time.second)

        self.header['time'] = '13:01:04'
        self.assertEqual(13, self.header.time.hour)
        self.assertEqual(1, self.header.time.minute)
        self.assertEqual(4, self.header.time.second)

    def testtimezone(self):
        self.header.timezone = 'US/Eastern'
        self.assertEqual('US/Eastern', str(self.header.timezone))
    
    def testchecksum(self):
        checksum = Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD', 'SHA-1')
        self.header.checksum = checksum
        self.assertEqual('53AAD59C05D59A40AD746D6928EA6D2D526865FD', self.header.checksum.value)
        self.assertRaises(ValueError, self.header.set_checksum, '53AAD59C05D59A40AD746D6928EA6D2D526865FD')

    def test__setitem__(self):
        self.header['Test'] = 'Abc'
        self.assertEqual('Abc', self.header['Test'])

        self.header['Test'] = None
        self.assertNotIn('Test', self.header)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
