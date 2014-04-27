#!/usr/bin/env python
"""
================================================================================
:mod:`analysis` -- Analysis (0D collection)
================================================================================

.. module:: analysis
   :synopsis: Analysis

.. inheritance-diagram:: analysis

"""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.datum import _Datum
from pyhmsa.spec.condition.detector import DetectorSpectrometer

# Globals and constants variables.

class _Analysis(_Datum):
    """
    Stores a single measurement of a specimen at a single point in space or
    time.
    """
    pass

    TEMPLATE = "Analysis"

class Analysis0D(_Analysis):
    """
    Data with 0 collection dimensions and 0 datum dimensions implies a dataset
    comprising of one single-valued measurement.
    """

    CLASS = "0D"

    def __new__(cls, value, dtype=np.float32,
                offset=0, strides=None, order=None,
                conditions=None):
        buffer = np.array(value, dtype=dtype)
        return _Analysis.__new__(cls, (), dtype,
                                 buffer, offset, strides, order, conditions)

class Analysis1D(_Analysis):
    """
    Stores a measurement of a specimen at a single point in space or time
    with one datum dimension.
    """

    CLASS = "1D"

    def __new__(cls, channels, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        if channels <= 0:
            raise ValueError('Number of channel must be greater than 0')
        shape = (channels,)
        return _Analysis.__new__(cls, shape, dtype,
                                 buffer, offset, strides, order, conditions)

    def get_xy(self, with_labels=False):
        xs = range(self.channels)
        xlabel = 'Channels'
        ylabel = 'Values'

        conditions = self.conditions.findvalues(DetectorSpectrometer)
        if conditions:
            condition = next(iter(conditions))
            calibration = condition.calibration
            xs = list(map(calibration, xs))
            xlabel = '%s (%s)' % (calibration.quantity, calibration.unit)
            if condition.measurement_unit is not None:
                ylabel += ' (%s)' % condition.measurement_unit

        outarr = np.transpose(np.array([xs, self]))

        if with_labels:
            return xlabel, ylabel, outarr
        else:
            return outarr

    @property
    def channels(self):
        return np.uint32(len(self))

    @property
    def datum_dimensions(self):
        dims = _Analysis.datum_dimensions.fget(self) # @UndefinedVariable
        dims['Channel'] = self.channels
        return dims

class Analysis2D(_Analysis):
    """
    Store a single measurement of the specimen at a single point in space or
    time with two datum dimensions, such as a diffraction pattern.

    .. note::

       This dataset type shall not be used to store 2 dimensional images
       rastered over the specimen, such as a conventional TEM or SEM image.
       Instead, such data shall be stored using the :class:`ImageRaster2D`.
    """

    CLASS = "2D"

    def __new__(cls, u, v, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        if u <= 0 or v <= 0:
            raise ValueError('Dimension must be greater than 0')
        shape = (u, v)
        return _Analysis.__new__(cls, shape, dtype,
                                 buffer, offset, strides, order, conditions)

    @property
    def u(self):
        return np.uint32(self.shape[0])

    @property
    def v(self):
        return np.uint32(self.shape[1])

    @property
    def datum_dimensions(self):
        dims = _Analysis.datum_dimensions.fget(self) # @UndefinedVariable
        dims['U'] = self.u
        dims['V'] = self.v
        return dims
