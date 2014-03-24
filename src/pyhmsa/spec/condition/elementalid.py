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
    NumericalAttribute, TextAttribute, AtomicNumberAttribute
from pyhmsa.util.element_properties import get_symbol, get_atomic_number

# Globals and constants variables.

class ElementalID(_Condition):

    TEMPLATE = 'ElementalID'

    atomic_number = AtomicNumberAttribute(True, 'Element', "atomic number")

    def __init__(self, atomic_number):
        """
        Defines and elemental identification, as may be useful for region of
        interest images, XAFS spectral maps, and the like.

        :arg z: atomic number (required)
        """
        _Condition.__init__(self)

        self.atomic_number = atomic_number

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

    line = TextAttribute(True, 'Line', 'x-ray line')
    energy = NumericalAttribute('eV', False, 'Energy', 'energy of x-ray line')

    def __init__(self, atomic_number, line, energy=None):
        """
        Defines and elemental identification based on an x-ray peak, as may be
        useful for region of interest images and the like.

        :arg atomic_number: atomic number (required)
        :arg line: x-ray line (required)
        :arg energy: energy of x-ray line (optional)
        """
        ElementalID.__init__(self, atomic_number)

        self.line = line
        self.energy = energy
