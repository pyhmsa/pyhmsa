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

try:
    from PIL import Image
except ImportError:
    Image = None

# Local modules.
from pyhmsa.spec.datum import _Datum

# Globals and constants variables.

class _Analysis(_Datum):
    """
    Stores a single measurement of a specimen at a single point in space or
    time.
    """
    pass

class Analysis0D(_Analysis):
    """
    Data with 0 collection dimensions and 0 datum dimensions implies a dataset
    comprising of one single-valued measurement.
    """

    def __new__(cls, value, dtype=np.float32, conditions=None):
        buffer = np.array(value, dtype=dtype)
        return _Analysis.__new__(cls, (), dtype, buffer, conditions)

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 0:
            raise ValueError('Invalid dimension of array. Only 0D array accepted.')

class Analysis1D(_Analysis):
    """
    Stores a measurement of a specimen at a single point in space or time
    with one datum dimension.
    """

    def __new__(cls, channels, dtype=np.float32, buffer=None, conditions=None):
        if channels <= 0:
            raise ValueError('Number of channel must be greater than 0')
        shape = (channels,)
        return _Analysis.__new__(cls, shape, dtype, buffer, conditions)

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 1:
            raise ValueError('Invalid dimension of array. Only 1D array accepted.')

    @property
    def channels(self):
        return np.uint32(len(self))

class Analysis2D(_Analysis):
    """
    Store a single measurement of the specimen at a single point in space or
    time with two datum dimensions, such as a diffraction pattern.

    .. note::

       This dataset type shall not be used to store 2 dimensional images
       rastered over the specimen, such as a conventional TEM or SEM image.
       Instead, such data shall be stored using the :class:`ImageRaster2D`.
    """

    def __new__(cls, u, v, dtype=np.float32, buffer=None, conditions=None):
        if u <= 0 or v <= 0:
            raise ValueError('Dimension must be greater than 0')
        shape = (u, v)
        return _Analysis.__new__(cls, shape, dtype, buffer, conditions)

    @classmethod
    def fromimage(cls, im):
        width, height = im.size
        mode = im.mode

        if mode in ['1', 'L', 'P']:
            dtype = np.uint8
        elif mode == 'I':
            dtype = np.int32
        elif mode == 'F':
            dtype = np.float32
        else:
            raise ValueError('Unsupported mode: %s' % mode)

        buffer = np.array(im, dtype=dtype)
        return cls(width, height, dtype, buffer)

    def __array_finalize__(self, obj):
        _Analysis.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 2:
            raise ValueError('Invalid dimension of array. Only 2D array accepted.')

    @property
    def u(self):
        return np.uint32(self.shape[0])

    @property
    def v(self):
        return np.uint32(self.shape[1])

    def toimage(self):
        if Image is None:
            raise RuntimeError('PIL is not installed')
        return Image.fromarray(self)
