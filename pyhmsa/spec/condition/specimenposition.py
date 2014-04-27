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