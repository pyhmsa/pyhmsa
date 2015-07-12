""" """

# Standard library modules.
import unittest
import logging

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.imageraster import \
    ImageRaster2D, ImageRaster2DSpectral, ImageRaster2DHyperimage, stitch
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.spec.condition.acquisition import AcquisitionRasterXY
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import \
    POSITION_LOCATION_CENTER, POSITION_LOCATION_START, POSITION_LOCATION_END

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def teststitch1(self):
        acq = AcquisitionRasterXY(7, 7, 1e3, 1e3)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(6.0, 6.0, 0.0)
        datum0 = ImageRaster2D(7, 7)
        datum0[:, :] = 1.0
        datum0.conditions.add('Acq0', acq)

        acq = AcquisitionRasterXY(7, 7, 1e3, 1e3)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(6.0, 6.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(12.0, 12.0, 0.0)
        datum1 = ImageRaster2D(7, 7)
        datum1[:, :] = 2.0
        datum1.conditions.add('Acq0', acq)

        datum = stitch(datum0, datum1)

        self.assertEqual((13, 13), datum.shape)
        self.assertAlmostEqual(1.0, datum[0, 0], 4)
        self.assertAlmostEqual(0.0, datum[0, -1], 4)
        self.assertAlmostEqual(2.0, datum[-1, -1], 4)
        self.assertAlmostEqual(0.0, datum[-1, 0], 4)

    def teststitch2(self):
        acq = AcquisitionRasterXY(7, 7, 1e3, 1e3)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(6.0, 6.0, 0.0)
        datum0 = ImageRaster2DSpectral(7, 7, 3)
        datum0[:, :] = [1.0, 2.0, 3.0]
        datum0.conditions.add('Acq0', acq)

        acq = AcquisitionRasterXY(7, 7, 1e3, 1e3)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(6.0, 6.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(12.0, 12.0, 0.0)
        datum1 = ImageRaster2DSpectral(7, 7, 3)
        datum1[:, :] = [4.0, 5.0, 6.0]
        datum1.conditions.add('Acq0', acq)

        datum = stitch(datum0, datum1)

        self.assertEqual((13, 13, 3), datum.shape)
        self.assertAlmostEqual(1.0, datum[0, 0, 0], 4)
        self.assertAlmostEqual(2.0, datum[0, 0, 1], 4)
        self.assertAlmostEqual(3.0, datum[0, 0, 2], 4)
        self.assertAlmostEqual(0.0, datum[0, -1, 0], 4)
        self.assertAlmostEqual(4.0, datum[-1, -1, 0], 4)
        self.assertAlmostEqual(5.0, datum[-1, -1, 1], 4)
        self.assertAlmostEqual(6.0, datum[-1, -1, 2], 4)
        self.assertAlmostEqual(0.0, datum[-1, 0, 0], 4)

class TestImageRaster2D(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datum = ImageRaster2D(7, 7)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0, 0] = 5.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(7, self.datum.x)
        self.assertEqual(7, self.datum.y)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(5.0, self.datum[0, 0], 4)

        self.assertEqual(7, self.datum.collection_dimensions['X'])
        self.assertEqual(7, self.datum.collection_dimensions['Y'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0, 0)
        self.assertAlmostEqual(5.0, analysis, 4)
        self.assertEqual(1, len(analysis.conditions))

    def testget_position1(self):
        acq = AcquisitionRasterXY(7, 7)
        acq.positions[POSITION_LOCATION_CENTER] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(-1.0, 1.0, 0.0)
        self.datum.conditions.add('Acq0', acq)

        pos = self.datum.get_position(0, 0)
        self.assertAlmostEqual(-1.0, pos.x, 4)
        self.assertAlmostEqual(1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 0)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 3)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(0.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        actual = self.datum.get_position(-1, -1)
        expected = self.datum.get_position(6, 6)
        self.assertAlmostEqual(expected.x, actual.x, 4)
        self.assertAlmostEqual(expected.y, actual.y, 4)
        self.assertAlmostEqual(expected.z, actual.z, 4)

    def testget_position2(self):
        acq = AcquisitionRasterXY(7, 7)
        acq.positions[POSITION_LOCATION_CENTER] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(1.0, -1.0, 0.0)
        self.datum.conditions.add('Acq0', acq)

        pos = self.datum.get_position(0, 0)
        self.assertAlmostEqual(1.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 0)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 3)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(0.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        actual = self.datum.get_position(-1, -1)
        expected = self.datum.get_position(6, 6)
        self.assertAlmostEqual(expected.x, actual.x, 4)
        self.assertAlmostEqual(expected.y, actual.y, 4)
        self.assertAlmostEqual(expected.z, actual.z, 4)

    def testget_position3(self):
        acq = AcquisitionRasterXY(7, 7)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(1.0, -1.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(-1.0, 1.0, 0.0)
        self.datum.conditions.add('Acq0', acq)

        pos = self.datum.get_position(0, 0)
        self.assertAlmostEqual(1.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 0)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 3)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(0.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        actual = self.datum.get_position(-1, -1)
        expected = self.datum.get_position(6, 6)
        self.assertAlmostEqual(expected.x, actual.x, 4)
        self.assertAlmostEqual(expected.y, actual.y, 4)
        self.assertAlmostEqual(expected.z, actual.z, 4)

    def testget_position4(self):
        acq = AcquisitionRasterXY(7, 7)
        acq.positions[POSITION_LOCATION_CENTER] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_END] = SpecimenPosition(-1.0, 1.0, 0.0)
        self.datum.conditions.add('Acq0', acq)

        pos = self.datum.get_position(0, 0)
        self.assertAlmostEqual(1.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 0)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(-1.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        pos = self.datum.get_position(3, 3)
        self.assertAlmostEqual(0.0, pos.x, 4)
        self.assertAlmostEqual(0.0, pos.y, 4)
        self.assertAlmostEqual(0.0, pos.z, 4)

        actual = self.datum.get_position(-1, -1)
        expected = self.datum.get_position(6, 6)
        self.assertAlmostEqual(expected.x, actual.x, 4)
        self.assertAlmostEqual(expected.y, actual.y, 4)
        self.assertAlmostEqual(expected.z, actual.z, 4)

    def testget_index(self):
        acq = AcquisitionRasterXY(7, 7)
        acq.positions[POSITION_LOCATION_CENTER] = SpecimenPosition(0.0, 0.0, 0.0)
        acq.positions[POSITION_LOCATION_START] = SpecimenPosition(-1.0, 1.0, 0.0)
        self.datum.conditions.add('Acq0', acq)

        position = self.datum.get_position(0, 0)
        self.assertEqual((0, 0), self.datum.get_index(position))

        position = self.datum.get_position(3, 3)
        self.assertEqual((3, 3), self.datum.get_index(position))

        position = self.datum.get_position(-1, -1)
        self.assertEqual((6, 6), self.datum.get_index(position))

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
