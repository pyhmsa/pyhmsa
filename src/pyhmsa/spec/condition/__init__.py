#!/usr/bin/env python
"""
================================================================================
:mod:`condition` -- Conditions
================================================================================

.. module:: condition
   :synopsis: Conditions

.. inheritance-diagram:: pyhmsa.condition

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
from pyhmsa.util.parameter import Parameter
from pyhmsa.type.identifier import _IdentifierDict

# Globals and constants variables.

class _Condition(Parameter):

    TEMPLATE = None
    CLASS = None

class Conditions(_IdentifierDict):

    def __setitem__(self, identifier, condition):
        _IdentifierDict.__setitem__(self, identifier, condition)
        if not isinstance(condition, _Condition):
            raise ValueError("Value is not a condition")
