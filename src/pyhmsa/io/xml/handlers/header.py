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
from pyhmsa.io.xml.handler import _XMLHandler

# Globals and constants variables.

class HeaderXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Header'

    def from_xml(self, element):
        header = Header()
        
        for subelement in element:
            header[subelement.tag] = subelement.text

        return header

    def can_convert(self, obj):
        return isinstance(obj, Header)

    def to_xml(self, obj):
        element = etree.Element('Header')

        for tag, value in obj.items():
            subelement = etree.Element(tag)

            if tag == 'Date':
                pass
            else:
                subelement.text = str(value)

            element.append(subelement)

        return element
