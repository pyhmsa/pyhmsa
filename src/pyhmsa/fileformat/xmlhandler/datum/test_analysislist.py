#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import filecmp

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.xmlhandler.datum.test_datum import BaseTestCaseDatum
from pyhmsa.fileformat.xmlhandler.datum.analysislist import \
    AnalysisList0DXMLHandler, AnalysisList1DXMLHandler, AnalysisList2DXMLHandler
from pyhmsa.spec.datum.analysislist import AnalysisList0D, AnalysisList1D, AnalysisList2D

# Globals and constants variables.

class TestAnalysisList0DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysislist0d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysislist0d.xml')

        buffer = np.indices((5,), np.uint8)
        self.obj = AnalysisList0D(5, np.uint8, buffer)

    def testparse(self):
        obj = self.load(AnalysisList0DXMLHandler, self.hmsa_filepath, 'AnalysisList')

        self.assertEqual(5, obj.analysis_count)
        self.assertEqual((5, 1), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(AnalysisList0DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestAnalysisList1DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysislist1d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysislist1d.xml')

        buffer = np.indices((5, 7), np.uint8)
        self.obj = AnalysisList1D(5, 7, np.uint8, buffer)

    def testparse(self):
        obj = self.load(AnalysisList1DXMLHandler, self.hmsa_filepath, 'AnalysisList')

        self.assertEqual(5, obj.analysis_count)
        self.assertEqual(7, obj.channels)
        self.assertEqual((5, 7), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(AnalysisList1DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestAnalysisList2DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'analysislist2d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'analysislist2d.xml')

        buffer = np.indices((5, 6, 7), np.uint8)
        self.obj = AnalysisList2D(5, 6, 7, np.uint8, buffer)

    def testparse(self):
        obj = self.load(AnalysisList2DXMLHandler, self.hmsa_filepath, 'AnalysisList')

        self.assertEqual(5, obj.analysis_count)
        self.assertEqual(6, obj.u)
        self.assertEqual(7, obj.v)
        self.assertEqual((5, 6, 7), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        np.testing.assert_array_equal(obj, self.obj)

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(AnalysisList2DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
