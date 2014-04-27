#!/usr/bin/env python
"""
================================================================================
:mod:`elementid` -- Element ID condition
================================================================================

.. module:: elementid
   :synopsis: Element ID condition

.. inheritance-diagram:: elementid

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.util.parameter import \
    NumericalAttribute, XRayLineAttribute, AtomicNumberAttribute
from pyhmsa.util.element_properties import get_symbol, get_atomic_number

# Globals and constants variables.
from pyhmsa.type.xrayline import NOTATION_SIEGBAHN

class ElementalID(_Condition):

    TEMPLATE = 'ElementalID'

    atomic_number = AtomicNumberAttribute(True, 'Element', "atomic number")

    def __init__(self, atomic_number=None, symbol=None):
        """
        Defines and elemental identification, as may be useful for region of
        interest images, XAFS spectral maps, and the like.

        :arg z: atomic number (required)
        """
        _Condition.__init__(self)

        if atomic_number is not None:
            self.atomic_number = atomic_number
        elif symbol is not None:
            self.symbol = symbol
        else:
            raise ValueError('Atomic number or symbol is required')

    def get_symbol(self):
        """
        Returns the symbol.
        """
        return get_symbol(self.atomic_number)

    def set_symbol(self, symbol):
        self.atomic_number = get_atomic_number(symbol)

    symbol = property(get_symbol, set_symbol, doc='Symbol')

class ElementalIDXray(ElementalID):

    CLASS = 'X-ray'

    line = XRayLineAttribute(NOTATION_SIEGBAHN, True, 'Line', 'x-ray line')
    energy = NumericalAttribute('eV', False, 'Energy', 'energy of x-ray line')

    def __init__(self, atomic_number=None, line=None, energy=None, symbol=None):
        """
        Defines and elemental identification based on an x-ray peak, as may be
        useful for region of interest images and the like.

        :arg atomic_number: atomic number (required)
        :arg line: x-ray line (required)
        :arg energy: energy of x-ray line (optional)
        """
        ElementalID.__init__(self, atomic_number, symbol)

        if line is None:
            raise ValueError('x-ray line is required')
        self.line = line
        self.energy = energy
