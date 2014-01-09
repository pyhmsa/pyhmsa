#!/usr/bin/env python
"""
================================================================================
:mod:`datum` -- Datum
================================================================================

.. module:: datum
   :synopsis: Datum

.. inheritance-diagram:: pyhmsa.datum

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from collections import OrderedDict

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.condition import Conditions
from pyhmsa.type.numerical import validate_dtype
from pyhmsa.type.identifier import _IdentifierDict

# Globals and constants variables.

class _Datum(np.ndarray):

    def __new__(cls, shape, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        validate_dtype(dtype)

        if buffer is None:
            buffer = np.zeros(shape, dtype)

        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset=offset,
                                 strides=strides, order=order)

        if conditions is None:
            conditions = Conditions()
        obj._conditions = conditions

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._conditions = getattr(obj, 'conditions', Conditions())

    @property
    def conditions(self):
        return self._conditions

    @property
    def datum_dimensions(self):
        return OrderedDict()

    @property
    def collection_dimensions(self):
        return OrderedDict()

class Data(_IdentifierDict):

    def __setitem__(self, name, datum):
        if not isinstance(datum, _Datum):
            raise ValueError("Value is not a datum")
        _IdentifierDict.__setitem__(self, name, datum)
