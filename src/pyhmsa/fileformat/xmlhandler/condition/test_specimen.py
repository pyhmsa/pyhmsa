#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.specimen import \
     SpecimenXMLHandler, SpecimenMultilayerXMLHandler
from pyhmsa.spec.condition.specimen import Specimen, SpecimenMultilayer
from pyhmsa.spec.condition.composition import CompositionElemental

# Globals and constants variables.

class TestSpecimenXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = SpecimenXMLHandler(1.0)

        comp = CompositionElemental('atoms')
        comp.update({11: 3, 13: 1, 9: 6})
        self.obj = Specimen('Cryolite', 'Natural cryolite standard',
                            'Kitaa, Greenland', 'Na3AlF6', comp, -20.0)

        source = '<Specimen><Name>Cryolite</Name><Description>Natural cryolite standard</Description><Origin>Kitaa, Greenland</Origin><Formula>Na3AlF6</Formula><Composition Class="Elemental"><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="atoms" DataType="float">1.</Element><Element Z="9" Unit="atoms" DataType="float">6.</Element></Composition><Temperature Unit="degreesC" DataType="float">-20.0</Temperature></Specimen>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Cryolite', obj.name)
        self.assertEqual('Natural cryolite standard', obj.description)
        self.assertEqual('Kitaa, Greenland', obj.origin)
        self.assertEqual('Na3AlF6', obj.formula)
        self.assertEqual(3, len(obj.composition))
        self.assertAlmostEqual(3.0, obj.composition[11], 4)
        self.assertAlmostEqual(1.0, obj.composition[13], 4)
        self.assertAlmostEqual(6.0, obj.composition[9], 4)
        self.assertAlmostEqual(-20.0, obj.temperature, 4)
        self.assertEqual('degreesC', obj.temperature.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Specimen', element.tag)
        self.assertEqual('Cryolite', element.find('Name').text)
        self.assertEqual('Natural cryolite standard', element.find('Description').text)
        self.assertEqual('Kitaa, Greenland', element.find('Origin').text)
        self.assertEqual('Na3AlF6', element.find('Formula').text)
        self.assertEqual(3, len(element.findall('Composition/Element')))
        self.assertEqual('-20.0', element.find('Temperature').text)

class TestSpecimenMultilayerXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = SpecimenMultilayerXMLHandler(1.0)

        self.obj = SpecimenMultilayer('Cryolite', 'Natural cryolite standard',
                            'Kitaa, Greenland', 'Na3AlF6')

        comp = CompositionElemental('wt%')
        comp.update({6: 100.0})
        self.obj.append_layer('Carbon coat', 50.0, 'C', comp)

        source = u'<Specimen Class="Multilayer"><Name>Cryolite</Name><Description>Natural cryolite standard</Description><Origin>Kitaa, Greenland</Origin><Formula>Na3AlF6</Formula><Layers><Layer Name="Carbon coat"><Thickness Unit="nm" DataType="float">50</Thickness><Formula>C</Formula><Composition Class="Elemental"><Element Z="6" Unit="wt%" DataType="float">50.</Element></Composition></Layer></Layers></Specimen>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Specimen')))
        self.assertFalse(self.h.can_parse(etree.Element('ABC')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('Cryolite', obj.name)
        self.assertEqual('Natural cryolite standard', obj.description)
        self.assertEqual('Kitaa, Greenland', obj.origin)
        self.assertEqual('Na3AlF6', obj.formula)
        self.assertEqual(1, len(obj.layers))
        self.assertEqual('Carbon coat', obj.layers[0].name)
        self.assertAlmostEqual(50.0, obj.layers[0].thickness, 4)
        self.assertEqual('nm', obj.layers[0].thickness.unit)
        self.assertEqual('C', obj.layers[0].formula)
        self.assertAlmostEqual(50.0, obj.layers[0].composition[6], 4)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Specimen', element.tag)
        self.assertEqual('Cryolite', element.find('Name').text)
        self.assertEqual('Natural cryolite standard', element.find('Description').text)
        self.assertEqual('Kitaa, Greenland', element.find('Origin').text)
        self.assertEqual('Na3AlF6', element.find('Formula').text)
        self.assertEqual('Carbon coat', element.find('Layers/Layer').get('Name'))
        self.assertEqual('50.0', element.find('Layers/Layer/Thickness').text)
        self.assertEqual('C', element.find('Layers/Layer/Formula').text)
        self.assertEqual('100.0', element.find('Layers/Layer/Composition/Element').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
