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
from pyhmsa.spec.header import Header
from pyhmsa.io.xmlhandler import _XMLHandler

# Globals and constants variables.

class HeaderXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Header'

    def parse(self, element):
        obj = self._parse_parameter(element, Header)

        for subelement in element.iter():
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
