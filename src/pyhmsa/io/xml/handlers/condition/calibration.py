#!/usr/bin/env python
"""
================================================================================
:mod:`calibration` -- XML handler for calibrations
================================================================================

.. module:: calibration
   :synopsis: XML handler for calibrations

.. inheritance-diagram:: calibration

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
from pyhmsa.core.condition.calibration import \
    (_Calibration, CalibrationConstant, CalibrationLinear,
     CalibrationPolynomial, CalibrationExplicit)
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class _CalibrationXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Calibration'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Quantity')
        kwargs['quantity'] = subelement.text

        subelement = element.find('Unit')
        kwargs['unit'] = subelement.text

        return _Calibration(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, _Calibration)

    def to_xml(self, obj):
        element = etree.Element('Calibration')

        subelement = etree.Element('Quantity')
        subelement.text = obj.quantity
        element.append(subelement)

        subelement = etree.Element('Unit')
        subelement.text = obj.unit
        element.append(subelement)

        return element

class CalibrationConstantXMLHandler(_CalibrationXMLHandler):

    def can_parse(self, element):
        if not _CalibrationXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Constant'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Value')
        kwargs['value'] = self._handler_numerical.from_xml(subelement)

        parent = _CalibrationXMLHandler.from_xml(self, element)
        return CalibrationConstant(parent.quantity, parent.unit, **kwargs)

    def can_convert(self, obj):
        if not _CalibrationXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, CalibrationConstant)

    def to_xml(self, obj):
        element = _CalibrationXMLHandler.to_xml(self, obj)
        element.set('Class', 'Constant')

        subelement = self._handler_numerical.to_xml(obj.value)
        subelement.tag = 'Value'
        element.append(subelement)

        return element

class CalibrationLinearXMLHandler(_CalibrationXMLHandler):

    def can_parse(self, element):
        if not _CalibrationXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Linear'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Gain')
        kwargs['gain'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Offset')
        kwargs['offset'] = self._handler_numerical.from_xml(subelement)

        parent = _CalibrationXMLHandler.from_xml(self, element)
        return CalibrationLinear(parent.quantity, parent.unit, **kwargs)

    def can_convert(self, obj):
        if not _CalibrationXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, CalibrationLinear)

    def to_xml(self, obj):
        element = _CalibrationXMLHandler.to_xml(self, obj)
        element.set('Class', 'Linear')

        subelement = self._handler_numerical.to_xml(obj.gain)
        subelement.tag = 'Gain'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.offset)
        subelement.tag = 'Offset'
        element.append(subelement)

        return element

class CalibrationPolynomialXMLHandler(_CalibrationXMLHandler):

    def can_parse(self, element):
        if not _CalibrationXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Polynomial'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Coefficients')
        kwargs['coefficients'] = self._handler_numerical.from_xml(subelement)

        parent = _CalibrationXMLHandler.from_xml(self, element)
        return CalibrationPolynomial(parent.quantity, parent.unit, **kwargs)

    def can_convert(self, obj):
        if not _CalibrationXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, CalibrationPolynomial)

    def to_xml(self, obj):
        element = _CalibrationXMLHandler.to_xml(self, obj)
        element.set('Class', 'Polynomial')

        subelement = self._handler_numerical.to_xml(obj.coefficients)
        subelement.tag = 'Coefficients'
        element.append(subelement)

        return element

class CalibrationExplicitXMLHandler(_CalibrationXMLHandler):

    def can_parse(self, element):
        if not _CalibrationXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Explicit'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Values')
        kwargs['values'] = self._handler_numerical.from_xml(subelement)

        parent = _CalibrationXMLHandler.from_xml(self, element)
        return CalibrationExplicit(parent.quantity, parent.unit, **kwargs)

    def can_convert(self, obj):
        if not _CalibrationXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, CalibrationExplicit)

    def to_xml(self, obj):
        element = _CalibrationXMLHandler.to_xml(self, obj)
        element.set('Class', 'Explicit')

        subelement = self._handler_numerical.to_xml(obj.values)
        subelement.tag = 'Values'
        element.append(subelement)

        return element
