#!/usr/bin/env python
"""
================================================================================
:mod:`xmlhandler` -- Handler to convert core objects to XML
================================================================================

.. module:: xmlhandler
   :synopsis: Handler to convert core objects to XML

.. inheritance-diagram:: xmlhandler

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import xml.etree.ElementTree as etree
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.numerical import convert_value
from pyhmsa.type.language import langstr
from pyhmsa.type.checksum import Checksum
from pyhmsa.util.parameter import \
    (NumericalAttribute, TextAttribute, ObjectAttribute, DateAttribute,
     TimeAttribute, ChecksumAttribute)

# Globals and constants variables.
DTYPES_LOOKUP_parse = {'byte': np.dtype(np.uint8),
                          'int16': np.dtype(np.int16),
                          'uint16': np.dtype(np.uint16),
                          'int32': np.dtype(np.int32),
                          'uint32': np.dtype(np.uint32),
                          'int64': np.dtype(np.int64),
                          'float': np.dtype(np.float32),
                          'double': np.dtype(np.float64)}

DTYPES_LOOKUP_convert = {np.dtype(np.uint8): 'byte',
                        np.dtype(np.int16): 'int16',
                        np.dtype(np.uint16): 'uint16',
                        np.dtype(np.int32): 'int32',
                        np.dtype(np.uint32): 'uint32',
                        np.dtype(np.int64): 'int64',
                        np.dtype(np.float32): 'float',
                        np.dtype(np.float64): 'double'}

class _XMLHandler(object):

    def __init__(self, version):
        self._version = version

        self._parsers = {NumericalAttribute: self._parse_numerical_attribute,
                         TextAttribute: self._parse_text_attribute,
                         ObjectAttribute: self._parse_object_attribute,
                         DateAttribute: self._parse_date_attribute,
                         TimeAttribute: self._parse_time_attribute,
                         ChecksumAttribute: self._parse_checksum_attribute,
                         }
        self._converters = {NumericalAttribute: self._convert_numerical_attribute,
                            TextAttribute: self._convert_text_attribute,
                            ObjectAttribute: self._convert_object_attribute,
                            DateAttribute: self._convert_date_attribute,
                            TimeAttribute: self._convert_time_attribute,
                            ChecksumAttribute: self._convert_checksum_attribute,
                            }

    def _find_method(self, lookup, attrib):
        attrib_class = attrib.__class__
        method = lookup.get(attrib_class, None)
        if method is not None:
            return method

        for base_class in attrib_class.__bases__:
            method = lookup.get(base_class, None)
            if method is not None:
                return method

        raise ValueError('No class was found for %s' % attrib_class.__name__)

    def can_parse(self, element):
        return False

    def _parse_parameter(self, element, klass):
        obj = klass.__new__(klass)

        for name, attrib in klass.__attributes__.items():
            if attrib.xmlname is None: # skip, undefined way to load
                continue

            subelement = element.find(attrib.xmlname)
            if subelement is None:
                if attrib.is_required():
                    raise ValueError('Element %s is missing' % attrib.xmlname)
                else:
                    value = None
            else:
                method = self._find_method(self._parsers, attrib)
                value = method(subelement, attrib)
            setattr(obj, name, value)

        return obj

    def _parse_numerical_attribute(self, element, attrib=None):
        datatype = element.attrib['DataType']
        if datatype.startswith('array:'):
            dtype = DTYPES_LOOKUP_parse[datatype[6:]]
            value = np.array(list(map(float, element.text.split(','))), dtype=dtype)
            assert len(value) == int(element.attrib['Count'])
        else:
            dtype = DTYPES_LOOKUP_parse[datatype]
            value = dtype.type(float(element.text))

        unit = element.get('Unit')

        return convert_value(value, unit)

    def _parse_text_attribute(self, element, attrib=None):
        attribs = list(filter(lambda s: s.startswith('alt-lang-'), element.keys()))
        if any(attribs):
            alternatives = {}
            for attrib in attribs:
                language_tag = attrib[9:]
                altvalue = element.get(attrib)
                alternatives[language_tag] = altvalue
            return langstr(element.text, alternatives)
        else:
            return element.text

    def _parse_object_attribute(self, element, attrib=None):
        return self._parse_parameter(element, attrib.type_)

    def _parse_date_attribute(self, element, attrib=None):
        dt = datetime.datetime.strptime(element.text, '%Y-%m-%d')
        return datetime.date(dt.year, dt.month, dt.day)

    def _parse_time_attribute(self, element, attrib=None):
        dt = datetime.datetime.strptime(element.text, '%H:%M:%S')
        return datetime.time(dt.hour, dt.minute, dt.second)

    def _parse_checksum_attribute(self, element, attrib=None):
        value = element.text
        algorithm = element.attrib['Algorithm']
        return Checksum(value, algorithm)

    def parse(self, element):
        raise NotImplementedError # pragma: no cover

    def can_convert(self, obj):
        return False

    def _convert_parameter(self, obj, tag=None, attrib=None):
        if attrib is None:
            attrib = {}
        element = etree.Element(tag or 'Unknown', attrib)

        for name, attrib in obj.__class__.__attributes__.items():
            if attrib.xmlname is None: # skip, undefined way to convert
                continue

            value = getattr(obj, name, None)
            if value is None:
                if attrib.is_required():
                    raise ValueError('Value for %s is required' % name)
                else:
                    continue

            method = self._find_method(self._converters, attrib)
            subelements = method(value, attrib)
            element.extend(subelements)

        return element

    def _convert_numerical_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)

        if hasattr(value, 'unit') and value.unit is not None:
            element.attrib['Unit'] = value.unit

        datatype = DTYPES_LOOKUP_convert[value.dtype]

        value = value.tolist()
        if np.isscalar(value):
            element.text = str(value)
        else:
            element.text = ','.join(map(str, value))
            element.attrib['Count'] = str(len(value))
            datatype = 'array:' + datatype

        element.attrib['DataType'] = datatype

        return [element]

    def _convert_text_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)
        element.text = str(value)

        if isinstance(value, langstr):
            for language_tag, altvalue in value.alternatives.items():
                element.set('alt-lang-' + language_tag, altvalue)

        return [element]

    def _convert_object_attribute(self, value, attrib):
        return [self._convert_parameter(value, attrib.xmlname)]

    def _convert_date_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)
        element.text = value.strftime('%Y-%m-%d')
        return [element]

    def _convert_time_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)
        element.text = value.strftime('%H:%M:%S')
        return [element]

    def _convert_checksum_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)
        element.text = value.value
        element.set('Algorithm', value.algorithm)
        return [element]

    def convert(self, obj):
        raise NotImplementedError # pragma: no cover

    @property
    def version(self):
        return self._version
