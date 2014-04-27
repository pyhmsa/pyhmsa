#!/usr/bin/env python
"""
================================================================================
:mod:`analysis` -- XML analysis for analysis data
================================================================================

.. module:: analysis
   :synopsis: XML analysis for analysis data

.. inheritance-diagram:: analysis

"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.datum.datum import _DatumXMLHandler
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D

# Globals and constants variables.

class Analysis0DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Analysis' and element.get('Class') == '0D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        if element is not None and len(element.text) != 0:
            value = dtype.type(float(element.text))
        else:
            value = self._parse_binary(element)

        conditions = self._parse_include_conditions(element)

        return Analysis0D(value, dtype, conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, Analysis0D)

    def convert(self, obj):
        element = etree.Element('Analysis', {'Class': '0D'})
        element.extend(self._convert(obj))
        element.text = str(obj)
        return element

class Analysis1DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Analysis' and element.get('Class') == '1D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if 'Channel' not in dimensions:
            raise ValueError('Channel dimension is required')
        channel = dimensions['Channel']

        buffer = self._parse_binary(element)

        conditions = self._parse_include_conditions(element)

        return Analysis1D(channel, dtype, buffer, order='F', conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, Analysis1D)

    def convert(self, obj):
        element = etree.Element('Analysis', {'Class': '1D'})
        element.extend(self._convert(obj))
        self._convert_binary(obj)
        return element

class Analysis2DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Analysis' and element.get('Class') == '2D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if 'U' not in dimensions:
            raise ValueError('U dimension is required')
        u = dimensions['U']
        if 'V' not in dimensions:
            raise ValueError('V dimension is required')
        v = dimensions['V']

        buffer = self._parse_binary(element)

        conditions = self._parse_include_conditions(element)

        return Analysis2D(u, v, dtype, buffer, order='F', conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, Analysis2D)

    def convert(self, obj):
        element = etree.Element('Analysis', {'Class': '2D'})
        element.extend(self._convert(obj))
        self._convert_binary(obj)
        return element
