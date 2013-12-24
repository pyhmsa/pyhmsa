#!/usr/bin/env python
"""
================================================================================
:mod:`region` -- XML handler for region condition
================================================================================

.. module:: region
   :synopsis: XML handler for region condition

.. inheritance-diagram:: region

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
from pyhmsa.core.condition.region import RegionOfInterest
from pyhmsa.io.xml.handler import _XMLHandler

# Globals and constants variables.

class RegionOfInterestXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'RegionOfInterest'

    def from_xml(self, element):
        obj = self._parse_parameter(element, RegionOfInterest)

        subelement = element.find('StartChannel')
        if subelement is None:
            raise ValueError('Element StartChannel is missing')
        start = self._parse_numerical_attribute(subelement)

        subelement = element.find('EndChannel')
        if subelement is None:
            raise ValueError('Element EndChannel is missing')
        end = self._parse_numerical_attribute(subelement)

        obj.channels = (start, end)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, RegionOfInterest)

    def to_xml(self, obj):
        element = self._convert_parameter(obj, etree.Element('RegionOfInterest'))

        value = obj.start_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'StartChannel'})
        subelement = self._convert_numerical_attribute(value, attrib)
        element.append(subelement)

        value = obj.end_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'EndChannel'})
        subelement = self._convert_numerical_attribute(value, attrib)
        element.append(subelement)

        return element
