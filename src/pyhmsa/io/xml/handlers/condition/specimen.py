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
from pyhmsa.core.condition.specimen import \
    SpecimenPosition, Specimen, SpecimenMultilayer, Composition, SpecimenLayer
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class SpecimenPositionXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'SpecimenPosition'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('X')
        if subelement is not None:
            kwargs['x'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Y')
        if subelement is not None:
            kwargs['y'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Z')
        if subelement is not None:
            kwargs['z'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('R')
        if subelement is not None:
            kwargs['r'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('T')
        if subelement is not None:
            kwargs['t'] = self._handler_numerical.from_xml(subelement)

        return SpecimenPosition(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, SpecimenPosition)

    def to_xml(self, obj):
        element = etree.Element('SpecimenPosition')

        if obj.x:
            subelement = self._handler_numerical.to_xml(obj.x)
            subelement.tag = 'X'
            element.append(subelement)

        if obj.y:
            subelement = self._handler_numerical.to_xml(obj.y)
            subelement.tag = 'Y'
            element.append(subelement)

        if obj.z:
            subelement = self._handler_numerical.to_xml(obj.z)
            subelement.tag = 'Z'
            element.append(subelement)

        if obj.r:
            subelement = self._handler_numerical.to_xml(obj.r)
            subelement.tag = 'R'
            element.append(subelement)

        if obj.t:
            subelement = self._handler_numerical.to_xml(obj.t)
            subelement.tag = 'T'
            element.append(subelement)

        return element

class CompositionXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Composition'

    def from_xml(self, element):
        units = []
        tmpcomposition = {}
        for subelement in element.findall('Element'):
            z = int(subelement.attrib['Z'])
            fraction, unit = self._handler_numerical.from_xml(subelement)
            units.append(unit)
            tmpcomposition.setdefault(z, fraction)

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

        for z, fraction in obj.items():
            subelement = self._handler_numerical.to_xml(fraction)
            subelement.tag = 'Element'
            subelement.set('Unit', obj.unit)
            subelement.set('Z', str(z))
            element.append(subelement)

        return element

class SpecimenXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()
        self._handler_composition = CompositionXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Specimen'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Name')
        kwargs['name'] = subelement.text

        subelement = element.find('Description')
        if subelement is not None:
            kwargs['description'] = subelement.text

        subelement = element.find('Origin')
        if subelement is not None:
            kwargs['origin'] = subelement.text

        subelement = element.find('Formula')
        if subelement is not None:
            kwargs['formula'] = subelement.text

        subelement = element.find('Composition')
        if subelement is not None:
            kwargs['composition'] = self._handler_composition.from_xml(subelement)

        subelement = element.find('Temperature')
        if subelement is not None:
            kwargs['temperature'] = self._handler_numerical.from_xml(subelement)

        return Specimen(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, Specimen)

    def to_xml(self, obj):
        element = etree.Element('Specimen')

        subelement = etree.Element('Name')
        subelement.text = obj.name
        element.append(subelement)

        if obj.description:
            subelement = etree.Element('Description')
            subelement.text = obj.description
            element.append(subelement)

        if obj.origin:
            subelement = etree.Element('Origin')
            subelement.text = obj.origin
            element.append(subelement)

        if obj.formula:
            subelement = etree.Element('Formula')
            subelement.text = obj.formula
            element.append(subelement)

        if obj.composition:
            subelement = self._handler_composition.to_xml(obj.composition)
            element.append(subelement)

        if obj.temperature:
            subelement = self._handler_numerical.to_xml(obj.temperature)
            subelement.tag = 'Temperature'
            element.append(subelement)

        return element

class SpecimenMultilayerXMLHandler(SpecimenXMLHandler):

    def can_parse(self, element):
        if not SpecimenXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Multilayer'

    def from_xml(self, element):
        kwargs = {}

        layers = []
        for subelement in element.findall('Layers/Layer'):
            subkwargs = {}

            subkwargs['name'] = subelement.get('Name')

            subsubelement = subelement.find('Thickness')
            if subsubelement is not None:
                subkwargs['thickness'] = self._handler_numerical.from_xml(subsubelement)

            subsubelement = subelement.find('Formula')
            if subsubelement is not None:
                subkwargs['formula'] = subsubelement.text

            subsubelement = subelement.find('Composition')
            if subsubelement is not None:
                subkwargs['composition'] = self._handler_composition.from_xml(subsubelement)

            layers.append(SpecimenLayer(**subkwargs))

        kwargs['layers'] = layers

        parent = SpecimenXMLHandler.from_xml(self, element)
        obj = SpecimenMultilayer(parent.name, **kwargs)
        obj.__dict__.update(parent.__dict__)
        return obj

    def can_convert(self, obj):
        if not SpecimenXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, SpecimenMultilayer)

    def to_xml(self, obj):
        element = SpecimenXMLHandler.to_xml(self, obj)
        element.set('Class', 'Multilayer')

        subelement = etree.Element('Layers')

        for layer in obj.layers:
            subsubelement = etree.Element('Layer')

            if layer.name:
                subsubelement.set('Name', layer.name)

            if layer.thickness:
                subsubsubelement = self._handler_numerical.to_xml(layer.thickness)
                subsubsubelement.tag = 'Thickness'
                subsubelement.append(subsubsubelement)

            if layer.formula:
                subsubsubelement = etree.Element('Formula')
                subsubsubelement.text = layer.formula
                subsubelement.append(subsubsubelement)

            if layer.composition:
                subsubsubelement = self._handler_composition.to_xml(layer.composition)
                subsubelement.append(subsubsubelement)

            subelement.append(subsubelement)

        element.append(subelement)

        return element
