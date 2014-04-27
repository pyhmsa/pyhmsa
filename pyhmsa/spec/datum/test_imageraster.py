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

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.imageraster import \
    ImageRaster2D, ImageRaster2DSpectral, ImageRaster2DHyperimage
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class TestImageRaster2D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = ImageRaster2D(5, 5)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0, 0] = 5.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(5, self.datum.x)
        self.assertEqual(5, self.datum.y)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(5.0, self.datum[0, 0], 4)

        self.assertEqual(5, self.datum.collection_dimensions['X'])
        self.assertEqual(5, self.datum.collection_dimensions['Y'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0, 0)
        self.assertAlmostEqual(5.0, analysis, 4)
        self.assertEqual(1, len(analysis.conditions))

class TestImageRaster2DSpectral(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = ImageRaster2DSpectral(5, 5, 3)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0, 0] = [5.0, 4.0, 3.0]

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(5, self.datum.x)
        self.assertEqual(5, self.datum.y)
        self.assertEqual(3, self.datum.channels)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(5.0, self.datum[0, 0, 0], 4)
        self.assertAlmostEqual(4.0, self.datum[0, 0, 1], 4)
        self.assertAlmostEqual(3.0, self.datum[0, 0, 2], 4)

        self.assertEqual(5, self.datum.collection_dimensions['X'])
        self.assertEqual(5, self.datum.collection_dimensions['Y'])
        self.assertEqual(3, self.datum.datum_dimensions['Channel'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0, 0)
        self.assertAlmostEqual(5.0, analysis[0], 4)
        self.assertAlmostEqual(4.0, analysis[1], 4)
        self.assertAlmostEqual(3.0, analysis[2], 4)
        self.assertEqual(3, analysis.channels)
        self.assertEqual(1, len(analysis.conditions))

class TestImageRaster2DHyperimage(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = ImageRaster2DHyperimage(5, 5, 3, 3)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0, 0] = np.ones((3, 3))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(5, self.datum.x)
        self.assertEqual(5, self.datum.y)
        self.assertEqual(3, self.datum.u)
        self.assertEqual(3, self.datum.v)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(1.0, self.datum[0, 0, 0, 0], 4)

        self.assertEqual(5, self.datum.collection_dimensions['X'])
        self.assertEqual(5, self.datum.collection_dimensions['Y'])
        self.assertEqual(3, self.datum.datum_dimensions['U'])
        self.assertEqual(3, self.datum.datum_dimensions['V'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0, 0)
        self.assertAlmostEqual(1.0, analysis[0, 0], 4)
        self.assertEqual(3, analysis.u)
        self.assertEqual(3, analysis.v)
        self.assertEqual(1, len(analysis.conditions))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
