#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimen import \
    Specimen, SpecimenLayer, SpecimenMultilayer
from pyhmsa.spec.condition.composition import CompositionElemental

# Globals and constants variables.

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
        comp = CompositionElemental('atoms')
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
        self.assertEqual('degreesC', self.spc.temperature.unit)

    def testpickle(self):
        self.spc.description = 'Natural cryolite standard'
        self.spc.origin = 'Kitaa, Greenland'
        self.spc.formula = 'Na3AlF6'
        comp = CompositionElemental('atoms')
        comp[11] = 3
        comp[13] = 1
        comp[9] = 6
        self.spc.composition = comp
        self.spc.temperature = -20.0

        s = pickle.dumps(self.spc)
        spc = pickle.loads(s)

        self.assertEqual('Cryolite', spc.name)
        self.assertEqual('Natural cryolite standard', spc.description)
        self.assertEqual('Kitaa, Greenland', spc.origin)
        self.assertEqual('Na3AlF6', spc.formula)
        self.assertAlmostEqual(3, spc.composition[11], 4)
        self.assertAlmostEqual(1, spc.composition[13], 4)
        self.assertAlmostEqual(6, spc.composition[9], 4)
        self.assertAlmostEqual(-20.0, spc.temperature, 4)
        self.assertEqual('degreesC', spc.temperature.unit)

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
        comp = CompositionElemental('wt%')
        comp[6] = 100.0
        self.layer.composition = comp
        self.assertAlmostEqual(100.0, self.layer.composition[6], 4)

    def testpickle(self):
        self.layer.name = 'Carbon coat'
        self.layer.thickness = 50.0
        self.layer.formula = 'C'
        comp = CompositionElemental('wt%')
        comp[6] = 100.0
        self.layer.composition = comp

        s = pickle.dumps(self.layer)
        layer = pickle.loads(s)

        self.assertEqual('Carbon coat', layer.name)
        self.assertAlmostEqual(50.0, layer.thickness, 4)
        self.assertEqual('nm', layer.thickness.unit)
        self.assertAlmostEqual(100.0, layer.composition[6], 4)

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

    def testpickle(self):
        s = pickle.dumps(self.spc)
        spc = pickle.loads(s)

        self.assertEqual(1, len(spc.layers))
        self.assertEqual('Carbon coat', spc.layers[0].name)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
