#!/usr/bin/env python
"""
================================================================================
:mod:`analysislist` -- Analysis list (1D collection)
================================================================================

.. module:: analysislist
   :synopsis: Analysis list (1D collection)

.. inheritance-diagram:: analysislist

"""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.datum import _Datum
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D, Analysis2D

# Globals and constants variables.

class _AnalysisList(_Datum):
    """
    Represents a sequence of point measurements collected under the same
    conditions but in an irregular pattern, such as a line scan, a time
    sequence, or sparsely scanned images.

    Each row (first index) represents a point measurement.
    """

    TEMPLATE = 'AnalysisList'

    @property
    def analysis_count(self):
        return np.uint32(len(self))

    @property
    def collection_dimensions(self):
        dims = _Datum.collection_dimensions.fget(self) # @UndefinedVariable
        dims['Analysis'] = self.analysis_count
        return dims

class AnalysisList0D(_AnalysisList):
    """
    Represents a sequence of point measurements with zero datum dimension,
    such as a line scan or time sequence of single-valued data (e.g. Ti counts,
    BSE yield, vacuum pressure).
    """

    CLASS = "0D"

    def __new__(cls, analysis_count, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (analysis_count, 1)
        return _AnalysisList.__new__(cls, shape, dtype,
                                     buffer, offset, strides, order, conditions)

    def toanalysis(self, analysis_index):
        return Analysis0D(self[analysis_index, 0], self.dtype,
                          conditions=self.conditions)

class AnalysisList1D(_AnalysisList):
    """
    Represents a sequence of point measurements with one datum dimension,
    such as a spectrum.
    """

    CLASS = "1D"

    def __new__(cls, analysis_count, channels, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (analysis_count, channels)
        return _AnalysisList.__new__(cls, shape, dtype,
                                     buffer, offset, strides, order, conditions)

    @property
    def channels(self):
        return np.uint32(self.shape[1])

    @property
    def datum_dimensions(self):
        dims = _Datum.datum_dimensions.fget(self) # @UndefinedVariable
        dims['Channel'] = self.channels
        return dims

    def toanalysis(self, analysis_index):
        return Analysis1D(self.channels, self.dtype, self[analysis_index, :],
                          conditions=self.conditions)

class AnalysisList2D(_AnalysisList):
    """
    Represents a sequence of point measurements with two datum dimensions,
    such as a diffraction pattern.
    """

    CLASS = "2D"

    def __new__(cls, analysis_count, u, v, dtype=np.float32,
                buffer=None, offset=0, strides=None, order=None,
                conditions=None):
        shape = (analysis_count, u, v)
        return _AnalysisList.__new__(cls, shape, dtype,
                                     buffer, offset, strides, order, conditions)

    @property
    def u(self):
        return np.uint32(self.shape[1])

    @property
    def v(self):
        return np.uint32(self.shape[2])

    @property
    def datum_dimensions(self):
        dims = _Datum.datum_dimensions.fget(self) # @UndefinedVariable
        dims['U'] = self.u
        dims['V'] = self.v
        return dims

    def toanalysis(self, analysis_index):
        return Analysis2D(self.u, self.v, self.dtype, self[analysis_index],
                          conditions=self.conditions)
