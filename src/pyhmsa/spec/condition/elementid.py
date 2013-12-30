#!/usr/bin/env python
"""
================================================================================
:mod:`elementid` -- Element ID condition
================================================================================

.. module:: elementid
   :synopsis: Element ID condition

.. inheritance-diagram:: elementid

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
from pyhmsa.spec.condition import _Condition
from pyhmsa.util.parameter import \
    NumericalAttribute, TextAttribute, AtomicNumberAttribute

# Globals and constants variables.

_SYMBOLS = [
        "H"  , "He" , "Li" , "Be" , "B"  , "C"  , "N"  , "O",
        "F"  , "Ne" , "Na" , "Mg" , "Al" , "Si" , "P"  , "S",
        "Cl" , "Ar" , "K"  , "Ca" , "Sc" , "Ti" , "V"  , "Cr",
        "Mn" , "Fe" , "Co" , "Ni" , "Cu" , "Zn" , "Ga" , "Ge",
        "As" , "Se" , "Br" , "Kr" , "Rb" , "Sr" , "Y"  , "Zr",
        "Nb" , "Mo" , "Tc" , "Ru" , "Rh" , "Pd" , "Ag" , "Cd",
        "In" , "Sn" , "Sb" , "Te" , "I"  , "Xe" , "Cs" , "Ba",
        "La" , "Ce" , "Pr" , "Nd" , "Pm" , "Sm" , "Eu" , "Gd",
        "Tb" , "Dy" , "Ho" , "Er" , "Tm" , "Yb" , "Lu" , "Hf",
        "Ta" , "W"  , "Re" , "Os" , "Ir" , "Pt" , "Au" , "Hg",
        "Tl" , "Pb" , "Bi" , "Po" , "At" , "Rn" , "Fr" , "Ra",
        "Ac" , "Th" , "Pa" , "U"  , "Np" , "Pu" , "Am" , "Cm",
        "Bk" , "Cf" , "Es" , "Fm" , "Md" , "No" , "Lr" , "Rf",
        "Db" , "Sg" , "Bh" , "Hs" , "Mt" , "Ds" , "Rg" , "Cn",
        "Uut", "Fl" , "Uup", "Lv" , "Uus", "Uuo"
    ]

class ElementID(_Condition):

    TEMPLATE = 'ElementID'

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
        return _SYMBOLS[self.atomic_number - 1]

    symbol = property(get_symbol, doc='Symbol')

class ElementIDXray(ElementID):

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
        ElementID.__init__(self, atomic_number)

        self.line = line
        self.energy = energy
