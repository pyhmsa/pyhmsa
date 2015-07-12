""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.

class TestSpecimenPosition(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.position = SpecimenPosition(y=5.0, r=90.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testx(self):
        self.assertFalse(self.position.x)

        self.position.set_x(4.0, 'm')
        self.assertAlmostEqual(4.0, self.position.x, 4)
        self.assertEqual('m', self.position.x.unit)

    def testy(self):
        self.assertTrue(self.position.y)

        self.position.set_y(4.0, 'mm')
        self.assertAlmostEqual(4.0, self.position.y, 4)
        self.assertEqual('mm', self.position.y.unit)

    def testz(self):
        self.assertFalse(self.position.z)

        self.position.set_z(4.0, 'nm')
        self.assertAlmostEqual(4.0, self.position.z, 4)
        self.assertEqual('nm', self.position.z.unit)

    def testr(self):
        self.assertTrue(self.position.r)

        self.position.set_r(4.0, 'rad')
        self.assertAlmostEqual(4.0, self.position.r, 4)
        self.assertEqual('rad', self.position.r.unit)

    def testt(self):
        self.assertFalse(self.position.t)

        self.position.set_t(4.0, 'rad')
        self.assertAlmostEqual(4.0, self.position.t, 4)
        self.assertEqual('rad', self.position.t.unit)

    def testpickle(self):
        s = pickle.dumps(self.position)
        position = pickle.loads(s)

        self.assertAlmostEqual(5.0, position.y, 4)
        self.assertEqual('mm', position.y.unit)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertEqual('degrees', position.r.unit)

    def test__add__(self):
        position = self.position + SpecimenPosition(x=1.0, y=1.0, t=1.0)
        self.assertIsNone(position.x)
        self.assertAlmostEqual(6.0, position.y, 4)
        self.assertIsNone(position.z)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertIsNone(position.t)

        position = self.position + SpecimenPosition()
        self.assertIsNone(position.x)
        self.assertAlmostEqual(5.0, position.y, 4)
        self.assertIsNone(position.z)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertIsNone(position.t)

        self.position += SpecimenPosition(x=1.0, y=1.0, t=1.0)
        self.assertIsNone(self.position.x)
        self.assertAlmostEqual(6.0, self.position.y, 4)
        self.assertIsNone(self.position.z)
        self.assertAlmostEqual(90.0, self.position.r, 4)
        self.assertIsNone(self.position.t)

    def test__sub__(self):
        position = self.position - SpecimenPosition(x=1.0, y=1.0, t=1.0)
        self.assertIsNone(position.x)
        self.assertAlmostEqual(4.0, position.y, 4)
        self.assertIsNone(position.z)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertIsNone(position.t)

        position = self.position - SpecimenPosition()
        self.assertIsNone(position.x)
        self.assertAlmostEqual(5.0, position.y, 4)
        self.assertIsNone(position.z)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertIsNone(position.t)

        self.position -= SpecimenPosition(x=1.0, y=1.0, t=1.0)
        self.assertIsNone(self.position.x)
        self.assertAlmostEqual(4.0, self.position.y, 4)
        self.assertIsNone(self.position.z)
        self.assertAlmostEqual(90.0, self.position.r, 4)
        self.assertIsNone(self.position.t)

    def testtolist(self):
        l = self.position.tolist()
        self.assertIsNone(l[0])
        self.assertAlmostEqual(5.0, l[1], 4)
        self.assertIsNone(l[2])
        self.assertAlmostEqual(90.0, l[3], 4)
        self.assertIsNone(l[4])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
