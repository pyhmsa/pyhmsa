#!/usr/bin/env python
"""
================================================================================
:mod:`header` -- XML handler for header
================================================================================

.. module:: header
   :synopsis: XML handler for header

.. inheritance-diagram:: header

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
from pyhmsa.core.header import Header
from pyhmsa.io.xmlhandler import _XMLHandler

# Globals and constants variables.

class HeaderXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Header'

    def from_xml(self, element):
        obj = self._parse_parameter(element, Header)

        for subelement in element.iter():
            name = subelement.tag.lower()
            if hasattr(obj, name):
                continue # already parsed
            obj[name] = subelement.text

        return obj

    def can_convert(self, obj):
        return isinstance(obj, Header)

    def to_xml(self, obj):
        element = self._convert_parameter(obj, etree.Element('Header'))

        for name, value in obj.__dict__.items():
            if name in obj.__class__.__dict__:
                continue # already converted

            subelement = etree.Element(name.title())
            subelement.text = str(value)

            element.append(subelement)

        return element
