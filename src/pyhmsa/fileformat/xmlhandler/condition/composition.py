#!/usr/bin/env python
"""
================================================================================
:mod:`composition` -- Composition XML handler
================================================================================

.. module:: composition
   :synopsis: Composition XML handler

.. inheritance-diagram:: pyhmsa.fileformat.xmlhandler.condition.composition

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.composition import CompositionElemental
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class CompositionElementalXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Composition' and element.get('Class') == 'Elemental'

    def parse(self, element):
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

        composition = CompositionElemental(unit)
        composition.update(tmpcomposition)
        return composition

    def can_convert(self, obj):
        return type(obj) is CompositionElemental

    def convert(self, obj):
        element = etree.Element('Composition', {'Class': 'Elemental'})

        attrib = type('MockAttribute', (object,), {'xmlname': 'Element'})
        for z, fraction in obj.items():
            subelement = self._convert_numerical_attribute(fraction, attrib)[0]
            subelement.set('Unit', obj.unit)
            subelement.set('Z', str(z))
            element.append(subelement)

        return element