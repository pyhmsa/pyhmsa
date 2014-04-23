#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os

# Third party modules.
import numpy as np
from PIL import Image

# Local modules.
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class TestAnalysis0D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = Analysis0D(4.0)
        self.datum.conditions['Test'] = _Condition()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertAlmostEqual(4.0, self.datum, 4)
        self.assertEqual(1, len(self.datum.conditions))

class TestAnalysis1D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = Analysis1D(5)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0] = 5.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(1, len(self.datum.conditions))
        self.assertEqual(5, self.datum.channels)
        self.assertAlmostEqual(5.0, self.datum[0], 4)
        self.assertAlmostEqual(0.0, self.datum[1], 4)
        self.assertAlmostEqual(0.0, self.datum[2], 4)
        self.assertAlmostEqual(0.0, self.datum[3], 4)
        self.assertAlmostEqual(0.0, self.datum[4], 4)

        self.assertEqual(5, self.datum.datum_dimensions['Channel'])

        datum = np.arange(5.0).view(Analysis1D)
        self.assertAlmostEqual(3.0, datum[3], 4)
        self.assertEqual(0, len(datum.conditions))
        self.assertEqual(5, datum.channels)

        datum = datum[:3]
        self.assertEqual(3, datum.channels)

    def testget_xy(self):
        xy = self.datum.get_xy()
        print(xy)

class TestAnalysis2D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata')
        self.im = Image.open(os.path.join(testdata, 'diffraction_pattern.png'))
        self.datum = Analysis2D(220, 220, np.uint8, np.array(self.im))
        self.datum.conditions['Test'] = _Condition()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(220, self.datum.u)
        self.assertEqual(220, self.datum.v)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertEqual(147, self.datum[0, 0])
        self.assertEqual(218, self.datum[-1, -1])

        self.assertEqual(220, self.datum.datum_dimensions['U'])
        self.assertEqual(220, self.datum.datum_dimensions['V'])

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
