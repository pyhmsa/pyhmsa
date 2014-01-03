#!/usr/bin/env python
"""
================================================================================
:mod:`imageraster` -- Image raster (2D and 3D collection)
================================================================================

.. module:: imageraster
   :synopsis: Image raster (2D and 3D collection)

.. inheritance-diagram:: pyhmsa.datum.imageraster

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
from pyhmsa.spec.datum import _Datum
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D

# Globals and constants variables.

class _ImageRaster(_Datum):
    """
    Represents a dataset that has been rastered over regularly spaced intervals
    in one or more dimensions, such as a 1D linescan, a 2D image or a 3D
    serial section.
    """

class ImageRaster2D(_ImageRaster):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions).
    """

    def __new__(cls, x, y, dtype=np.float32, buffer=None, conditions=None):
        shape = (x, y)
        return _ImageRaster.__new__(cls, shape, dtype, buffer, conditions)

    @property
    def x(self):
        return np.uint32(self.shape[0])

    @property
    def y(self):
        return np.uint32(self.shape[1])

    def toanalysis(self, x, y):
        return Analysis0D(self[x, y], self.dtype, self.conditions)

class ImageRaster2DSpectral(_ImageRaster):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 1D array
    (channel dimension).
    An example of this type of dataset is a SEM-XEDS map.
    """

    def __new__(cls, x, y, channels, dtype=np.float32,
                buffer=None, conditions=None):
        shape = (x, y, channels)
        return _ImageRaster.__new__(cls, shape, dtype, buffer, conditions)

    @property
    def x(self):
        return np.uint32(self.shape[0])

    @property
    def y(self):
        return np.uint32(self.shape[1])

    @property
    def channels(self):
        return np.uint32(self.shape[2])

    def toanalysis(self, x, y):
        return Analysis1D(self.channels, self.dtype, self[x, y], self.conditions)

class ImageRaster2DHyperimage(_ImageRaster):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 2D image
    (U/V dimensions.
    """

    def __new__(cls, x, y, u, v, dtype=np.float32,
                buffer=None, conditions=None):
        shape = (x, y, u, v)
        return _ImageRaster.__new__(cls, shape, dtype, buffer, conditions)

    @property
    def x(self):
        return np.uint32(self.shape[0])

    @property
    def y(self):
        return np.uint32(self.shape[1])

    @property
    def u(self):
        return np.uint32(self.shape[2])

    @property
    def v(self):
        return np.uint32(self.shape[3])

    def toanalysis(self, x, y):
        return Analysis2D(self.u, self.v, self.dtype, self[x, y], self.conditions)
