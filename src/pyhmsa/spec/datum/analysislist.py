#!/usr/bin/env python
"""
================================================================================
:mod:`analysislist` -- Analysis list (1D collection)
================================================================================

.. module:: analysislist
   :synopsis: Analysis list (1D collection)

.. inheritance-diagram:: analysislist

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

class _AnalysisList(_Datum):
    """
    Represents a sequence of point measurements collected under the same
    conditions but in an irregular pattern, such as a line scan, a time
    sequence, or sparsely scanned images.

    Each row (first index) represents a point measurement.
    """

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

    def __new__(cls, analysis_count, dtype=np.float32,
                buffer=None, conditions=None, order=None):
        shape = (analysis_count, 1)
        return _AnalysisList.__new__(cls, shape, dtype, buffer, conditions, order)

    def toanalysis(self, analysis_index):
        return Analysis0D(self[analysis_index, 0], self.dtype, self.conditions)

class AnalysisList1D(_AnalysisList):
    """
    Represents a sequence of point measurements with one datum dimension,
    such as a spectrum.
    """

    def __new__(cls, analysis_count, channels, dtype=np.float32,
                buffer=None, conditions=None, order=None):
        shape = (analysis_count, channels)
        return _AnalysisList.__new__(cls, shape, dtype, buffer, conditions, order)

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
                          self.conditions)

class AnalysisList2D(_AnalysisList):
    """
    Represents a sequence of point measurements with two datum dimensions,
    such as a diffraction pattern.
    """

    def __new__(cls, analysis_count, u, v, dtype=np.float32,
                buffer=None, conditions=None, order=None):
        shape = (analysis_count, u, v)
        return _AnalysisList.__new__(cls, shape, dtype, buffer, conditions, order)

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
                          self.conditions)
