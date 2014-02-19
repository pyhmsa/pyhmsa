#!/usr/bin/env python
"""
================================================================================
:mod:`analysislist` -- XML analysis for analysis list data
================================================================================

.. module:: analysislist
   :synopsis: XML analysis for analysis list data

.. inheritance-diagram:: pyhmsa.fileformat.xmlhandler.datum.analysislist

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
import numpy as np

# Local modules.
from pyhmsa.fileformat.xmlhandler.datum.datum import _DatumXMLHandler
from pyhmsa.spec.datum.analysislist import AnalysisList0D, AnalysisList1D, AnalysisList2D

# Globals and constants variables.

class AnalysisList0DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'AnalysisList' and element.get('Class') == '0D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        collections = self._parse_collection_dimensions(element)
        if "Analysis" not in collections:
            raise ValueError('Analysis dimension is required')
        analysis_count = collections['Analysis']

        conditions = self._parse_include_conditions(element)

        buffer = self._parse_binary(element)

        return AnalysisList0D(analysis_count, dtype, buffer,
                              conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, AnalysisList0D)

    def convert(self, obj):
        element = etree.Element('AnalysisList', {'Class': '0D'})
        element.extend(self._convert(obj))
        self._convert_binary(obj)
        return element

class AnalysisList1DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'AnalysisList' and element.get('Class') == '1D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if "Channel" not in dimensions:
            raise ValueError('Channel dimension is required')
        channel = dimensions['Channel']

        collections = self._parse_collection_dimensions(element)
        if "Analysis" not in collections:
            raise ValueError('Analysis dimension is required')
        analysis_count = collections['Analysis']

        conditions = self._parse_include_conditions(element)

        buffer = self._parse_binary(element)
        buffer = np.reshape(buffer, (channel, analysis_count), order='F')
        buffer = np.rollaxis(buffer, 0, 2)
        buffer = np.ravel(buffer)

        return AnalysisList1D(analysis_count, channel, dtype, buffer,
                              conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, AnalysisList1D)

    def convert(self, obj):
        element = etree.Element('AnalysisList', {'Class': '1D'})
        element.extend(self._convert(obj))

        buffer = np.rollaxis(obj, 1, 0)
        self._convert_binary(buffer)

        return element

class AnalysisList2DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'AnalysisList' and element.get('Class') == '2D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if "U" not in dimensions:
            raise ValueError('U dimension is required')
        u = dimensions['U']

        if "V" not in dimensions:
            raise ValueError('V dimension is required')
        v = dimensions['V']

        collections = self._parse_collection_dimensions(element)
        if "Analysis" not in collections:
            raise ValueError('Analysis dimension is required')
        analysis_count = collections['Analysis']

        conditions = self._parse_include_conditions(element)

        buffer = self._parse_binary(element)
        buffer = np.reshape(buffer, (u, v, analysis_count), order='F')
        buffer = np.rollaxis(buffer, 2, 0)
        buffer = np.ravel(buffer)

        return AnalysisList2D(analysis_count, u, v, dtype, buffer,
                              conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, AnalysisList2D)

    def convert(self, obj):
        element = etree.Element('AnalysisList', {'Class': '2D'})
        element.extend(self._convert(obj))

        buffer = np.rollaxis(obj, 0, 3)
        self._convert_binary(buffer)

        return element
