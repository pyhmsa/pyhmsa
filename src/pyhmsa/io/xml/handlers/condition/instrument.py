#!/usr/bin/env python
"""
================================================================================
:mod:`instrument` -- XML handler for instrument condition
================================================================================

.. module:: instrument
   :synopsis: XML handler for instrument condition

.. inheritance-diagram:: instrument

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
from pyhmsa.core.condition.instrument import Instrument
from pyhmsa.io.xml.handler import _XMLHandler

# Globals and constants variables.

class InstrumentXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Instrument'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Manufacturer')
        kwargs['manufacturer'] = subelement.text

        subelement = element.find('Model')
        kwargs['model'] = subelement.text

        subelement = element.find('SerialNumber')
        if subelement is not None:
            kwargs['serial_number'] = subelement.text

        return Instrument(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, Instrument)

    def to_xml(self, obj):
        element = etree.Element('Instrument')

        subelement = etree.Element('Manufacturer')
        subelement.text = obj.manufacturer
        element.append(subelement)

        subelement = etree.Element('Model')
        subelement.text = obj.model
        element.append(subelement)

        if obj.serial_number:
            subelement = etree.Element('SerialNumber')
            subelement.text = obj.serial_number
            element.append(subelement)

        return element
