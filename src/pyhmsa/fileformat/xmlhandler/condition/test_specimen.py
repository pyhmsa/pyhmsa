#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree
from io import StringIO

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.specimen import \
    (CompositionXMLHandler, SpecimenPositionXMLHandler,
     SpecimenXMLHandler, SpecimenMultilayerXMLHandler)
from pyhmsa.spec.condition.specimen import \
    (Composition, SpecimenPosition, Specimen, SpecimenMultilayer)

# Globals and constants variables.

class TestSpecimenPositionXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = SpecimenPositionXMLHandler(1.0)

        self.obj = SpecimenPosition(0.0, 0.0, 10.0, 90.0, 70.0)

        source = StringIO('<SpecimenPosition><X Unit="mm" DataType="float">0.0</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z><R Unit="\u00b0" DataType="float">90.0</R><T Unit="\u00b0" DataType="float">70.0</T></SpecimenPosition>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertAlmostEqual(0.0, obj.x, 4)
        self.assertEqual('mm', obj.x.unit)
        self.assertAlmostEqual(0.0, obj.y, 4)
        self.assertEqual('mm', obj.y.unit)
        self.assertAlmostEqual(10.0, obj.z, 4)
        self.assertEqual('mm', obj.z.unit)
        self.assertAlmostEqual(90.0, obj.r, 4)
        self.assertEqual(u'\u00b0', obj.r.unit)
        self.assertAlmostEqual(70.0, obj.t, 4)
        self.assertEqual(u'\u00b0', obj.t.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('SpecimenPosition', element.tag)
        self.assertEqual('0.0', element.find('X').text)
        self.assertEqual('0.0', element.find('Y').text)
        self.assertEqual('10.0', element.find('Z').text)
        self.assertEqual('90.0', element.find('R').text)
        self.assertEqual('70.0', element.find('T').text)

class TestCompositionXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = CompositionXMLHandler(1.0)

        self.obj = Composition('atoms')
        self.obj[11] = 3
        self.obj[13] = 1
        self.obj[9] = 6

        source = StringIO('<Composition><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="atoms" DataType="float">1.</Element><Element Z="9" Unit="atoms" DataType="float">6.</Element></Composition>')
        self.element = etree.parse(source).getroot()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual('atoms', obj.unit)
        self.assertEqual(3, len(obj))
        self.assertAlmostEqual(3.0, obj[11], 4)
        self.assertAlmostEqual(1.0, obj[13], 4)
        self.assertAlmostEqual(6.0, obj[9], 4)

        source = StringIO('<Composition></Composition>')
        element = etree.parse(source)
        obj = self.h.parse(element)
        self.assertIsNone(obj)

        source = StringIO('<Composition><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="wt%" DataType="float">1.</Element></Composition>')
        element = etree.parse(source)
        self.assertRaises(ValueError, self.h.parse, element)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Composition', element.tag)
        self.assertEqual(3, len(element.findall('Element')))

class TestSpecimenXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = SpecimenXMLHandler(1.0)

        comp = Composition('atoms')
        comp.update({11: 3, 13: 1, 9: 6})
        self.obj = Specimen('Cryolite', 'Natural cryolite standard',
                            'Kitaa, Greenland', 'Na3AlF6', comp, -20.0)

        source = StringIO('<Specimen><Name>Cryolite</Name><Description>Natural cryolite standard</Description><Origin>Kitaa, Greenland</Origin><Formula>Na3AlF6</Formula><Composition><Element Z="11" Unit="atoms" DataType="float">3.</Element><Element Z="13" Unit="atoms" DataType="float">1.</Element><Element Z="9" Unit="atoms" DataType="float">6.</Element></Composition><Temperature Unit="\u00b0\u0043" DataType="float">-20.0</Temperature></Specimen>')
        self.element = etree.parse(source).getroot()

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
        self.assertEqual(u'\u00b0\u0043', obj.temperature.unit)

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

        comp = Composition('wt%')
        comp.update({6: 100.0})
        self.obj.append_layer('Carbon coat', 50.0, 'C', comp)

        source = StringIO('<Specimen Class="Multilayer"><Name>Cryolite</Name><Description>Natural cryolite standard</Description><Origin>Kitaa, Greenland</Origin><Formula>Na3AlF6</Formula><Layers><Layer Name="Carbon coat"><Thickness Unit="nm" DataType="float">50</Thickness><Formula>C</Formula><Composition><Element Z="6" Unit="wt%" DataType="float">50.</Element></Composition></Layer></Layers></Specimen>')
        self.element = etree.parse(source).getroot()

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
