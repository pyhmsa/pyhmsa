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

# Local modules.
from pyhmsa.core.datum import _Datum

# Globals and constants variables.

class _ImageRaster(_Datum):
    """
    Represents a dataset that has been rastered over regularly spaced intervals 
    in one or more dimensions, such as a 1D linescan, a 2D image or a 3D
    serial section.
    """

    def __array_finalize__(self, obj):
        _Datum.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim < 2:
            raise ValueError('Invalid dimension of array')

class ImageRaster2D(_ImageRaster):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions).
    """

    def __array_finalize__(self, obj):
        _ImageRaster.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim < 2:
            raise ValueError('Invalid dimension of array')

    @property
    def x(self):
        return self.shape[0]

    @property
    def y(self):
        return self.shape[1]
    
class ImageRaster2DSpectral(ImageRaster2D):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 1D array
    (channel dimension). 
    An example of this type of dataset is a SEM-XEDS map.
    """
    
    def __array_finalize__(self, obj):
        ImageRaster2D.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 3:
            raise ValueError('Invalid dimension of array')

    @property
    def channel(self):
        return self.shape[2]

class ImageRaster2DHyperimage(ImageRaster2D):
    """
    Represents a dataset that has been raster mapped in 2D (x/y dimensions),
    where for each raster coordinate, the datum collected was a 2D image
    (U/V dimensions.
    """

    def __array_finalize__(self, obj):
        _ImageRaster.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 4:
            raise ValueError('Invalid dimension of array')

    @property
    def u(self):
        return self.shape[2]

    @property
    def v(self):
        return self.shape[3]

