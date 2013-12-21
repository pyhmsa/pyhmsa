#!/usr/bin/env python
"""
================================================================================
:mod:`numerical` -- Numerical data type
================================================================================

.. module:: numerical
   :synopsis: Numerical data type

.. inheritance-diagram:: pyhmsa.type.numerical

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from collections import namedtuple, Iterable
from numbers import Integral, Real

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.unit import validate_unit

# Globals and constants variables.

_SUPPORTED_DTYPES = frozenset([np.dtype(np.uint8), np.dtype(np.int16),
                               np.dtype(np.uint16), np.dtype(np.int32),
                               np.dtype(np.uint32), np.dtype(np.int64),
                               np.dtype(np.float32), np.dtype(np.float64)])

def _convert_python_to_numpy(value):
    if value is not None:
        if isinstance(value, Iterable):
            value = np.array(value)
        elif isinstance(value, (Integral, Real)):
            value = np.array([value])[0]

        if value.dtype not in _SUPPORTED_DTYPES:
            raise ValueError('Unsupported data type: %s' % value.dtype.name)

    return value

def extract_value(val, unit=None):
    if unit is None:
        return _convert_python_to_numpy(val)
    else:
        if isinstance(val, tuple):
            if len(val) == 2:
                unit = val[1] or unit
                val = val[0]
            else:
                raise ValueError("Too many arguments")

        return NumericalValue(val, unit)

class NumericalValue(namedtuple('Unit', ['value', 'unit'])):
    
    def __new__(cls, value, unit):
        value = _convert_python_to_numpy(value)
        validate_unit(unit)
        return cls.__bases__[0].__new__(cls, value, unit)

    def __nonzero__(self): # Python 2.x # pragma: no cover
        return self.value is not None

    def __bool__(self): # Python 3.x # pragma: no cover
        return self.value is not None
