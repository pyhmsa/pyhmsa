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

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.condition import Conditions
from pyhmsa.type.numerical import validate_dtype
from pyhmsa.type.identifier import _IdentifierDict

# Globals and constants variables.

class _Datum(np.ndarray):

    def __new__(cls, shape, dtype=np.float32, buffer=None, conditions=None):
        validate_dtype(dtype)
        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset=0,
                                 strides=None, order=None)

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

class Data(_IdentifierDict):

    def __setitem__(self, identifier, condition):
        _IdentifierDict.__setitem__(self, identifier, condition)
        if not isinstance(condition, _Datum):
            raise ValueError("Value is not a datum")
