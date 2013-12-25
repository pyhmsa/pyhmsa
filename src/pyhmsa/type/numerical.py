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

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.unit import validate_unit

# Globals and constants variables.

_SUPPORTED_DTYPES = frozenset(map(np.dtype, [np.uint8, np.int16, np.uint16,
                                             np.int32, np.uint32, np.int64,
                                             np.float32, np.float64]))

def validate_dtype(arg):
    if hasattr(arg, 'dtype'):
        dtype = arg.dtype
    else:
        raise ValueError('Cannot find dtype of argument')

    if dtype not in _SUPPORTED_DTYPES:
        raise ValueError('Unsupported data type: %s' % dtype.name)

    return True

class arrayunit(np.ndarray):
    
    def __new__(cls, shape, dtype=float, buffer=None, offset=0,
                 strides=None, order=None, unit=None):
        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset, strides,
                                 order)
        obj._unit = unit
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._unit = getattr(obj, '_unit', None)
    
    def __array_wrap__(self, out_arr, context=None):
        ret_arr = np.ndarray.__array_wrap__(self, out_arr, context)
        return np.array(ret_arr) # Cast as regular array
    
    def __str__(self):
        if self._unit is not None:
            return np.ndarray.__str__(self) + ' ' + self.unit
        else:
            return np.ndarray.__str__(self)

    @property
    def unit(self):
        return self._unit

def convert_value(value, unit=None):
    if value is None:
        return None

    if not isinstance(value, arrayunit):
        value = np.asarray(value)
    else:
        unit = value.unit or unit

    validate_dtype(value)
    if unit is not None:
        validate_unit(unit)

    return arrayunit(value.shape, value.dtype, value, unit=unit)
