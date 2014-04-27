#!/usr/bin/env python
"""
================================================================================
:mod:`instrument` -- XML handler for instrument condition
================================================================================

.. module:: instrument
   :synopsis: XML handler for instrument condition

.. inheritance-diagram:: instrument

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.instrument import Instrument
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class InstrumentXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Instrument'

    def parse(self, element):
        return self._parse_parameter(element, Instrument)

    def can_convert(self, obj):
        return type(obj) is Instrument

    def convert(self, obj):
        return self._convert_parameter(obj, 'Instrument')
