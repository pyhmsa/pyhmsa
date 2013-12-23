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

# Local modules.
from pyhmsa.core.condition.acquisition import \
    (_Acquisition, AcquisitionPoint, AcquisitionMultipoint, _AcquisitionRaster,
     AcquisitionRasterLinescan, AcquisitionRasterXY, AcquisitionRasterXYZ)
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler
from pyhmsa.io.xml.handlers.condition.specimen import SpecimenPositionXMLHandler

# Globals and constants variables.

class _AcquisitionXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Acquisition'

    def from_xml(self, element):
        kwargs = {}
        
        subelement = element.find('DwellTime')
        if subelement is not None:
            kwargs['dwell_time'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('TotalTime')
        if subelement is not None:
            kwargs['total_time'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('DwellTime_Live')
        if subelement is not None:
            kwargs['dwell_time_live'] = self._handler_numerical.from_xml(subelement)

        return _Acquisition(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, _Acquisition)

    def to_xml(self, obj):
        element = etree.Element('Acquisition')

        if obj.dwell_time:
            subelement = self._handler_numerical.to_xml(obj.dwell_time)
            subelement.tag = 'DwellTime'
            element.append(subelement)

        if obj.total_time:
            subelement = self._handler_numerical.to_xml(obj.total_time)
            subelement.tag = 'TotalTime'
            element.append(subelement)

        if obj.dwell_time_live:
            subelement = self._handler_numerical.to_xml(obj.dwell_time_live)
            subelement.tag = 'DwellTime_Live'
            element.append(subelement)

        return element

class AcquisitionPointXMLHandler(_AcquisitionXMLHandler):

    def __init__(self):
        _AcquisitionXMLHandler.__init__(self)
        self._handler_specimen_position = SpecimenPositionXMLHandler()

    def can_parse(self, element):
        if not _AcquisitionXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Point'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('SpecimenPosition')
        kwargs['position'] = self._handler_specimen_position.from_xml(subelement)

        obj = AcquisitionPoint(**kwargs)
        obj.__dict__.update(_AcquisitionXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, AcquisitionPoint)

    def to_xml(self, obj):
        element = _AcquisitionXMLHandler.to_xml(self, obj)
        element.set('Class', 'Point')

        subelement = self._handler_specimen_position.to_xml(obj.position)
        element.append(subelement)

        return element

class AcquisitionMultipointXMLHandler(_AcquisitionXMLHandler):

    def __init__(self):
        _AcquisitionXMLHandler.__init__(self)
        self._handler_specimen_position = SpecimenPositionXMLHandler()

    def can_parse(self, element):
        if not _AcquisitionXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Multipoint'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('PointCount')
        count = self._handler_numerical.from_xml(subelement)

        positions = []
        for subelement in element.findall('./Positions/SpecimenPosition'):
            positions.append(self._handler_specimen_position.from_xml(subelement))

        assert len(positions) == count
        kwargs['positions'] = positions

        obj = AcquisitionMultipoint(**kwargs)
        obj.__dict__.update(_AcquisitionXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, AcquisitionMultipoint)

    def to_xml(self, obj):
        element = _AcquisitionXMLHandler.to_xml(self, obj)
        element.set('Class', 'Multipoint')

        subelement = self._handler_numerical.to_xml(obj.point_count)
        subelement.tag = 'PointCount'
        element.append(subelement)

        subelement = etree.Element('Positions')
        for position in obj.positions:
            subsubelement = self._handler_specimen_position.to_xml(position)
            subelement.append(subsubelement)
        element.append(subelement)

        return element

class _AcquisitionRasterXMLHandler(_AcquisitionXMLHandler):

    def __init__(self):
        _AcquisitionXMLHandler.__init__(self)
        self._handler_specimen_position = SpecimenPositionXMLHandler()

    def can_parse(self, element):
        if not _AcquisitionXMLHandler.can_parse(self, element):
            return False
        return element.get('Class', '').startswith('Raster')

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('RasterMode')
        if subelement is not None:
            kwargs['raster_mode'] = subelement.text

        positions = {}
        for subelement in element.findall('SpecimenPosition'):
            location = subelement.attrib['Name']
            position = self._handler_specimen_position.from_xml(subelement)
            positions[location] = position

        kwargs['positions'] = positions

        obj = _AcquisitionRaster(**kwargs)
        obj.__dict__.update(_AcquisitionXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, _AcquisitionRaster)

    def to_xml(self, obj):
        element = _AcquisitionXMLHandler.to_xml(self, obj)
        element.set('Class', 'Raster')

        if obj.raster_mode:
            subelement = etree.Element('RasterMode')
            subelement.text = obj.raster_mode
            element.append(subelement)

        for location, position in obj.positions.items():
            subelement = self._handler_specimen_position.to_xml(position)
            subelement.set('Name', location)
            element.append(subelement)

        return element

class AcquisitionRasterLinescanXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        if not _AcquisitionRasterXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Raster/Linescan'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('StepCount')
        kwargs['step_count'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('StepSize')
        if subelement is not None:
            kwargs['step_size'] = self._handler_numerical.from_xml(subelement)

        obj = AcquisitionRasterLinescan(**kwargs)
        obj.__dict__.update(_AcquisitionRasterXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionRasterXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, AcquisitionRasterLinescan)

    def to_xml(self, obj):
        element = _AcquisitionRasterXMLHandler.to_xml(self, obj)
        element.set('Class', 'Raster/Linescan')

        subelement = self._handler_numerical.to_xml(obj.step_count)
        subelement.tag = 'StepCount'
        element.append(subelement)
        
        if obj.step_size:
            subelement = self._handler_numerical.to_xml(obj.step_size)
            subelement.tag = 'StepSize'
            element.append(subelement)

        return element

class AcquisitionRasterXYXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        if not _AcquisitionRasterXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Raster/XY'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('XStepCount')
        kwargs['step_count_x'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('YStepCount')
        kwargs['step_count_y'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('XStepSize')
        if subelement is not None:
            kwargs['step_size_x'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('YStepSize')
        if subelement is not None:
            kwargs['step_size_y'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('FrameCount')
        if subelement is not None:
            kwargs['frame_count'] = self._handler_numerical.from_xml(subelement)

        obj = AcquisitionRasterXY(**kwargs)
        obj.__dict__.update(_AcquisitionRasterXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionRasterXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, AcquisitionRasterXY)

    def to_xml(self, obj):
        element = _AcquisitionRasterXMLHandler.to_xml(self, obj)
        element.set('Class', 'Raster/XY')

        subelement = self._handler_numerical.to_xml(obj.step_count_x)
        subelement.tag = 'XStepCount'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.step_count_y)
        subelement.tag = 'YStepCount'
        element.append(subelement)

        if obj.step_size_x:
            subelement = self._handler_numerical.to_xml(obj.step_size_x)
            subelement.tag = 'XStepSize'
            element.append(subelement)

        if obj.step_size_y:
            subelement = self._handler_numerical.to_xml(obj.step_size_y)
            subelement.tag = 'YStepSize'
            element.append(subelement)

        if obj.frame_count:
            subelement = self._handler_numerical.to_xml(obj.frame_count)
            subelement.tag = 'FrameCount'
            element.append(subelement)

        return element

class AcquisitionRasterXYZXMLHandler(_AcquisitionRasterXMLHandler):

    def can_parse(self, element):
        if not _AcquisitionRasterXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Raster/XYZ'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('XStepCount')
        kwargs['step_count_x'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('YStepCount')
        kwargs['step_count_y'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ZStepCount')
        kwargs['step_count_z'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('XStepSize')
        if subelement is not None:
            kwargs['step_size_x'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('YStepSize')
        if subelement is not None:
            kwargs['step_size_y'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ZStepSize')
        if subelement is not None:
            kwargs['step_size_z'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ZRasterMode')
        if subelement is not None:
            kwargs['raster_mode_z'] = subelement.text

        obj = AcquisitionRasterXYZ(**kwargs)
        obj.__dict__.update(_AcquisitionRasterXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _AcquisitionRasterXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, AcquisitionRasterXYZ)

    def to_xml(self, obj):
        element = _AcquisitionRasterXMLHandler.to_xml(self, obj)
        element.set('Class', 'Raster/XYZ')

        subelement = self._handler_numerical.to_xml(obj.step_count_x)
        subelement.tag = 'XStepCount'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.step_count_y)
        subelement.tag = 'YStepCount'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.step_count_z)
        subelement.tag = 'ZStepCount'
        element.append(subelement)

        if obj.step_size_x:
            subelement = self._handler_numerical.to_xml(obj.step_size_x)
            subelement.tag = 'XStepSize'
            element.append(subelement)

        if obj.step_size_y:
            subelement = self._handler_numerical.to_xml(obj.step_size_y)
            subelement.tag = 'YStepSize'
            element.append(subelement)

        if obj.step_size_z:
            subelement = self._handler_numerical.to_xml(obj.step_size_z)
            subelement.tag = 'ZStepSize'
            element.append(subelement)

        if obj.raster_mode_z:
            subelement = etree.Element('ZRasterMode')
            subelement.text = obj.raster_mode_z
            element.append(subelement)

        return element
