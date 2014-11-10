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
from pyhmsa.spec.condition.acquisition import AcquisitionRasterXY
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.type.numerical import convert_unit

# Globals and constants variables.
from pyhmsa.spec.condition.acquisition import \
    POSITION_LOCATION_CENTER, POSITION_LOCATION_START

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

    def get_position(self, x, y):
        if x < 0:
            x = self.x + x
        if y < 0:
            y = self.y + y

        if x < 0 or x >= self.x:
            raise IndexError('Index %i is out of bounds' % x)
        if y < 0 or y >= self.y:
            raise IndexError('Index %i is out of bounds' % y)

        acqs = self.conditions.findvalues(AcquisitionRasterXY)
        if not acqs:
            raise ValueError('No acquisition raster XY found in conditions')
        acq = next(iter(acqs))

        position_start = acq.positions.get(POSITION_LOCATION_START)
        if position_start is None:
            raise ValueError('Missing start position in acquisition condition')

        position_center = acq.positions.get(POSITION_LOCATION_CENTER)
        if position_center is None:
            raise ValueError('Missing center position in acquisition condition')

        if convert_unit('m', position_start.z) != convert_unit('m', position_center.z):
            raise ValueError('Positions must have the same z: %s != %s' % \
                             (position_start.z, position_center.z))
        if convert_unit('degrees', position_start.r) != convert_unit('degrees', position_center.r):
            raise ValueError('Positions must have the same rotation: %s != %s' % \
                             (position_start.r, position_center.r))
        if convert_unit('degrees', position_start.t) != convert_unit('degrees', position_center.t):
            raise ValueError('Positions must have the same tilt: %s != %s' % \
                             (position_start.t, position_center.t))

        delta = position_center - position_start
        delta_x = convert_unit('mm', delta.x) / (acq.step_count_x / 2)
        delta_y = convert_unit('mm', delta.y) / (acq.step_count_y / 2)

        return SpecimenPosition(x=convert_unit('mm', position_start.x) + delta_x * x,
                                y=convert_unit('mm', position_start.y) + delta_y * y,
                                z=position_start.z,
                                r=position_start.r,
                                t=position_start.t)

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
