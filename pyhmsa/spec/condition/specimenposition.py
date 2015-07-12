"""
Specimen position condition
"""

# Standard library modules.
import operator

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.util.parameter import NumericalAttribute
from pyhmsa.type.numerical import convert_unit, convert_value

# Globals and constants variables.

def _apply_operator(op, a, b, unit):
    if a is None:
        return None
    if b is None:
        b = convert_value(0.0, unit)
    return op(convert_unit(unit, a), convert_unit(unit, b))

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

        x = _apply_operator(operator.add, self.x, other.x, 'mm')
        y = _apply_operator(operator.add, self.y, other.y, 'mm')
        z = _apply_operator(operator.add, self.z, other.z, 'mm')
        r = _apply_operator(operator.add, self.r, other.r, 'degrees')
        t = _apply_operator(operator.add, self.t, other.t, 'degrees')

        return SpecimenPosition(x, y, z, r, t)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        x = _apply_operator(operator.sub, self.x, other.x, 'mm')
        y = _apply_operator(operator.sub, self.y, other.y, 'mm')
        z = _apply_operator(operator.sub, self.z, other.z, 'mm')
        r = _apply_operator(operator.sub, self.r, other.r, 'degrees')
        t = _apply_operator(operator.sub, self.t, other.t, 'degrees')

        return SpecimenPosition(x, y, z, r, t)

    def tolist(self, coordinate_unit='mm', angle_unit='degrees'):
        def _float(x):
            return float(x) if x is not None else None
        return [_float(convert_unit(coordinate_unit, self.x)),
                _float(convert_unit(coordinate_unit, self.y)),
                _float(convert_unit(coordinate_unit, self.z)),
                _float(convert_unit(angle_unit, self.r)),
                _float(convert_unit(angle_unit, self.t))]
