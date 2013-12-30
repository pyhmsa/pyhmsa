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
import numpy as np

# Local modules.
from pyhmsa.spec.datum.analysis import Analysis1D

# Globals and constants variables.

class TestAnalysis1D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = Analysis1D(50)
        self.datum[0] = 5.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(5.0, self.datum[0], 4)
        self.assertEqual(0, len(self.datum.conditions))
        self.assertEqual(50, self.datum.channel)

        datum = np.arange(5.0).view(Analysis1D)
        self.assertAlmostEqual(3.0, datum[3], 4)
        self.assertEqual(0, len(datum.conditions))
        self.assertEqual(5, datum.channel)

        datum = datum[:3]
        self.assertEqual(3, datum.channel)


if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
