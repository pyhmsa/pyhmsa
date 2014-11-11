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
    POSITION_LOCATION_CENTER, POSITION_LOCATION_START, POSITION_LOCATION_END

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
        position_center = acq.positions.get(POSITION_LOCATION_CENTER)
        position_end = acq.positions.get(POSITION_LOCATION_END)

        if position_start and position_end:
            pass
        elif position_start and position_center:
            delta = position_center - position_start
            position_end = position_center + delta
        elif position_center and position_end:
            delta = position_end - position_center
            position_start = position_center - delta
        else:
            raise ValueError('At least two positions must be defined in acquisition condition')

        if convert_unit('degrees', position_start.r) != convert_unit('degrees', position_end.r):
            raise ValueError('Positions must have the same rotation: %s != %s' % \
                             (position_start.r, position_end.r))
        if convert_unit('degrees', position_start.t) != convert_unit('degrees', position_end.t):
            raise ValueError('Positions must have the same tilt: %s != %s' % \
                             (position_start.t, position_end.t))

        delta = position_end - position_start
        delta_x = convert_unit('mm', delta.x) / (acq.step_count_x - 1)
        delta_y = convert_unit('mm', delta.y) / (acq.step_count_y - 1)

        x = convert_unit('mm', position_start.x) + delta_x * x
        y = convert_unit('mm', position_start.y) + delta_y * y
        if position_start.z is None and position_end.z is None:
            z = None
        else:
            z = np.mean([position_start.z, position_end.z])
        r = position_start.r
        t = position_start.t

        return SpecimenPosition(x, y, z, r, t)

    def get_index(self, position):
        acqs = self.conditions.findvalues(AcquisitionRasterXY)
        if not acqs:
            raise ValueError('No acquisition raster XY found in conditions')
        acq = next(iter(acqs))

        position_start = self.get_position(0, 0)

        step_size_x = convert_unit('mm', acq.step_size_x)
        step_size_y = convert_unit('mm', acq.step_size_y)

        if step_size_x is None or step_size_y is None:
            position_end = self.get_position(-1, -1)
            delta = position_end - position_start

            if acq.step_size_x is None:
                step_size_x = convert_unit('mm', delta.x) / (acq.step_count_x - 1)

            if acq.step_size_y is None:
                step_size_y = convert_unit('mm', delta.y) / (acq.step_count_y - 1)

        delta = position - position_start
        x = abs(int(convert_unit('mm', delta.x) / step_size_x))
        y = abs(int(convert_unit('mm', delta.y) / step_size_y))

        if x < 0 or x >= self.x or y < 0 or y >= self.y:
            raise IndexError('Position (%i, %i) is out of bounds [0,%i[ : [0,%i[' % \
                             (x, y, self.x, self.y))

        return x, y

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
