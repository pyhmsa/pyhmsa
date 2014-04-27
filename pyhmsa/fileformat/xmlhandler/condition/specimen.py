#!/usr/bin/env python
"""
================================================================================
:mod:`specimen` -- Specimen XML handler
================================================================================

.. module:: specimen
   :synopsis: Specimen XML handler

.. inheritance-diagram:: specimen

"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimen import \
    Specimen, SpecimenMultilayer, SpecimenLayer
from pyhmsa.spec.condition.composition import CompositionElemental
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler
from pyhmsa.fileformat.xmlhandler.condition.composition import CompositionElementalXMLHandler

# Globals and constants variables.

class _SpecimenXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._handler_composition = CompositionElementalXMLHandler(version)

    def _parse_composition(self, element):
        subelement = element.find('Composition')
        if subelement is None:
            return CompositionElemental("wt%")
        return self._handler_composition.parse(subelement)

    def _convert_composition(self, obj):
        if obj.composition is None:
            return []
        return [self._handler_composition.convert(obj.composition)]

class SpecimenXMLHandler(_SpecimenXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Specimen'

    def parse(self, element):
        obj = self._parse_parameter(element, Specimen)
        obj.composition = self._parse_composition(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is Specimen

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Specimen')
        element.extend(self._convert_composition(obj))
        return element

class SpecimenLayerXMLHandler(_SpecimenXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Layer'

    def parse(self, element):
        obj = self._parse_parameter(element, SpecimenLayer)
        obj.name = element.get('Name')
        obj.composition = self._parse_composition(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is Specimen

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Layer')
        if obj.name is not None:
            element.set('Name', obj.name)
        element.extend(self._convert_composition(obj))
        return element

class SpecimenMultilayerXMLHandler(_SpecimenXMLHandler):

    def __init__(self, version):
        _SpecimenXMLHandler.__init__(self, version)
        self._handler_layer = SpecimenLayerXMLHandler(version)

    def can_parse(self, element):
        return element.tag == 'Specimen' and element.get('Class') == 'Multilayer'

    def parse(self, element):
        obj = self._parse_parameter(element, SpecimenMultilayer)
        obj.composition = self._parse_composition(element)

        for subelement in element.findall('Layers/Layer'):
            layer = self._handler_layer.parse(subelement)
            obj.layers.append(layer)

        return obj

    def can_convert(self, obj):
        return type(obj) is SpecimenMultilayer

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Specimen', {'Class': 'Multilayer'})
        element.extend(self._convert_composition(obj))

        subelement = etree.Element('Layers')
        for layer in obj.layers:
            subsubelement = self._handler_layer.convert(layer)
            subelement.append(subsubelement)
        element.append(subelement)

        return element
