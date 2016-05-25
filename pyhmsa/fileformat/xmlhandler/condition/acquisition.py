"""
XML handler for acquisition classes
"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.condition.acquisition import \
    (AcquisitionPoint, AcquisitionMultipoint,
     AcquisitionRasterLinescan, AcquisitionRasterXY, AcquisitionRasterXYZ)
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler
from pyhmsa.util.parameter import ObjectAttribute

# Globals and constants variables.

class AcquisitionPointXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(AcquisitionPoint, version)

class AcquisitionMultipointXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(AcquisitionMultipoint, version)
        self._attrib_specimen_position = \
            ObjectAttribute(SpecimenPosition, xmlname='SpecimenPosition')

    def parse(self, element):
        obj = super().parse(element)

        for subelement in element.findall('./Positions/SpecimenPosition'):
            position = \
                self._parse_object_attribute(subelement,
                                             self._attrib_specimen_position)
            obj.positions.append(position)

        subelement = element.find('PointCount')
        count = self._parse_numerical_attribute(subelement)
        assert len(obj.positions) == count

        return obj

    def convert(self, obj):
        element = super().convert(obj)

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

class _AcquisitionRasterXMLHandler(_ConditionXMLHandler):

    def __init__(self, clasz, version):
        super().__init__(clasz, version)
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

    def parse(self, element):
        obj = super().parse(element)
        obj.positions.update(self._parse_positions(element))
        return obj

    def _convert_positions(self, obj):
        elements = []

        for location, position in obj.positions.items():
            subelement = \
                self._convert_object_attribute(position,
                                               self._attrib_specimen_position)[0]
            subelement.set('Name', location)
            elements.append(subelement)

        return elements

    def convert(self, obj):
        element = super().convert(obj)
        element.extend(self._convert_positions(obj))
        return element

class AcquisitionRasterLinescanXMLHandler(_AcquisitionRasterXMLHandler):

    def __init__(self, version):
        super().__init__(AcquisitionRasterLinescan, version)

class AcquisitionRasterXYXMLHandler(_AcquisitionRasterXMLHandler):

    def __init__(self, version):
        super().__init__(AcquisitionRasterXY, version)

class AcquisitionRasterXYZXMLHandler(_AcquisitionRasterXMLHandler):

    def __init__(self, version):
        super().__init__(AcquisitionRasterXYZ, version)

