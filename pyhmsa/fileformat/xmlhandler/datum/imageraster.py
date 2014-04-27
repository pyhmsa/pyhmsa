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
import numpy as np

# Local modules.
from pyhmsa.fileformat.xmlhandler.datum.datum import _DatumXMLHandler
from pyhmsa.spec.datum.imageraster import \
    ImageRaster2D, ImageRaster2DSpectral, ImageRaster2DHyperimage

# Globals and constants variables.

class ImageRaster2DXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'ImageRaster' and element.get('Class') == '2D'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        collections = self._parse_collection_dimensions(element)
        if 'X' not in collections:
            raise ValueError('X dimension is required')
        x = collections['X']
        if 'Y' not in collections:
            raise ValueError('X dimension is required')
        y = collections['Y']

        buffer = self._parse_binary(element)

        conditions = self._parse_include_conditions(element)

        return ImageRaster2D(x, y, dtype, buffer, order='F',
                             conditions=conditions)

    def can_convert(self, obj):
        return isinstance(obj, ImageRaster2D)

    def convert(self, obj):
        element = etree.Element('ImageRaster', {'Class': '2D'})
        element.extend(self._convert(obj))
        self._convert_binary(obj)
        return element

class ImageRaster2DSpectralXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'ImageRaster' and element.get('Class') == '2D/Spectral'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if 'Channel' not in dimensions:
            raise ValueError('Channel dimension is required')
        channel = dimensions['Channel']

        collections = self._parse_collection_dimensions(element)
        if 'X' not in collections:
            raise ValueError('X dimension is required')
        x = collections['X']
        if 'Y' not in collections:
            raise ValueError('X dimension is required')
        y = collections['Y']

        conditions = self._parse_include_conditions(element)

        buffer = self._parse_binary(element)
        buffer = np.reshape(buffer, (channel, x, y), order='F')
        buffer = np.rollaxis(buffer, 0, 3)
        buffer = np.ravel(buffer)

        datum = ImageRaster2DSpectral(x, y, channel, dtype, buffer,
                                      conditions=conditions)

        return datum

    def can_convert(self, obj):
        return isinstance(obj, ImageRaster2DSpectral)

    def convert(self, obj):
        element = etree.Element('ImageRaster', {'Class': '2D/Spectral'})
        element.extend(self._convert(obj))

        buffer = np.rollaxis(obj, 2, 0)
        self._convert_binary(buffer)

        return element

class ImageRaster2DHyperimageXMLHandler(_DatumXMLHandler):

    def can_parse(self, element):
        return element.tag == 'ImageRaster' and element.get('Class') == '2D/Hyperimage'

    def parse(self, element):
        dtype = self._parse_datum_type(element)

        dimensions = self._parse_datum_dimensions(element)
        if 'U' not in dimensions:
            raise ValueError('U dimension is required')
        u = dimensions['U']
        if 'V' not in dimensions:
            raise ValueError('V dimension is required')
        v = dimensions['V']

        collections = self._parse_collection_dimensions(element)
        if 'X' not in collections:
            raise ValueError('X dimension is required')
        x = collections['X']
        if 'Y' not in collections:
            raise ValueError('X dimension is required')
        y = collections['Y']

        conditions = self._parse_include_conditions(element)

        buffer = self._parse_binary(element)
        buffer = np.reshape(buffer, (u, v, x, y), order='F')
        buffer = np.rollaxis(np.rollaxis(buffer, 0, 4), 0, 4)
        buffer = np.ravel(buffer)

        datum = ImageRaster2DHyperimage(x, y, u, v, dtype, buffer,
                                        conditions=conditions)

        return datum

    def can_convert(self, obj):
        return isinstance(obj, ImageRaster2DHyperimage)

    def convert(self, obj):
        element = etree.Element('ImageRaster', {'Class': '2D/Hyperimage'})
        element.extend(self._convert(obj))

        buffer = np.rollaxis(np.rollaxis(obj, 2, 0), 3, 1)
        self._convert_binary(buffer)

        return element