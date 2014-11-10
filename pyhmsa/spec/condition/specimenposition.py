#!/usr/bin/env python
"""
================================================================================
:mod:`specimenposition` -- Specimen position condition
================================================================================

.. module:: specimenposition
   :synopsis: Specimen position condition

.. inheritance-diagram:: pyhmsa.spec.condition.specimenposition

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.util.parameter import NumericalAttribute
from pyhmsa.type.numerical import convert_unit

# Globals and constants variables.

class SpecimenPosition(_Condition):

    TEMPLATE = 'SpecimenPosition'

    x = NumericalAttribute('mm', False, 'X', 'x coordinate')
    y = NumericalAttribute('mm', False, 'Y', 'y coordinate')
    z = NumericalAttribute('mm', False, 'Z', 'z coordinate')
    r = NumericalAttribute('degrees', False, 'R', 'rotation')
    t = NumericalAttribute('degrees', False, 'T', 'tilt')

    def __init__(self, x=None, y=None, z=None, r=None, t=None):
        """
        Defines a physical location on (or in) the specimen.
        The position shall be defined in the coordinate system of the instrument.
        This version of the HMSA standard does not specify a template or
        definition of coordinate systems.

        :arg x: x coordinate
        :arg y: y coordinate
        :arg z: z coordinate
        :arg r: rotation
        :arg t: tilt
        """
        _Condition.__init__(self)

        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.t = t

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        x = self.x + (other.x or 0.0) if self.x is not None else None
        y = self.y + (other.y or 0.0) if self.y is not None else None
        z = self.z + (other.z or 0.0) if self.z is not None else None
        r = self.r + (other.r or 0.0) if self.r is not None else None
        t = self.t + (other.t or 0.0) if self.t is not None else None

        return SpecimenPosition(x, y, z, r, t)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        x = self.x - (other.x or 0.0) if self.x is not None else None
        y = self.y - (other.y or 0.0) if self.y is not None else None
        z = self.z - (other.z or 0.0) if self.z is not None else None
        r = self.r - (other.r or 0.0) if self.r is not None else None
        t = self.t - (other.t or 0.0) if self.t is not None else None

        return SpecimenPosition(x, y, z, r, t)

    def tolist(self, coordinate_unit='mm', angle_unit='degrees'):
        def _float(x):
            return float(x) if x is not None else None
        return [_float(convert_unit(coordinate_unit, self.x)),
                _float(convert_unit(coordinate_unit, self.y)),
                _float(convert_unit(coordinate_unit, self.z)),
                _float(convert_unit(angle_unit, self.r)),
                _float(convert_unit(angle_unit, self.t))]