#!/usr/bin/env python
"""
================================================================================
:mod:`analysis` -- Analysis (0D collection)
================================================================================

.. module:: analysis
   :synopsis: Analysis

.. inheritance-diagram:: analysis

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
from pyhmsa.core.datum import _Datum

# Globals and constants variables.

class _Analysis(_Datum):
    """
    Stores a single measurement of a specimen at a single point in space or
    time.
    """
    pass

class Analysis0D(_Analysis):
    """

    """

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if not np.isscalar(obj):
            raise ValueError("Invalid dimension. Only scalar value accepted.")

class Analysis1D(_Analysis):
    """
    Stores a measurement of a specimen at a single point in space or time
    with one datum dimension.
    """

    def __new__(cls, channels, dtype=np.float32, buffer=None, conditions=None):
        shape = (channels,)
        return _Analysis.__new__(cls, shape, dtype, buffer, conditions)

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 1:
            raise ValueError('Invalid dimension of array. Only 1D array accepted.')

    @property
    def channel(self):
        return len(self)

class Analysis2D(_Analysis):
    """
    Store a single measurement of the specimen at a single point in space or
    time with two datum dimensions, such as a diffraction pattern.

    .. note::

       This dataset type shall not be used to store 2 dimensional images
       rastered over the specimen, such as a conventional TEM or SEM image.
       Instead, such data shall be stored using the :class:`ImageRaster2D`.
    """

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 2:
            raise ValueError('Invalid dimension of array. Only 2D array accepted.')

    @property
    def u(self):
        return self.shape[0]

    @property
    def v(self):
        return self.shape[1]

    def toimage(self):
        raise NotImplementedError
