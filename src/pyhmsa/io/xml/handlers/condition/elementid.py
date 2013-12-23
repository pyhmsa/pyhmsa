#!/usr/bin/env python
"""
================================================================================
:mod:`elementid` -- XML handler for element id condition
================================================================================

.. module:: elementid
   :synopsis: XML handler for element id condition

.. inheritance-diagram:: elementid

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
from pyhmsa.core.condition.elementid import ElementID, ElementIDXray
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class ElementIDXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'ElementID'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Element')
        kwargs['z'] = self._handler_numerical.from_xml(subelement)

        return ElementID(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, ElementID)

    def to_xml(self, obj):
        element = etree.Element('ElementID')

        subelement = self._handler_numerical.to_xml(obj.z)
        subelement.tag = 'Element'
        subelement.set('Symbol', obj.symbol)
        element.append(subelement)

        return element

class ElementIDXrayXMLHandler(ElementIDXMLHandler):

    def can_parse(self, element):
        if not ElementIDXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'X-ray'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Line')
        kwargs['line'] = subelement.text
        
        subelement = element.find('Energy')
        if subelement is not None:
            kwargs['energy'] = self._handler_numerical.from_xml(subelement)

        parent = ElementIDXMLHandler.from_xml(self, element)
        return ElementIDXray(parent.z, **kwargs)

    def can_convert(self, obj):
        if not ElementIDXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, ElementIDXray)

    def to_xml(self, obj):
        element = ElementIDXMLHandler.to_xml(self, obj)
        element.set('Class', 'X-ray')

        subelement = etree.Element('Line')
        subelement.text = obj.line
        element.append(subelement)

        if obj.energy:
            subelement = self._handler_numerical.to_xml(obj.energy)
            subelement.tag = 'Energy'
            element.append(subelement)

        return element
