#!/usr/bin/env python
"""
================================================================================
:mod:`xmlhandler` -- Handler to convert core objects to XML
================================================================================

.. module:: xmlhandler
   :synopsis: Handler to convert core objects to XML

.. inheritance-diagram:: xmlhandler

"""

# Standard library modules.
import xml.etree.ElementTree as etree
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.numerical import convert_value
from pyhmsa.type.language import langstr
from pyhmsa.type.checksum import Checksum
from pyhmsa.type.xrayline import xrayline
from pyhmsa.util.parameter import \
    (NumericalAttribute, TextAttribute, ObjectAttribute, DateAttribute,
     TimeAttribute, ChecksumAttribute, XRayLineAttribute)

# Globals and constants variables.
from pyhmsa.type.xrayline import NOTATION_SIEGBAHN

DTYPES_LOOKUP_PARSE = {'byte': np.dtype(np.uint8),
                       'int16': np.dtype(np.int16),
                       'uint16': np.dtype(np.uint16),
                       'int32': np.dtype(np.int32),
                       'uint32': np.dtype(np.uint32),
                       'int64': np.dtype(np.int64),
                       'float': np.dtype(np.float32),
                       'double': np.dtype(np.float64)}

DTYPES_LOOKUP_CONVERT = {np.dtype(np.uint8): 'byte',
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
                         XRayLineAttribute: self._parse_xrayline_attribute,
                         }
        self._converters = {NumericalAttribute: self._convert_numerical_attribute,
                            TextAttribute: self._convert_text_attribute,
                            ObjectAttribute: self._convert_object_attribute,
                            DateAttribute: self._convert_date_attribute,
                            TimeAttribute: self._convert_time_attribute,
                            ChecksumAttribute: self._convert_checksum_attribute,
                            XRayLineAttribute: self._convert_xrayline_attribute,
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
        # Create object
        obj = klass.__new__(klass)

#        if hasattr(obj, '__reduce__'):
#            reduce = obj.__reduce__()
#
#            func = reduce[0]
#            args = reduce[1]
#            obj = func(*args)
#
#            # State
#            if len(reduce) > 2:
#                state = reduce[2]
#                if hasattr(obj, '__setstate__'):
#                    obj.__setstate__(state)
#                else:
#                    obj.__dict__.update(state)
#
#            # List items
#            if len(reduce) > 3:
#                obj.extend(reduce[3])
#
#            # Dict items
#            if len(reduce) > 4:
#                obj.update(reduce[4])

        # Load attributes
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
            dtype = DTYPES_LOOKUP_PARSE[datatype[6:]]
            value = np.array(list(map(float, element.text.split(','))), dtype=dtype)
            assert len(value) == int(element.attrib['Count'])
        else:
            dtype = DTYPES_LOOKUP_PARSE[datatype]
            value = dtype.type(float(element.text))

        unit = element.get('Unit')

        return convert_value(value, unit)

    def _parse_text_attribute(self, element, attrib=None):
        attribs = list(filter(lambda s: s.startswith('alt-lang-'), element.keys()))
        if any(attribs):
            alternatives = {}
            for subattrib in attribs:
                language_tag = subattrib[9:]
                altvalue = element.get(subattrib)
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

    def _parse_xrayline_attribute(self, element, attrib=None):
        value = element.text
        notation = element.get('Notation', NOTATION_SIEGBAHN)

        attribs = list(filter(lambda s: s.startswith('alt-'), element.keys()))
        if any(attribs):
            attrib = attribs[0]
            altvalue = element.get(attrib)
        else:
            altvalue = None

        return xrayline(value, notation, altvalue)

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
        if tag is None:
            tag = 'Unknown'
        element = etree.Element(tag, attrib)

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

        datatype = DTYPES_LOOKUP_CONVERT[value.dtype]

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
        element.text = value

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

    def _convert_xrayline_attribute(self, value, attrib):
        element = etree.Element(attrib.xmlname)
        element.set('Notation', value.notation)
        if value.alternative is not None:
            element.set('alt-%s' % value.alternative.notation,
                        str(value.alternative))
        element.text = str(value)
        return [element]

    def _convert_checksum_attribute(self, value, attrib):
        return [] # Checksum is added manually later by the writer

    def convert(self, obj):
        raise NotImplementedError # pragma: no cover

    @property
    def version(self):
        return self._version
