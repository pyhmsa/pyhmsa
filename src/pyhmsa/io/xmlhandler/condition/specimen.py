#!/usr/bin/env python
"""
================================================================================
:mod:`specimen` -- Specimen XML handler
================================================================================

.. module:: specimen
   :synopsis: Specimen XML handler

.. inheritance-diagram:: specimen

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
from pyhmsa.spec.condition.specimen import \
    SpecimenPosition, Specimen, SpecimenMultilayer, Composition, SpecimenLayer
from pyhmsa.io.xmlhandler import _XMLHandler

# Globals and constants variables.

class SpecimenPositionXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'SpecimenPosition'

    def from_xml(self, element):
        return self._parse_parameter(element, SpecimenPosition)

    def can_convert(self, obj):
        return isinstance(obj, SpecimenPosition)

    def to_xml(self, obj):
        return self._convert_parameter(obj, etree.Element('SpecimenPosition'))

class CompositionXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Composition'

    def from_xml(self, element):
        units = []
        tmpcomposition = {}
        for subelement in element.findall('Element'):
            z = int(subelement.attrib['Z'])
            value = self._parse_numerical_attribute(subelement)
            units.append(value.unit)
            tmpcomposition.setdefault(z, value)

        # Check units
        units = set(units)
        if not units:
            return None
        if len(units) > 1:
            raise ValueError('Incompatible unit in composition')
        unit = list(units)[0]

        composition = Composition(unit)
        composition.update(tmpcomposition)
        return composition

    def can_convert(self, obj):
        return isinstance(obj, Composition)

    def to_xml(self, obj):
        element = etree.Element('Composition')

        attrib = type('MockAttribute', (object,), {'xmlname': 'Element'})
        for z, fraction in obj.items():
            subelement = self._convert_numerical_attribute(fraction, attrib)
            subelement.set('Unit', obj.unit)
            subelement.set('Z', str(z))
            element.append(subelement)

        return element

class _SpecimenXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._handler_composition = CompositionXMLHandler(version)

    def _parse_composition(self, element):
        subelement = element.find('Composition')
        if subelement is None:
            return Composition("wt%")
        return self._handler_composition.from_xml(subelement)

    def _convert_composition(self, value, element):
        if value is None:
            return element
        element.append(self._handler_composition.to_xml(value))
        return element

class SpecimenXMLHandler(_SpecimenXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Specimen'

    def from_xml(self, element):
        obj = self._parse_parameter(element, Specimen)
        obj.composition = self._parse_composition(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, Specimen)

    def to_xml(self, obj):
        element = self._convert_parameter(obj, etree.Element('Specimen'))
        element = self._convert_composition(obj.composition, element)
        return element

class SpecimenLayerXMLHandler(_SpecimenXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Layer'

    def from_xml(self, element):
        obj = self._parse_parameter(element, SpecimenLayer)
        obj.name = element.get('Name')
        obj.composition = self._parse_composition(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, Specimen)

    def to_xml(self, obj):
        element = self._convert_parameter(obj, etree.Element('Layer'))
        if obj.name is not None:
            element.set('Name', obj.name)
        element = self._convert_composition(obj.composition, element)
        return element

class SpecimenMultilayerXMLHandler(_SpecimenXMLHandler):

    def __init__(self, version):
        _SpecimenXMLHandler.__init__(self, version)
        self._handler_layer = SpecimenLayerXMLHandler(version)

    def can_parse(self, element):
        return element.tag == 'Specimen' and element.get('Class') == 'Multilayer'

    def from_xml(self, element):
        obj = self._parse_parameter(element, SpecimenMultilayer)
        obj.composition = self._parse_composition(element)

        for subelement in element.findall('Layers/Layer'):
            layer = self._handler_layer.from_xml(subelement)
            obj.layers.append(layer)

        return obj

    def can_convert(self, obj):
        return isinstance(obj, SpecimenMultilayer)

    def to_xml(self, obj):
        element = etree.Element('Specimen', {'Class': 'Multilayer'})
        element = self._convert_parameter(obj, element)
        element = self._convert_composition(obj.composition, element)

        subelement = etree.Element('Layers')
        for layer in obj.layers:
            subsubelement = self._handler_layer.to_xml(layer)
            subelement.append(subsubelement)
        element.append(subelement)

        return element
