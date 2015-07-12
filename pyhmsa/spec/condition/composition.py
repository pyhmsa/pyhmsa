"""
Composition condition
"""

# Standard library modules.
from abc import ABCMeta
from collections import MutableMapping

# Third party modules.
import numpy as np
import six

# Local modules.
from pyhmsa.util.parameter import ParameterMetaclass, UnitAttribute
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.type.numerical import convert_value
import pyhmsa.util.element_properties as ep

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
                                   (MutableMapping, _Composition), {})

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

        self._data = {}

        if values is not None:
            self.update(values)
        self.update(**kwargs)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            key = ep.get_atomic_number(key)
        return self._data[key]

    def __setitem__(self, key, item):
        if key is None:
            return
        if isinstance(key, six.string_types):
            key = ep.get_atomic_number(key)
        if key < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if key > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        self._data[np.uint8(key)] = convert_value(item)

    def __delitem__(self, key):
        if isinstance(key, six.string_types):
            key = ep.get_atomic_number(key)
        del self._data[key]

    def __repr__(self):
        r = _Composition.__repr__(self)[:-2]

        if len(self) > 0:
            for z, fraction in self.items():
                r += ', %s=%s' % (ep.get_symbol(z), fraction)

        return r + ')>'

    __str__ = __repr__

    def to_wt(self):
        """
        Returns a :class:`CompositionElemental` with unit of wt%.
        """
        if self.unit.startswith('vol'):
            raise ValueError('Cannot be converted to wt%')

        def _get_factor(unit):
            if unit.endswith('%'):
                return 1.0
            elif unit.endswith('ppm'):
                return 0.0001
            elif unit.endswith('ppb'):
                return 0.0000001
            else:
                raise ValueError('Unknown unit')

        if self.unit.startswith('wt'):
            comp = CompositionElemental('wt%')
            factor = _get_factor(self.unit)
            for z, fraction in self.items():
                comp[z] = fraction * factor
            return comp

        elif self.unit == 'atoms' or self.unit.startswith('mol'):
            comp = CompositionElemental('wt%')
            for z, fraction in self.items():
                comp[z] = fraction * ep.get_atomic_mass_kg_mol(z)

            total = sum(comp.values())
            for z, fraction in comp.items():
                comp[z] = fraction / total * 100.0

            return comp

        else:
            raise ValueError('Unknown unit')

