#!/usr/bin/env python
"""
================================================================================
:mod:`data` -- Dictionary of datum objects
================================================================================

.. module:: data
   :synopsis: Dictionary of datum objects

.. inheritance-diagram:: pyhmsa.spec.datum.data

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.datum.datum import _Datum
from pyhmsa.type.identifier import _IdentifierDict

# Globals and constants variables.

class Data(_IdentifierDict):

    def __setitem__(self, name, datum):
        if not isinstance(datum, _Datum):
            raise ValueError("Value is not a datum")
        _IdentifierDict.__setitem__(self, name, datum)
