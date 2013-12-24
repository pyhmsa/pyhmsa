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
from pyhmsa.type.language import langstr

# Globals and constants variables.

class Testlangstr(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.s1 = langstr('Test1', {'en-US': 'TEST', 'en-CA': 'test'})

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('Test1', self.s1)
        self.assertEqual(2, len(self.s1.alternatives))
        self.assertEqual('TEST', self.s1.alternatives['en-US'])
        self.assertEqual('test', self.s1.alternatives['en-CA'])

        self.assertRaises(ValueError, langstr, 'Test1', {'blah': 'abc'})
        self.assertRaises(ValueError, langstr, 'Test1', {'en-blah': 'abc'})

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
