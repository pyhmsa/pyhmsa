#!/usr/bin/env python
"""
================================================================================
:mod:`composition` -- Composition condition
================================================================================

.. module:: composition
   :synopsis: Composition condition

.. inheritance-diagram:: pyhmsa.spec.condition.composition

"""

# Standard library modules.
from abc import ABCMeta
try:
    from collections import UserDict
except ImportError: # pragma: no cover
    from UserDict import UserDict
from collections import Mapping

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.util.parameter import ParameterMetaclass
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.type.numerical import convert_value
from pyhmsa.type.unit import validate_unit

# Globals and constants variables.
_COMPOSITION_UNITS = frozenset(['atoms', 'mol%', 'vol%', 'wt%',
                                'mol_ppm', 'vol_ppm', 'wt_ppm',
                                'mol_ppb', 'vol_ppb', 'wt_ppb'])

class _Composition(_Condition):

    TEMPLATE = 'Composition'

    def __init__(self, unit):
        """
        Defines the composition of a material.

        :arg unit: unit in which the composition is defined (required)
        """
        _Condition.__init__(self)

        validate_unit(unit)
        if unit not in _COMPOSITION_UNITS:
            raise ValueError('Invalid unit for composition')
        self._unit = unit

    def get_unit(self):
        """
        Returns unit.
        """
        return self._unit

    unit = property(get_unit, doc='Unit')

class _CompositionElementalMetaclass(ABCMeta, ParameterMetaclass):
    pass

_BaseCompositionElemental = \
    _CompositionElementalMetaclass('_CompositionElementalMetaclass',
                                   (UserDict, _Composition), {})

class CompositionElemental(_BaseCompositionElemental):

    CLASS = 'Elemental'

    def __init__(self, unit, adict=None, **kwargs):
        """
        Defines the composition of a material in terms of its constituent
        elements.
        The composition is a :class:`dict` where the keys are atomic numbers
        and the values the amounts of an element.

        :arg unit: unit in which the composition is defined (required)
        """
        _Composition.__init__(self, unit)
        UserDict.__init__(self, adict, **kwargs)

    def __setitem__(self, key, item):
        if key < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if key > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        UserDict.__setitem__(self, np.uint8(key), convert_value(item))

    def update(*args, **kwds): #@NoSelf
        # Bug fix in Python 2 that update method does not call __setitem__
        # Method copied literally from Python 3.3
        if len(args) > 2:
            raise TypeError("update() takes at most 2 positional "
                            "arguments ({} given)".format(len(args)))
        elif not args:
            raise TypeError("update() takes at least 1 argument (0 given)")
        self = args[0]
        other = args[1] if len(args) >= 2 else ()

        if isinstance(other, Mapping):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, "keys"):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwds.items():
            self[key] = value
