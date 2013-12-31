#!/usr/bin/env python
"""
================================================================================
:mod:`acquisition` -- XML handler for acquisition classes
================================================================================

.. module:: acquisition
   :synopsis: XML handler for acquisition classes

.. inheritance-diagram:: acquisition

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.condition.acquisition import \
    (AcquisitionPoint, AcquisitionMultipoint,
     AcquisitionRasterLinescan, AcquisitionRasterXY, AcquisitionRasterXYZ)
from pyhmsa.spec.condition.specimen import SpecimenPosition
from pyhmsa.io.xmlhandler import _XMLHandler
from pyhmsa.util.parameter import ObjectAttribute

# Globals and constants variables.

class AcquisitionPointXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Acquisition' and element.get('Class') == 'Point'

    def parse(self, element):
        return self._parse_parameter(element, AcquisitionPoint)

    def can_convert(self, obj):
        return isinstance(obj, AcquisitionPoint)

    def convert(self, obj):
        return self._convert_parameter(obj, 'Acquisition', {'Class': 'Point'})

class AcquisitionMultipointXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._attrib_specimen_position = \
            ObjectAttribute(SpecimenPosition, xmlname='SpecimenPosition')

    def can_parse(self, element):
        return element.tag == 'Acquisition' and element.get('Class') == 'Multipoint'

    def parse(self, element):
        obj = self._parse_parameter(element, AcquisitionMultipoint)

        for subelement in element.findall('./Positions/SpecimenPosition'):
            position = \
                self._parse_object_attribute(subelement,
                                             self._attrib_specimen_position)
            obj.positions.append(position)

        subelement = element.find('PointCount')
        count = self._parse_numerical_attribute(subelement)
        assert len(obj.positions) == count

        return obj

    def can_convert(self, obj):
        return isinstance(obj, AcquisitionMultipoint)

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Acquisition', {'Class': 'Multipoint'})

        value = np.uint32(len(obj.positions))
        attrib = type('MockAttribute', (object,), {'xmlname': 'PointCount'})
        subelements = self._convert_numerical_attribute(value, attrib)
        element.extend(subelements)

        subelement = etree.Element('Positions')
        for position in obj.positions:
            subsubelements = \
                self._convert_object_attribute(position,
                                               self._attrib_specimen_position)
            subelement.extend(subsubelements)
        element.append(subelement)

        return element

class _AcquisitionRasterXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._attrib_specimen_position = \
            ObjectAttribute(SpecimenPosition, xmlname='SpecimenPosition')

    def _parse_positions(self, element):
        positions = {}

        for subelement in element.findall('SpecimenPosition'):
            location = subelement.attrib['Name']
            position = \
                self._parse_object_attribute(subelement,
                                             self._attrib_specimen_position)
            positions[location] = position

        return positions

    def _convert_positions(self, obj):
        elements = []

        for location, position in obj.positions.items():
            subelement = \
                self._convert_object_attribute(position,
                                               self._attrib_specimen_position)[0]
            subelement.set('Name', location)
            elements.append(subelement)

        return elements

class AcquisitionRasterLinescanXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Acquisition' and element.get('Class') == 'Raster/Linescan'

    def parse(self, element):
        obj = self._parse_parameter(element, AcquisitionRasterLinescan)
        obj.positions.update(self._parse_positions(element))
        return obj

    def can_convert(self, obj):
        return isinstance(obj, AcquisitionRasterLinescan)

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Acquisition', {'Class': 'Raster/Linescan'})
        element.extend(self._convert_positions(obj))
        return element

class AcquisitionRasterXYXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Acquisition' and element.get('Class') == 'Raster/XY'

    def parse(self, element):
        obj = self._parse_parameter(element, AcquisitionRasterXY)
        obj.positions.update(self._parse_positions(element))
        return obj

    def can_convert(self, obj):
        return isinstance(obj, AcquisitionRasterXY)

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Acquisition', {'Class': 'Raster/XY'})
        element.extend(self._convert_positions(obj))
        return element

class AcquisitionRasterXYZXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Acquisition' and element.get('Class') == 'Raster/XYZ'

    def parse(self, element):
        obj = self._parse_parameter(element, AcquisitionRasterXYZ)
        obj.positions.update(self._parse_positions(element))
        return obj

    def can_convert(self, obj):
        return isinstance(obj, AcquisitionRasterXYZ)

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Acquisition', {'Class': 'Raster/XYZ'})
        element.extend(self._convert_positions(obj))
        return element
