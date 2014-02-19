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
        return isinstance(obj, Instrument)

    def convert(self, obj):
        return self._convert_parameter(obj, 'Instrument')