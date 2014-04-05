#!/usr/bin/env python
"""
================================================================================
:mod:`imageraster` -- Image raster (2D and 3D collection)
================================================================================

.. module:: imageraster
   :synopsis: Image raster (2D and 3D collection)

.. inheritance-diagram:: pyhmsa.datum.imageraster

"""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.datum import _Datum
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D

# Globals and constants variables.

class _ImageRaster(_Datum):
    """
    Represents a dataset that has been rastered over regularly spaced intervals
    in one or more dimensions, such as a 1D linescan, a 2D image or a 3D
    serial section.
    """

    TEMPLATE = "ImageRaster"

class _ImageRaster2D(_ImageRaster):
    """
    Abstract class for image raster 2D classes.
    """

    @property
    def x(self):
        return np.uint32(self.shape[0])

    @property
    def y(self):
        return np.uint32(self.shape[1])

    @property
    def collection_dimensions(self):
        dims = _ImageRaster.collection_dimensions.fget(self) # @UndefinedVariable
        dims['X'] = self.x
        dims['Y'] = self.y
        return dims

class ImageRaster2D(_ImageRaster2D):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions).
    """

    CLASS = "2D"

    def __new__(cls, x, y, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (x, y)
        return _ImageRaster2D.__new__(cls, shape, dtype,
                                      buffer, offset, strides, order, conditions)

    def toanalysis(self, x, y):
        return Analysis0D(self[x, y], self.dtype, conditions=self.conditions)

class ImageRaster2DSpectral(_ImageRaster2D):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 1D array
    (channel dimension).
    An example of this type of dataset is a SEM-XEDS map.
    """

    CLASS = "2D/Spectral"

    def __new__(cls, x, y, channels, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (x, y, channels)
        return _ImageRaster2D.__new__(cls, shape, dtype,
                                      buffer, offset, strides, order, conditions)

    @property
    def channels(self):
        return np.uint32(self.shape[2])

    @property
    def datum_dimensions(self):
        dims = _ImageRaster2D.datum_dimensions.fget(self) # @UndefinedVariable
        dims['Channel'] = self.channels
        return dims

    def toanalysis(self, x, y):
        return Analysis1D(self.channels, self.dtype, self[x, y],
                          conditions=self.conditions)

class ImageRaster2DHyperimage(_ImageRaster2D):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 2D image
    (U/V dimensions.
    """

    CLASS = "2D/Hyperimage"

    def __new__(cls, x, y, u, v, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (x, y, u, v)
        return _ImageRaster2D.__new__(cls, shape, dtype,
                                      buffer, offset, strides, order, conditions)

    @property
    def u(self):
        return np.uint32(self.shape[2])

    @property
    def v(self):
        return np.uint32(self.shape[3])

    @property
    def datum_dimensions(self):
        dims = _ImageRaster2D.datum_dimensions.fget(self) # @UndefinedVariable
        dims['U'] = self.u
        dims['V'] = self.v
        return dims

    def toanalysis(self, x, y):
        return Analysis2D(self.u, self.v, self.dtype, self[x, y],
                          conditions=self.conditions)
