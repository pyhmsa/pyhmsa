#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimen import \
    SpecimenPosition, Specimen, Composition, SpecimenLayer, SpecimenMultilayer

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

class TestComposition(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.comp = Composition('atoms', {11: 3})
        self.comp[13] = 1
        self.comp.update({9: 6})

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('atoms', self.comp.unit)
        self.assertAlmostEqual(3, self.comp[11], 4)
        self.assertAlmostEqual(1, self.comp[13], 4)
        self.assertAlmostEqual(6, self.comp[9], 4)

        self.assertRaises(ValueError, Composition, 'A')

    def test__setitem__(self):
        self.assertRaises(ValueError, self.comp.__setitem__, -1, 1)
        self.assertRaises(ValueError, self.comp.__setitem__, 119, 1)

class TestSpecimen(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.spc = Specimen('Cryolite')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testname(self):
        self.assertEqual('Cryolite', self.spc.name)
        self.assertRaises(ValueError, self.spc.set_name, None)

    def testdescription(self):
        self.spc.description = 'Natural cryolite standard'
        self.assertEqual('Natural cryolite standard', self.spc.description)

    def testorigin(self):
        self.spc.origin = 'Kitaa, Greenland'
        self.assertEqual('Kitaa, Greenland', self.spc.origin)

    def testformula(self):
        self.spc.formula = 'Na3AlF6'
        self.assertEqual('Na3AlF6', self.spc.formula)

    def testcomposition(self):
        comp = Composition('atoms')
        comp[11] = 3
        comp[13] = 1
        comp[9] = 6
        self.spc.composition = comp
        self.assertAlmostEqual(3, self.spc.composition[11], 4)
        self.assertAlmostEqual(1, self.spc.composition[13], 4)
        self.assertAlmostEqual(6, self.spc.composition[9], 4)

    def testtemperature(self):
        self.spc.temperature = -20.0
        self.assertAlmostEqual(-20.0, self.spc.temperature, 4)
        self.assertEqual(u'\u00b0\u0043', self.spc.temperature.unit)

class TestSpecimenLayer(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.layer = SpecimenLayer()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testname(self):
        self.layer.name = 'Carbon coat'
        self.assertEqual('Carbon coat', self.layer.name)

    def testthickness(self):
        self.assertTrue(self.layer.is_bulk())

        self.layer.thickness = 50.0
        self.assertAlmostEqual(50.0, self.layer.thickness, 4)
        self.assertEqual('nm', self.layer.thickness.unit)
        self.assertFalse(self.layer.is_bulk())

    def testformula(self):
        self.layer.formula = 'C'
        self.assertEqual('C', self.layer.formula)

    def testcomposition(self):
        comp = Composition('wt%')
        comp[6] = 100.0
        self.layer.composition = comp
        self.assertAlmostEqual(100.0, self.layer.composition[6], 4)

class TestSpecimenMultilayer(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.spc = SpecimenMultilayer('Carbon coated cryolite')

        layer = SpecimenLayer('Carbon coat', 50.0, 'C')
        self.spc.layers.append(layer)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testlayers(self):
        self.assertEqual(1, len(self.spc.layers))
        self.assertEqual('Carbon coat', self.spc.layers[0].name)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
