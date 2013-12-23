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
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class RegionOfInterestXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'RegionOfInterest'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('StartChannel')
        kwargs['start_channel'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('EndChannel')
        kwargs['end_channel'] = self._handler_numerical.from_xml(subelement)

        return RegionOfInterest(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, RegionOfInterest)

    def to_xml(self, obj):
        element = etree.Element('RegionOfInterest')

        subelement = self._handler_numerical.to_xml(obj.start_channel)
        subelement.tag = 'StartChannel'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.end_channel)
        subelement.tag = 'EndChannel'
        element.append(subelement)

        return element
