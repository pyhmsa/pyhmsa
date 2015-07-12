"""
Numerical data type
"""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.unit import validate_unit, parse_unit

# Globals and constants variables.
from pyhmsa.type.unit import  _PREFIXES_VALUES

_SUPPORTED_DTYPES = frozenset(map(np.dtype, [np.uint8, np.int16, np.uint16,
                                             np.int32, np.uint32, np.int64,
                                             np.float32, np.float64]))

def validate_dtype(arg):
    if isinstance(arg, np.dtype):
        dtype = arg
    elif isinstance(arg, type) and issubclass(arg, np.generic):
        dtype = np.dtype(arg)
    elif hasattr(arg, 'dtype'):
        dtype = arg.dtype
    else:
        raise ValueError('Cannot find dtype of argument')

    if dtype not in _SUPPORTED_DTYPES:
        raise ValueError('Unsupported data type: %s' % dtype.name)

    return True

class arrayunit(np.ndarray):

    def __new__(cls, shape, dtype=np.float32, buffer=None, offset=0,
                 strides=None, order=None, unit=None):
        validate_dtype(dtype)
        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset, strides,
                                 order)

        if unit is not None:
            unit = validate_unit(unit)
        obj._unit = unit

        return obj

    def __reduce__(self):
        order = 'C' if self.flags['C_CONTIGUOUS'] else 'F'
        return self.__class__, (self.shape, self.dtype, np.ravel(self),
                                0, None, order, self.unit)

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._unit = getattr(obj, '_unit', None)

    def __array_wrap__(self, out_arr, context=None):
        ret_arr = np.ndarray.__array_wrap__(self, out_arr, context)
        return np.array(ret_arr) # Cast as regular array

    def __str__(self):
        if self._unit is not None:
            return np.ndarray.__str__(self) + ' ' + self.unit
        else:
            return np.ndarray.__str__(self)

    def __format__(self, spec):
        if spec[-1].lower() in ['f', 'e', 'g', 'n']:
            return format(float(self), spec)
        elif spec[-1] in ['d']:
            return format(int(self), spec)
        else:
            return format(np.ndarray.__str__(self), spec)

    def __eq__(self, other):
        if not np.ndarray.__eq__(self, other):
            return False
        return self.unit == getattr(other, 'unit', self.unit)

    def __ne__(self, other):
        return not self == other

    @property
    def unit(self):
        return self._unit

def convert_value(value, unit=None):
    if value is None:
        return None

    if not isinstance(value, arrayunit):
        value = np.asarray(value)
    else:
        unit = value.unit or unit

    return arrayunit(value.shape, value.dtype, value, unit=unit)

def convert_unit(newunit, value, oldunit=None):
    if value is None:
        return None

    if oldunit is None:
        oldunit = value.unit

    newprefix, newbaseunit, newexponent = parse_unit(newunit)
    newprefix_value = _PREFIXES_VALUES.get(newprefix, 1.0)

    oldprefix, oldbaseunit, oldexponent = parse_unit(oldunit)
    oldprefix_value = _PREFIXES_VALUES.get(oldprefix, 1.0)

    # Fix for non SI units
    if newbaseunit == 'm' and oldbaseunit == u'\u00c5':
        oldbaseunit = 'm'
        oldprefix_value *= 1e-10
    elif newbaseunit == u'\u00c5' and oldbaseunit == 'm':
        oldbaseunit = u'\u00c5'
        oldprefix_value *= 1e10

    elif newbaseunit == 'rad' and oldbaseunit == 'degrees':
        oldbaseunit = 'rad'
        oldprefix_value *= np.pi / 180.0
    elif newbaseunit == 'degrees' and oldbaseunit == 'rad':
        oldbaseunit = 'degrees'
        oldprefix_value *= 180.0 / np.pi

    # Check
    if newbaseunit != oldbaseunit:
        raise ValueError('Base units must match: %s != %s' % \
                         (newbaseunit, oldbaseunit))
    if newexponent != oldexponent:
        raise ValueError('Exponents must match: %s != %s' % \
                         (newexponent, oldexponent))

    # Conversion
    factor = oldprefix_value ** oldexponent / newprefix_value ** oldexponent
    newvalue = value * factor

    if hasattr(value, 'unit'):
        newvalue = convert_value(newvalue, newunit)

    return newvalue
