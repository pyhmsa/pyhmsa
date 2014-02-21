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
from pyhmsa.fileformat.xmlhandler.datum.imageraster import \
    (ImageRaster2DXMLHandler, ImageRaster2DSpectralXMLHandler,
     ImageRaster2DHyperimageXMLHandler)
from pyhmsa.spec.datum.imageraster import \
    ImageRaster2D, ImageRaster2DSpectral, ImageRaster2DHyperimage

# Globals and constants variables.

class TestImageRaster2DXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'imageraster2d.hmsa')
        self.xml_filepath = os.path.join(testdata, 'imageraster2d.xml')

        buffer = sum(np.indices((5, 5), dtype=np.uint8))
        self.obj = ImageRaster2D(5, 5, np.uint8, buffer)

    def testparse(self):
        obj = self.load(ImageRaster2DXMLHandler, self.hmsa_filepath, 'ImageRaster')

        self.assertEqual(5, obj.x)
        self.assertEqual(5, obj.y)
        self.assertEqual((5, 5), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        self.assertEqual(0, obj[0, 0])
        self.assertEqual(8, obj[-1, -1])

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(ImageRaster2DXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestImageRaster2DSpectral(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'imageraster2dspectral.hmsa')
        self.xml_filepath = os.path.join(testdata, 'imageraster2dspectral.xml')

        buffer = sum(np.indices((5, 6, 7), dtype=np.uint8))
        self.obj = ImageRaster2DSpectral(5, 6, 7, np.uint8, buffer)

    def testparse(self):
        obj = self.load(ImageRaster2DSpectralXMLHandler, self.hmsa_filepath, 'ImageRaster')

        self.assertEqual(5, obj.x)
        self.assertEqual(6, obj.y)
        self.assertEqual(7, obj.channels)
        self.assertEqual((5, 6, 7), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        self.assertEqual(0, obj[0, 0, 0])
        self.assertEqual(15, obj[-1, -1, -1])

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(ImageRaster2DSpectralXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

class TestImageRaster2DHyperimageXMLHandler(BaseTestCaseDatum):

    def setUp(self):
        BaseTestCaseDatum.setUp(self)

        testdata = os.path.join(os.path.dirname(__file__),
                                '..', '..', '..', 'testdata')
        self.hmsa_filepath = os.path.join(testdata, 'imageraster2dhyperimage.hmsa')
        self.xml_filepath = os.path.join(testdata, 'imageraster2dhyperimage.xml')

        buffer = sum(np.indices((5, 6, 7, 8), dtype=np.uint8))
        self.obj = ImageRaster2DHyperimage(5, 6, 7, 8, np.uint8, buffer)

    def testparse(self):
        obj = self.load(ImageRaster2DHyperimageXMLHandler, self.hmsa_filepath, 'ImageRaster')

        self.assertEqual(5, obj.x)
        self.assertEqual(6, obj.y)
        self.assertEqual(7, obj.u)
        self.assertEqual(8, obj.v)
        self.assertEqual((5, 6, 7, 8), obj.shape)
        self.assertEqual(np.uint8, obj.dtype.type)
        self.assertEqual(0, obj[0, 0, 0, 0])
        self.assertEqual(22, obj[-1, -1, -1, -1])

    def testconvert(self):
        xml_filepath, hmsa_filepath = self.save(ImageRaster2DHyperimageXMLHandler, self.obj)

        self.assertTrue(filecmp.cmp(xml_filepath, self.xml_filepath, False))
        self.assertTrue(filecmp.cmp(hmsa_filepath, self.hmsa_filepath, False))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
