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
from pyhmsa.util.parameter import ParameterMetaclass, UnitAttribute
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.type.numerical import convert_value
from pyhmsa.util.element_properties import get_symbol

# Globals and constants variables.
_COMPOSITION_UNITS = frozenset(['atoms', 'mol%', 'vol%', 'wt%',
                                'mol_ppm', 'vol_ppm', 'wt_ppm',
                                'mol_ppb', 'vol_ppb', 'wt_ppb'])

class _Composition(_Condition):

    TEMPLATE = 'Composition'

    unit = UnitAttribute(None, True, 'Unit', 'unit in which the composition is defined')

    def __init__(self, unit):
        """
        Defines the composition of a material.

        :arg unit: unit in which the composition is defined (required)
        """
        _Condition.__init__(self)

        if unit not in _COMPOSITION_UNITS: # FIXME
            raise ValueError('Invalid unit for composition')
        self.unit = unit

class _CompositionElementalMetaclass(ABCMeta, ParameterMetaclass):
    pass

_BaseCompositionElemental = \
    _CompositionElementalMetaclass('_CompositionElementalMetaclass',
                                   (UserDict, _Composition), {})

class CompositionElemental(_BaseCompositionElemental):

    CLASS = 'Elemental'

    def __init__(self, unit, values=None, **kwargs):
        """
        Defines the composition of a material in terms of its constituent
        elements.
        The composition is a :class:`dict` where the keys are atomic numbers
        and the values the amounts of an element.

        :arg unit: unit in which the composition is defined (required)
        """
        _Composition.__init__(self, unit)
        UserDict.__init__(self, values, **kwargs)

    def __setitem__(self, key, item):
        if key is None:
            return
        if key < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if key > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        UserDict.__setitem__(self, np.uint8(key), convert_value(item))

    def __repr__(self):
        r = _Composition.__repr__(self)[:-2]

        if len(self) > 0:
            for z, fraction in self.items():
                r += ', %s=%s' % (get_symbol(z), fraction)

        return r + ')>'

    __str__ = __repr__

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
