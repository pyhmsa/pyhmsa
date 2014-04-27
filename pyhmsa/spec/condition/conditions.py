#!/usr/bin/env python
"""
================================================================================
:mod:`conditions` -- Dictionary of conditions
================================================================================

.. module:: conditions
   :synopsis: Dictionary

.. inheritance-diagram:: pyhmsa.spec.condition.conditions

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
from pyhmsa.type.identifier import _IdentifierDict
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class Conditions(_IdentifierDict):

    def __setitem__(self, identifier, condition):
        if not isinstance(condition, _Condition):
            raise ValueError("Value is not a condition")
        _IdentifierDict.__setitem__(self, identifier, condition)
