#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.condition.acquisition import \
    (AcquisitionPointXMLHandler, AcquisitionMultipointXMLHandler,
     AcquisitionRasterLinescanXMLHandler, AcquisitionRasterXYXMLHandler,
     AcquisitionRasterXYZXMLHandler)
from pyhmsa.spec.condition.acquisition import \
    (AcquisitionPoint, AcquisitionMultipoint,
     AcquisitionRasterLinescan, AcquisitionRasterXY, AcquisitionRasterXYZ)
from pyhmsa.spec.condition.specimenposition import SpecimenPosition

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import RASTER_MODE_STAGE, RASTER_MODE_Z_FIB

class TestAcquisitionPointXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = AcquisitionPointXMLHandler(1.0)

        position = SpecimenPosition(0.0, 0.0, 10.0, 90.0, 70.0)
        self.obj = AcquisitionPoint(position, 35.0, 14400.0, 36.0)

        source = '<Acquisition Class="Point"><DwellTime Unit="s" DataType="float">35.0</DwellTime><TotalTime Unit="s" DataType="float">14400.0</TotalTime><DwellTime_Live Unit="s" DataType="float">36.0</DwellTime_Live><SpecimenPosition><X Unit="mm" DataType="float">0.0</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z><R Unit="degrees" DataType="float">90.0</R><T Unit="degrees" DataType="float">70.0</T></SpecimenPosition></Acquisition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)

        self.assertAlmostEqual(35.0, obj.dwell_time, 4)
        self.assertEqual('s', obj.dwell_time.unit)
        self.assertAlmostEqual(14400.0, obj.total_time, 4)
        self.assertEqual('s', obj.total_time.unit)
        self.assertAlmostEqual(36.0, obj.dwell_time_live, 4)
        self.assertEqual('s', obj.dwell_time_live.unit)

        position = obj.position
        self.assertAlmostEqual(0.0, position.x, 4)
        self.assertEqual('mm', position.x.unit)
        self.assertAlmostEqual(0.0, position.y, 4)
        self.assertEqual('mm', position.y.unit)
        self.assertAlmostEqual(10.0, position.z, 4)
        self.assertEqual('mm', position.z.unit)
        self.assertAlmostEqual(90.0, position.r, 4)
        self.assertEqual('degrees', position.r.unit)
        self.assertAlmostEqual(70.0, position.t, 4)
        self.assertEqual('degrees', position.t.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Acquisition', element.tag)
        self.assertEqual('Point', element.attrib['Class'])

        self.assertEqual('35.0', element.find('DwellTime').text)
        self.assertEqual('14400.0', element.find('TotalTime').text)
        self.assertEqual('36.0', element.find('DwellTime_Live').text)

        self.assertEqual('0.0', element.find('SpecimenPosition').find('X').text)
        self.assertEqual('0.0', element.find('SpecimenPosition').find('Y').text)
        self.assertEqual('10.0', element.find('SpecimenPosition').find('Z').text)
        self.assertEqual('90.0', element.find('SpecimenPosition').find('R').text)
        self.assertEqual('70.0', element.find('SpecimenPosition').find('T').text)
#
class TestAcquisitionMultipointXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = AcquisitionMultipointXMLHandler(1.0)

        self.obj = AcquisitionMultipoint()
        self.obj.positions.append(SpecimenPosition(0.0, 0.0, 10.0, 90.0, 70.0))
        self.obj.positions.append(SpecimenPosition(1.0, 1.0, 11.0, 91.0, 71.0))

        source = '<Acquisition Class="Multipoint"><PointCount DataType="uint32">2</PointCount><Positions><SpecimenPosition><X Unit="mm" DataType="float">0.0</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z><R Unit="degrees" DataType="float">90.0</R><T Unit="degrees" DataType="float">70.0</T></SpecimenPosition><SpecimenPosition><X Unit="mm" DataType="float">1.0</X><Y Unit="mm" DataType="float">1.0</Y><Z Unit="mm" DataType="float">11.0</Z><R Unit="degrees" DataType="float">91.0</R><T Unit="degrees" DataType="float">71.0</T></SpecimenPosition></Positions></Acquisition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertAlmostEqual(0.0, obj.positions[0].x, 4)
        self.assertEqual('mm', obj.positions[0].x.unit)
        self.assertAlmostEqual(0.0, obj.positions[0].y, 4)
        self.assertEqual('mm', obj.positions[0].y.unit)
        self.assertAlmostEqual(10.0, obj.positions[0].z, 4)
        self.assertEqual('mm', obj.positions[0].z.unit)
        self.assertAlmostEqual(90.0, obj.positions[0].r, 4)
        self.assertEqual('degrees', obj.positions[0].r.unit)
        self.assertAlmostEqual(70.0, obj.positions[0].t, 4)
        self.assertEqual('degrees', obj.positions[0].t.unit)

        self.assertAlmostEqual(1.0, obj.positions[1].x, 4)
        self.assertEqual('mm', obj.positions[1].x.unit)
        self.assertAlmostEqual(1.0, obj.positions[1].y, 4)
        self.assertEqual('mm', obj.positions[1].y.unit)
        self.assertAlmostEqual(11.0, obj.positions[1].z, 4)
        self.assertEqual('mm', obj.positions[1].z.unit)
        self.assertAlmostEqual(91.0, obj.positions[1].r, 4)
        self.assertEqual('degrees', obj.positions[1].r.unit)
        self.assertAlmostEqual(71.0, obj.positions[1].t, 4)
        self.assertEqual('degrees', obj.positions[1].t.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Acquisition', element.tag)
        self.assertEqual('Multipoint', element.attrib['Class'])
        self.assertEqual('0.0', element.find('Positions').findall('SpecimenPosition')[0].find('X').text)
        self.assertEqual('0.0', element.find('Positions').findall('SpecimenPosition')[0].find('Y').text)
        self.assertEqual('10.0', element.find('Positions').findall('SpecimenPosition')[0].find('Z').text)
        self.assertEqual('90.0', element.find('Positions').findall('SpecimenPosition')[0].find('R').text)
        self.assertEqual('70.0', element.find('Positions').findall('SpecimenPosition')[0].find('T').text)
        self.assertEqual('1.0', element.find('Positions').findall('SpecimenPosition')[1].find('X').text)
        self.assertEqual('1.0', element.find('Positions').findall('SpecimenPosition')[1].find('Y').text)
        self.assertEqual('11.0', element.find('Positions').findall('SpecimenPosition')[1].find('Z').text)
        self.assertEqual('91.0', element.find('Positions').findall('SpecimenPosition')[1].find('R').text)
        self.assertEqual('71.0', element.find('Positions').findall('SpecimenPosition')[1].find('T').text)

class TestAcquisitionRasterLinescanXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = AcquisitionRasterLinescanXMLHandler(1.0)

        position_start = SpecimenPosition(0.0, 0.0, 10.0)
        position_end = SpecimenPosition(10.24, 0.0, 10.0)
        self.obj = AcquisitionRasterLinescan(1024, 10.0, position_start,
                                             position_end, RASTER_MODE_STAGE)

        source = '<Acquisition Class="Raster/Linescan"><RasterMode>Stage</RasterMode><StepCount DataType="uint32">1024</StepCount><StepSize Unit="um" DataType="float">10.</StepSize><SpecimenPosition Name="Start"><X Unit="mm" DataType="float">0.0</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z></SpecimenPosition><SpecimenPosition Name="End"><X Unit="mm" DataType="float">10.24</X><Y Unit="mm" DataType="float">0.0</Y><Z Unit="mm" DataType="float">10.0</Z></SpecimenPosition></Acquisition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(RASTER_MODE_STAGE, obj.raster_mode)
        self.assertEqual(1024, obj.step_count)
        self.assertAlmostEqual(10.0, obj.step_size, 4)
        self.assertEqual('um', obj.step_size.unit)
        self.assertAlmostEqual(0.0, obj.position_start.x, 4)
        self.assertEqual('mm', obj.position_start.x.unit)
        self.assertAlmostEqual(0.0, obj.position_start.y, 4)
        self.assertEqual('mm', obj.position_start.y.unit)
        self.assertAlmostEqual(10.0, obj.position_start.z, 4)
        self.assertEqual('mm', obj.position_start.z.unit)
        self.assertAlmostEqual(10.24, obj.position_end.x, 4)
        self.assertEqual('mm', obj.position_end.x.unit)
        self.assertAlmostEqual(0.0, obj.position_end.y, 4)
        self.assertEqual('mm', obj.position_end.y.unit)
        self.assertAlmostEqual(10.0, obj.position_end.z, 4)
        self.assertEqual('mm', obj.position_end.z.unit)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Acquisition', element.tag)
        self.assertEqual('Raster/Linescan', element.attrib['Class'])
        self.assertEqual('Stage', element.find('RasterMode').text)
        self.assertEqual('1024', element.find('StepCount').text)
        self.assertEqual('10.0', element.find('StepSize').text)
        self.assertEqual(2, len(element.findall('SpecimenPosition')))

class TestAcquisitionRasterXYXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = AcquisitionRasterXYXMLHandler(1.0)

        self.obj = AcquisitionRasterXY(158, 98, 1.0, 2.0, 40)

        source = '<Acquisition Class="Raster/XY"><XStepCount DataType="uint32">158</XStepCount><YStepCount DataType="uint32">98</YStepCount><XStepSize Unit="um" DataType="float">1.</XStepSize><YStepSize Unit="um" DataType="float">2.</YStepSize><FrameCount DataType="uint32">40</FrameCount></Acquisition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(158, obj.step_count_x)
        self.assertEqual(98, obj.step_count_y)
        self.assertAlmostEqual(1.0, obj.step_size_x, 4)
        self.assertEqual('um', obj.step_size_x.unit)
        self.assertAlmostEqual(2.0, obj.step_size_y, 4)
        self.assertEqual('um', obj.step_size_y.unit)
        self.assertEqual(40, obj.frame_count)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Acquisition', element.tag)
        self.assertEqual('Raster/XY', element.attrib['Class'])
        self.assertEqual('158', element.find('XStepCount').text)
        self.assertEqual('98', element.find('YStepCount').text)
        self.assertEqual('1.0', element.find('XStepSize').text)
        self.assertEqual('2.0', element.find('YStepSize').text)
        self.assertEqual('40', element.find('FrameCount').text)

class TestAcquisitionRasterXYZXMLHandler(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.h = AcquisitionRasterXYZXMLHandler(1.0)

        self.obj = AcquisitionRasterXYZ(158, 98, 185, 1.0, 2.0, 3.0,
                                        raster_mode_z=RASTER_MODE_Z_FIB)

        source = '<Acquisition Class="Raster/XYZ"><XStepCount DataType="uint32">158</XStepCount><YStepCount DataType="uint32">98</YStepCount><ZStepCount DataType="uint32">185</ZStepCount><XStepSize Unit="um" DataType="float">1.</XStepSize><YStepSize Unit="um" DataType="float">2.</YStepSize><ZStepSize Unit="um" DataType="float">3.</ZStepSize><ZRasterMode>FIB</ZRasterMode></Acquisition>'
        self.element = etree.fromstring(source.encode('utf-8'))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcan_parse(self):
        self.assertTrue(self.h.can_parse(self.element))
        self.assertFalse(self.h.can_parse(etree.Element('Acquisition')))
        self.assertFalse(self.h.can_parse(etree.Element('Abc')))

    def testparse(self):
        obj = self.h.parse(self.element)
        self.assertEqual(158, obj.step_count_x)
        self.assertEqual(98, obj.step_count_y)
        self.assertEqual(185, obj.step_count_z)
        self.assertAlmostEqual(1.0, obj.step_size_x, 4)
        self.assertEqual('um', obj.step_size_x.unit)
        self.assertAlmostEqual(2.0, obj.step_size_y, 4)
        self.assertEqual('um', obj.step_size_y.unit)
        self.assertAlmostEqual(3.0, obj.step_size_z, 4)
        self.assertEqual('um', obj.step_size_z.unit)
        self.assertEqual(RASTER_MODE_Z_FIB, obj.raster_mode_z)

    def testcan_convert(self):
        self.assertTrue(self.h.can_convert(self.obj))
        self.assertFalse(self.h.can_convert(object()))

    def testconvert(self):
        element = self.h.convert(self.obj)
        self.assertEqual('Acquisition', element.tag)
        self.assertEqual('Raster/XYZ', element.attrib['Class'])
        self.assertEqual('158', element.find('XStepCount').text)
        self.assertEqual('98', element.find('YStepCount').text)
        self.assertEqual('185', element.find('ZStepCount').text)
        self.assertEqual('1.0', element.find('XStepSize').text)
        self.assertEqual('2.0', element.find('YStepSize').text)
        self.assertEqual('3.0', element.find('ZStepSize').text)
        self.assertEqual('FIB', element.find('ZRasterMode').text)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
