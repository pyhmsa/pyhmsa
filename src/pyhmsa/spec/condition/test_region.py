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
from pyhmsa.spec.condition.region import RegionOfInterest

# Globals and constants variables.

class TestRegionOfInterest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.roi = RegionOfInterest(556, 636)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(556, self.roi.start_channel)
        self.assertEqual(636, self.roi.end_channel)

    def testset_channels(self):
        self.assertRaises(ValueError, self.roi.set_channels, None, 636)
        self.assertRaises(ValueError, self.roi.set_channels, 556, None)
        self.assertRaises(ValueError, self.roi.set_channels, -1, 636)
        self.assertRaises(ValueError, self.roi.set_channels, 636, 556)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
