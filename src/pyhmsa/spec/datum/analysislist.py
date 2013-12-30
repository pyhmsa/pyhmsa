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

# Local modules.
from pyhmsa.spec.datum import _Datum

# Globals and constants variables.

class _AnalysisList(_Datum):
    """
    Represents a sequence of point measurements collected under the same
    conditions but in an irregular pattern, such as a line scan, a time
    sequence, or sparsely scanned images.

    Each row (first index) represents a point measurement.
    """

    def __array_finalize__(self, obj):
        _Datum.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim < 2:
            raise ValueError('Invalid dimension of array')

    @property
    def analysis_count(self):
        return len(self)

class AnalysisList0D(_AnalysisList):
    """
    Represents a sequence of point measurements with zero datum dimension,
    such as a line scan or time sequence of single-valued data (e.g. Ti counts,
    BSE yield, vacuum pressure).
    """

    def __array_finalize__(self, obj):
        _AnalysisList.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 2 or obj.shape[1] != 1:
            raise ValueError('Invalid dimension of array')

class AnalysisList1D(_AnalysisList):
    """
    Represents a sequence of point measurements with one datum dimension,
    such as a spectrum.
    """

    def __array_finalize__(self, obj):
        _AnalysisList.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 2 or obj.shape[1] < 1:
            raise ValueError('Invalid dimension of array')

    @property
    def channel(self):
        return self.shape[1]

class AnalysisList2D(_AnalysisList):
    """
    Represents a sequence of point measurements with two datum dimensions,
    such as a diffraction pattern.
    """

    def __array_finalize__(self, obj):
        _AnalysisList.__array_finalize__(self, obj)

        if obj is None:
            return

        if obj.ndim != 3 or obj.shape[1] < 1 or obj.shape[2] < 1:
            raise ValueError('Invalid dimension of array')

    @property
    def u(self):
        return self.shape[1]

    @property
    def v(self):
        return self.shape[2]

    def toimage(self, index):
        raise NotImplementedError


