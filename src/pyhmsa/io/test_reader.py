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
import os

# Third party modules.

# Local modules.
from pyhmsa.io.reader import HMSAReader

# Globals and constants variables.

class TestHMSAReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        testdatadir = os.path.join(os.path.dirname(__file__), '..', 'testdata')
        filepath = os.path.join(testdatadir, 'breccia_eds.xml')
        self.reader = HMSAReader(filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testroot(self):
        with self.reader:
            self.assertEqual('1.0', self.reader.version)
            self.assertEqual('en-US', self.reader.language)
            self.assertEqual(b'60606EE485B42736', self.reader.uid)

    def testheader(self):
        with self.reader:
            print(self.reader.conditions)
            print(self.reader.data['EDS sum spectrum'].conditions)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
