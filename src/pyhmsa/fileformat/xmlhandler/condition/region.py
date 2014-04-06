#!/usr/bin/env python
"""
================================================================================
:mod:`region` -- XML handler for region condition
================================================================================

.. module:: region
   :synopsis: XML handler for region condition

.. inheritance-diagram:: region

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.region import RegionOfInterest
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class RegionOfInterestXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'RegionOfInterest'

    def parse(self, element):
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
        return type(obj) is RegionOfInterest

    def convert(self, obj):
        element = self._convert_parameter(obj, 'RegionOfInterest')

        value = obj.start_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'StartChannel'})
        subelements = self._convert_numerical_attribute(value, attrib)
        element.extend(subelements)

        value = obj.end_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'EndChannel'})
        subelements = self._convert_numerical_attribute(value, attrib)
        element.extend(subelements)

        return element
