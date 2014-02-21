#!/usr/bin/env python
"""
================================================================================
:mod:`datum` -- XML handler for datum
================================================================================

.. module:: datum
   :synopsis: XML handler for datum

.. inheritance-diagram:: datum

"""

# Standard library modules.
import xml.etree.ElementTree as etree
from collections import OrderedDict
import array

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.fileformat.xmlhandler.xmlhandler import \
    _XMLHandler, DTYPES_LOOKUP_PARSE, DTYPES_LOOKUP_CONVERT

# Globals and constants variables.

class _DatumXMLHandler(_XMLHandler):

    def __init__(self, version, hmsa_file, conditions):
        _XMLHandler.__init__(self, version)
        if hmsa_file.closed:
            raise ValueError('HMSA file object is closed')
#        if not hmsa_file.seekable():
#            raise ValueError('HMSA file object is not seekable')
        self._hmsa_file = hmsa_file
        self._conditions = conditions

    def _parse_data_offset(self, element):
        subelement = element.find('DataOffset')
        if subelement is None:
            raise ValueError('Element DataOffset is missing')
        return self._parse_numerical_attribute(subelement)

    def _convert_data_offset(self, obj):
        attrib = type('MockAttribute', (object,), {'xmlname': 'DataOffset'})
        value = np.int64(self._hmsa_file.tell())
        return self._convert_numerical_attribute(value, attrib)

    def _parse_data_length(self, element):
        subelement = element.find('DataLength')
        if subelement is None:
            raise ValueError('Element DataLength is missing')
        return self._parse_numerical_attribute(subelement)

    def _convert_data_length(self, obj):
        attrib = type('MockAttribute', (object,), {'xmlname': 'DataLength'})
        value = np.int64(obj.size * obj.itemsize)
        return self._convert_numerical_attribute(value, attrib)

    def _parse_datum_type(self, element):
        subelement = element.find('DatumType')
        if subelement is None:
            raise ValueError('Element DatumType is missing')

        dtype = DTYPES_LOOKUP_PARSE[subelement.text]
        dtype = dtype.newbyteorder('<') # Force little endian

        assert dtype.itemsize == int(subelement.get('SizeInBytes'))

        return dtype

    def _convert_datum_type(self, obj):
        element = etree.Element('DatumType')
        element.text = DTYPES_LOOKUP_CONVERT[obj.dtype]
        element.set('SizeInBytes', str(obj.dtype.itemsize))
        return [element]

    def _parse_datum_dimensions(self, element):
        dimensions = OrderedDict()

        for subelement in element.findall('DatumDimensions/Dimension'):
            key = subelement.get('Name')
            value = self._parse_numerical_attribute(subelement)
            dimensions[key] = value

        return dimensions

    def _convert_datum_dimensions(self, obj):
        element = etree.Element('DatumDimensions')

        attrib = type('MockAttribute', (object,), {'xmlname': 'Dimension'})
        for name, value in obj.datum_dimensions.items():
            subelement = self._convert_numerical_attribute(value, attrib)[0]
            subelement.set('Name', name)
            element.append(subelement)

        return [element]

    def _parse_collection_dimensions(self, element):
        dimensions = OrderedDict()

        for subelement in element.findall('CollectionDimensions/Dimension'):
            key = subelement.get('Name')
            value = self._parse_numerical_attribute(subelement)
            dimensions[key] = value

        return dimensions

    def _convert_collection_dimensions(self, obj):
        element = etree.Element('CollectionDimensions')

        attrib = type('MockAttribute', (object,), {'xmlname': 'Dimension'})
        for name, value in obj.collection_dimensions.items():
            subelement = self._convert_numerical_attribute(value, attrib)[0]
            subelement.set('Name', name)
            element.append(subelement)

        return [element]

    def _parse_include_conditions(self, element):
        conditions = Conditions()

        for subelement in element.findall('IncludeConditions/*'):
            identifier = subelement.text
            condition = self._conditions[identifier]
            conditions[identifier] = condition

        return conditions

    def _convert_include_conditions(self, obj):
        element = etree.Element('IncludeConditions')

        for identifier, condition in obj.conditions.items():
            subelement = etree.Element(condition.TEMPLATE)
            subelement.text = identifier
            element.append(subelement)

        return [element]

    def _parse_binary(self, element):
        offset = self._parse_data_offset(element)
        dtype = self._parse_datum_type(element)
        length = self._parse_data_length(element)

        self._hmsa_file.seek(offset)
        return np.fromfile(self._hmsa_file, dtype, length // dtype.itemsize)

    def _convert_binary(self, obj):
        arr = array.array(obj.dtype.char, obj.ravel(order='F'))
        arr.tofile(self._hmsa_file)
        del arr

    def _convert(self, obj):
        elements = []

        elements.extend(self._convert_data_offset(obj))
        elements.extend(self._convert_data_length(obj))
        elements.extend(self._convert_datum_type(obj))
        elements.extend(self._convert_datum_dimensions(obj))
        elements.extend(self._convert_collection_dimensions(obj))
        elements.extend(self._convert_include_conditions(obj))

        return elements
