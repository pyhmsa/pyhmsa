#!/usr/bin/env python
"""
================================================================================
:mod:`numerical` -- XML handler for numerical value
================================================================================

.. module:: numerical
   :synopsis: XML handler for numerical value

.. inheritance-diagram:: numerical

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
import numpy as np

# Local modules.
from pyhmsa.type.numerical import NumericalValue, extract_value
from pyhmsa.io.xml.handler import _XMLHandler

# Globals and constants variables.

DTYPES_LOOKUP_FROM_XML = {'byte': np.uint8,
                          'int16': np.int16,
                          'uint16': np.uint16,
                          'int32': np.int32,
                          'uint32': np.uint32,
                          'int64': np.int64,
                          'float': np.float32,
                          'double': np.float64}

DTYPES_LOOKUP_TO_XML = {np.uint8: 'byte',
                        np.int16: 'int16',
                        np.uint16: 'uint16',
                        np.int32: 'int32',
                        np.uint32: 'uint32',
                        np.int64: 'int64',
                        np.float32: 'float',
                        np.float64: 'double'}

class NumericalXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return 'DataType' in element.attrib

    def from_xml(self, element):
        datatype = element.attrib['DataType']
        if datatype.startswith('array:'):
            dtype = DTYPES_LOOKUP_FROM_XML[datatype[6:]]
            value = np.array(list(map(float, element.text.split(','))), dtype=dtype)
            assert len(value) == int(element.attrib['Count'])
        else:
            dtype = DTYPES_LOOKUP_FROM_XML[datatype]
            value = dtype(float(element.text))

        unit = element.attrib.get('Unit')

        return extract_value(value, unit)

    def can_convert(self, obj):
        return isinstance(obj, (NumericalValue, np.generic, np.ndarray))

    def to_xml(self, obj):
        element = etree.Element('NumericalValue')

        if hasattr(obj, 'unit'):
            element.attrib['Unit'] = obj.unit
            value = obj.value
        else:
            value = obj

        datatype = DTYPES_LOOKUP_TO_XML[value.dtype.type]

        if np.isscalar(value):
            element.text = str(value)
        else:
            element.text = ','.join(map(str, value))
            element.attrib['Count'] = str(len(value))
            datatype = 'array:' + datatype

        element.attrib['DataType'] = datatype

        return element

