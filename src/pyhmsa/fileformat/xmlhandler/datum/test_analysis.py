#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import filecmp

# Third party modules.
import numpy as np
from PIL import Image

# Local modules.
from pyhmsa.fileformat.xmlhandler.datum.test_datum import BaseTestCaseDatum
from pyhmsa.fileformat.xmlhandler.datum.analysis import \
    Analysis0DXMLHandler, Analysis1DXMLHandler, Analysis2DXMLHandler
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D

# Globals and constants variables.

class TestAnalysis0DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysis0d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysis0d.xml')

        self.obj = Analysis0D(123, np.int64)

    def testparse(self):
        obj = self.load(Analysis0DXMLHandler, self.hmsa_filepath, 'Analysis')

        self.assertEqual((), obj.shape)
        self.assertEqual(np.int64, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(Analysis0DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestAnalysis1DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysis1d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysis1d.xml')

        with open(self.hmsa_filepath, 'rb') as fp:
            fp.seek(8)
            buffer = np.fromfile(fp, np.int64)
        self.obj = Analysis1D(4096, np.int64, buffer)

    def testparse(self):
        obj = self.load(Analysis1DXMLHandler, self.hmsa_filepath, 'Analysis')

        self.assertEqual(4096, len(obj))
        self.assertEqual((4096,), obj.shape)
        self.assertEqual(np.int64, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(Analysis1DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestAnalysis2DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysis2d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysis2d.xml')

        with open(os.path.join(testdata, 'diffraction_pattern.png'), 'rb') as fp:
            im = Image.open(fp)
            self.obj = Analysis2D(220, 220, np.uint8, np.array(im))

    def testparse(self):
        obj = self.load(Analysis2DXMLHandler, self.hmsa_filepath, 'Analysis')

        self.assertEqual(220, len(obj))
        self.assertEqual((220, 220), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(Analysis2DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
