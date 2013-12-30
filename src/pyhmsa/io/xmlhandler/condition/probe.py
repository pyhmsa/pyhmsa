#!/usr/bin/env python
"""
================================================================================
:mod:`probe` -- XML handler for probe condition
================================================================================

.. module:: probe
   :synopsis: XML handler for probe condition

.. inheritance-diagram:: probe

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
from pyhmsa.spec.condition.probe import ProbeEM, ProbeTEM
from pyhmsa.io.xmlhandler import _XMLHandler

# Globals and constants variables.

class ProbeEMXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Probe' and element.get('Class') == 'EM'

    def from_xml(self, element):
        return self._parse_parameter(element, ProbeEM)

    def can_convert(self, obj):
        return isinstance(obj, ProbeEM)

    def to_xml(self, obj):
        element = etree.Element('Probe', {'Class': 'EM'})
        return self._convert_parameter(obj, element)

class ProbeTEMXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Probe' and element.get('Class') == 'TEM'

    def from_xml(self, element):
        return self._parse_parameter(element, ProbeTEM)

    def can_convert(self, obj):
        return isinstance(obj, ProbeTEM)

    def to_xml(self, obj):
        element = etree.Element('Probe', {'Class': 'TEM'})
        return self._convert_parameter(obj, element)
