#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.acquisition import \
    (_Acquisition, AcquisitionPoint, AcquisitionMultipoint,
     _AcquisitionRaster, AcquisitionRasterLinescan,
    AcquisitionRasterXY, AcquisitionRasterXYZ
     )
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import \
    (POSITION_LOCATION_CENTER, POSITION_LOCATION_START, POSITION_LOCATION_END,
     RASTER_MODE_STAGE, RASTER_MODE_Z_FIB)

class Test_Acquisition(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = _Acquisition(5.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testdwell_time(self):
        self.assertAlmostEqual(5.0, self.acq.dwell_time, 4)
        self.assertEqual('s', self.acq.dwell_time.unit)
        self.assertAlmostEqual(5.0, self.acq.get_dwell_time(), 4)
        self.assertEqual('s', self.acq.get_dwell_time().unit)

        self.acq.set_dwell_time(10.0, 'ms')
        self.assertAlmostEqual(10.0, self.acq.dwell_time, 4)
        self.assertEqual('ms', self.acq.dwell_time.unit)
        self.assertAlmostEqual(10.0, self.acq.get_dwell_time(), 4)
        self.assertEqual('ms', self.acq.get_dwell_time().unit)

        self.acq.dwell_time = 15.0
        self.assertAlmostEqual(15.0, self.acq.dwell_time, 4)
        self.assertEqual('s', self.acq.dwell_time.unit)
        self.assertAlmostEqual(15.0, self.acq.get_dwell_time(), 4)
        self.assertEqual('s', self.acq.get_dwell_time().unit)

        self.acq.dwell_time = (15.0, 'ms')
        self.assertAlmostEqual(15.0, self.acq.dwell_time, 4)
        self.assertEqual('ms', self.acq.dwell_time.unit)
        self.assertAlmostEqual(15.0, self.acq.get_dwell_time(), 4)
        self.assertEqual('ms', self.acq.get_dwell_time().unit)

        self.acq.dwell_time = (15.0, None)
        self.assertAlmostEqual(15.0, self.acq.dwell_time, 4)
        self.assertEqual('s', self.acq.dwell_time.unit)
        self.assertAlmostEqual(15.0, self.acq.get_dwell_time(), 4)
        self.assertEqual('s', self.acq.get_dwell_time().unit)

    def testtotal_time(self):
        self.assertFalse(self.acq.total_time)

        self.acq.set_total_time(6.0, 'ns')
        self.assertAlmostEqual(6.0, self.acq.total_time, 4)
        self.assertEqual('ns', self.acq.total_time.unit)

    def testdwell_time_live(self):
        self.assertFalse(self.acq.dwell_time_live)

        self.acq.set_dwell_time_live(7.0, 'ms')
        self.assertAlmostEqual(7.0, self.acq.dwell_time_live, 4)
        self.assertEqual('ms', self.acq.dwell_time_live.unit)

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertAlmostEqual(5.0, acq.dwell_time, 4)

class TestAcquisitionPosition(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        position = SpecimenPosition(x=5, y=5, z=11)
        self.acq = AcquisitionPoint(position, total_time=10.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testposition(self):
        self.assertAlmostEqual(5.0, self.acq.position.x, 4)
        self.assertAlmostEqual(5.0, self.acq.position.y, 4)
        self.assertAlmostEqual(11.0, self.acq.position.z, 4)

        self.assertRaises(ValueError, self.acq.set_position, None)

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertAlmostEqual(10.0, acq.total_time, 4)
        self.assertAlmostEqual(5.0, acq.position.x, 4)
        self.assertAlmostEqual(5.0, acq.position.y, 4)
        self.assertAlmostEqual(11.0, acq.position.z, 4)

class TestAcquisitionMultipoint(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = AcquisitionMultipoint()
        self.acq.positions.append(SpecimenPosition(x=5, y=5, z=11))
        self.acq.positions.append(SpecimenPosition(x=6, y=6, z=11))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testpositions(self):
        self.assertEqual(2, len(self.acq.positions))

        self.assertAlmostEqual(5.0, self.acq.positions[0].x, 4)
        self.assertAlmostEqual(5.0, self.acq.positions[0].y, 4)
        self.assertAlmostEqual(11.0, self.acq.positions[0].z, 4)

        self.assertAlmostEqual(6.0, self.acq.positions[1].x, 4)
        self.assertAlmostEqual(6.0, self.acq.positions[1].y, 4)
        self.assertAlmostEqual(11.0, self.acq.positions[1].z, 4)

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertEqual(2, len(acq.positions))

        self.assertAlmostEqual(5.0, acq.positions[0].x, 4)
        self.assertAlmostEqual(5.0, acq.positions[0].y, 4)
        self.assertAlmostEqual(11.0, acq.positions[0].z, 4)

        self.assertAlmostEqual(6.0, acq.positions[1].x, 4)
        self.assertAlmostEqual(6.0, acq.positions[1].y, 4)
        self.assertAlmostEqual(11.0, acq.positions[1].z, 4)

class Test_AcquisitionRaster(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = _AcquisitionRaster(RASTER_MODE_STAGE)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testraster_mode(self):
        self.assertEqual(RASTER_MODE_STAGE, self.acq.raster_mode)

        self.assertRaises(ValueError, self.acq.set_raster_mode, 'ABC')

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertEqual(RASTER_MODE_STAGE, acq.raster_mode)

class TestAcquisitionRasterLinescan(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = AcquisitionRasterLinescan(100, (0.5, 'nm'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def teststep_count(self):
        self.assertEqual(100, self.acq.step_count)

        self.assertRaises(ValueError, self.acq.set_step_count, None)

    def teststep_size(self):
        self.assertTrue(self.acq.step_size)
        self.assertAlmostEqual(0.5, self.acq.step_size, 4)
        self.assertEqual('nm', self.acq.step_size.unit)

    def teststart_position(self):
        self.assertFalse(self.acq.position_start)

        self.acq.position_start = SpecimenPosition(y=1.0)
        self.assertAlmostEqual(1.0, self.acq.position_start.y, 4)
        self.assertEqual('mm', self.acq.position_start.y.unit)

        self.assertEqual(1, len(self.acq.positions))
        self.assertAlmostEqual(1.0, self.acq.positions[POSITION_LOCATION_START].y, 4)
        self.assertEqual('mm', self.acq.positions[POSITION_LOCATION_START].y.unit)

    def testend_position(self):
        self.assertFalse(self.acq.position_end)

        self.acq.position_end = SpecimenPosition(y=2.0)
        self.assertAlmostEqual(2.0, self.acq.position_end.y, 4)
        self.assertEqual('mm', self.acq.position_end.y.unit)

        self.assertEqual(1, len(self.acq.positions))
        self.assertAlmostEqual(2.0, self.acq.positions[POSITION_LOCATION_END].y, 4)
        self.assertEqual('mm', self.acq.positions[POSITION_LOCATION_END].y.unit)

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertEqual(100, acq.step_count)
        self.assertAlmostEqual(0.5, acq.step_size, 4)
        self.assertEqual('nm', acq.step_size.unit)

class TestAcquisitionRasterXY(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = AcquisitionRasterXY(4, 5)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testposition(self):
        self.assertIsNone(self.acq.position)

        position = SpecimenPosition(0.5)
        self.acq.set_position(position, POSITION_LOCATION_CENTER)
        self.assertAlmostEqual(0.5, self.acq.get_position().x, 4)
        self.assertIn(POSITION_LOCATION_CENTER, self.acq.get_positions())

        position = SpecimenPosition(0.4)
        self.acq.position = position
        self.assertAlmostEqual(0.4, self.acq.position.x, 4)
        self.assertIn(POSITION_LOCATION_START, self.acq.positions)

        position = SpecimenPosition(0.3)
        self.acq.position = (position, POSITION_LOCATION_CENTER)
        self.assertAlmostEqual(0.3, self.acq.position.x, 4)
        self.assertIn(POSITION_LOCATION_CENTER, self.acq.positions)

    def teststep_count_x(self):
        self.assertEqual(4, self.acq.step_count_x)

        self.assertRaises(ValueError, self.acq.set_step_count_x, None)

    def teststep_count_y(self):
        self.assertEqual(5, self.acq.step_count_y)

        self.assertRaises(ValueError, self.acq.set_step_count_y, None)

    def teststep_size_x(self):
        self.assertFalse(self.acq.step_size_x)

        self.acq.set_step_size_x(5.0, 'pm')
        self.assertAlmostEqual(5, self.acq.step_size_x, 4)
        self.assertEqual('pm', self.acq.step_size_x.unit)

    def teststep_size_y(self):
        self.assertFalse(self.acq.step_size_y)

        self.acq.set_step_size_y(5.0, 'pm')
        self.assertAlmostEqual(5, self.acq.step_size_y, 4)
        self.assertEqual('pm', self.acq.step_size_y.unit)

    def testframe_count(self):
        self.assertFalse(self.acq.frame_count)

        self.acq.frame_count = 30
        self.assertEqual(30, self.acq.frame_count)

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertEqual(4, acq.step_count_x)
        self.assertEqual(5, acq.step_count_y)

class TestAcquisitionRasterXYZ(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.acq = AcquisitionRasterXYZ(4, 5, 6)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testposition(self):
        self.assertIsNone(self.acq.position)

        position = SpecimenPosition(0.5)
        self.acq.set_position(position, POSITION_LOCATION_CENTER)
        self.assertAlmostEqual(0.5, self.acq.get_position().x, 4)
        self.assertIn(POSITION_LOCATION_CENTER, self.acq.get_positions())

    def teststep_count_x(self):
        self.assertEqual(4, self.acq.step_count_x)

        self.assertRaises(ValueError, self.acq.set_step_count_x, None)

    def teststep_count_y(self):
        self.assertEqual(5, self.acq.step_count_y)

        self.assertRaises(ValueError, self.acq.set_step_count_y, None)

    def teststep_count_z(self):
        self.assertEqual(6, self.acq.step_count_z)

        self.assertRaises(ValueError, self.acq.set_step_count_z, None)

    def teststep_size_x(self):
        self.assertFalse(self.acq.step_size_x)

        self.acq.set_step_size_x(5.0, 'pm')
        self.assertAlmostEqual(5, self.acq.step_size_x, 4)
        self.assertEqual('pm', self.acq.step_size_x.unit)

    def teststep_size_y(self):
        self.assertFalse(self.acq.step_size_y)

        self.acq.set_step_size_y(5.0, 'pm')
        self.assertAlmostEqual(5, self.acq.step_size_y, 4)
        self.assertEqual('pm', self.acq.step_size_y.unit)

    def teststep_size_z(self):
        self.assertFalse(self.acq.step_size_z)

        self.acq.set_step_size_z(5.0, 'pm')
        self.assertAlmostEqual(5, self.acq.step_size_z, 4)
        self.assertEqual('pm', self.acq.step_size_z.unit)

    def testraster_mode_z(self):
        self.assertFalse(self.acq.raster_mode_z)

        self.acq.raster_mode_z = RASTER_MODE_Z_FIB
        self.assertEqual(RASTER_MODE_Z_FIB, self.acq.raster_mode_z)

        self.assertRaises(ValueError, self.acq.set_raster_mode_z, 'ABC')

    def testpickle(self):
        s = pickle.dumps(self.acq)
        acq = pickle.loads(s)

        self.assertEqual(4, acq.step_count_x)
        self.assertEqual(5, acq.step_count_y)
        self.assertEqual(6, acq.step_count_z)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
