#!/usr/bin/env python
"""
================================================================================
:mod:`specimenposition` -- Specimen position XML handler
================================================================================

.. module:: specimenposition
   :synopsis: Specimen position XML handler

.. inheritance-diagram:: pyhmsa.fileformat.xmlhandler.condition.specimenposition

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class SpecimenPositionXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'SpecimenPosition'

    def parse(self, element):
        return self._parse_parameter(element, SpecimenPosition)

    def can_convert(self, obj):
        return type(obj) is SpecimenPosition

    def convert(self, obj):
        return self._convert_parameter(obj, 'SpecimenPosition')