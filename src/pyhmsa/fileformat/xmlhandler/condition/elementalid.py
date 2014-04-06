#!/usr/bin/env python
"""
================================================================================
:mod:`elementid` -- XML handler for element id condition
================================================================================

.. module:: elementid
   :synopsis: XML handler for element id condition

.. inheritance-diagram:: elementid

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.elementalid import ElementalID, ElementalIDXray
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class ElementalIDXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'ElementalID'

    def parse(self, element):
        return self._parse_parameter(element, ElementalID)

    def can_convert(self, obj):
        return type(obj) is ElementalID

    def convert(self, obj):
        element = self._convert_parameter(obj, 'ElementalID')
        element.find('Element').set('Symbol', obj.symbol) # manually add symbol
        return element

class ElementalIDXrayXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'ElementalID' and element.get('Class') == 'X-ray'

    def parse(self, element):
        return self._parse_parameter(element, ElementalIDXray)

    def can_convert(self, obj):
        return type(obj) is ElementalIDXray

    def convert(self, obj):
        element = self._convert_parameter(obj, 'ElementalID', {'Class': 'X-ray'})
        element.find('Element').set('Symbol', obj.symbol) # manually add symbol
        return element
