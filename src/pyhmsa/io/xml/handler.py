#!/usr/bin/env python
"""
================================================================================
:mod:`handler` -- Handler to convert core objects to XML
================================================================================

.. module:: handler
   :synopsis: Handler to convert core objects to XML

.. inheritance-diagram:: handler

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

# Globals and constants variables.

class _XMLHandler(object):

    def can_parse(self, element):
        return False

    def from_xml(self, element):
        raise NotImplementedError

    def can_convert(self, obj):
        return False

    def to_xml(self, obj):
        raise NotImplementedError


