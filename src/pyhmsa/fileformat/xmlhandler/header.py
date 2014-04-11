#!/usr/bin/env python
"""
================================================================================
:mod:`header` -- XML handler for header
================================================================================

.. module:: header
   :synopsis: XML handler for header

.. inheritance-diagram:: header

"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.header import Header
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class HeaderXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Header'

    def parse(self, element):
        obj = self._parse_parameter(element, Header)

        for subelement in element:
            name = subelement.tag
            if name in obj:
                continue # already parsed
            obj[name] = subelement.text

        return obj

    def can_convert(self, obj):
        return isinstance(obj, Header)

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Header')

        for name, value in obj._extras.items():
            subelement = etree.Element(name)
            subelement.text = str(value)
            element.append(subelement)

        return element
