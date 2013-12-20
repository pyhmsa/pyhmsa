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
try:
    from collections import UserDict
except ImportError: # Python 2.7 # pragma: no cover
    from UserDict import UserDict
from collections import Iterable

# Third party modules.

# Local modules.
from pyhmsa.type.numerical import NumericalValue
from pyhmsa.type.identifier import validate_identifier

# Globals and constants variables.

def extract_numerical_value(val, unit):
    if isinstance(val, tuple):
        if len(val) == 2:
            unit = val[1] or unit
            val = val[0]
        else:
            raise ValueError("Too many arguments")

    return NumericalValue(val, unit)

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

class _Condition(object):
    pass

class Conditions(UserDict):

    def __setitem__(self, key, item):
        validate_identifier(key)
        UserDict.__setitem__(self, key, item)
