#!/usr/bin/env python
"""
================================================================================
:mod:`element_properties` -- Element properties
================================================================================

.. module:: element_properties
   :synopsis: Element properties

.. inheritance-diagram:: pyhmsa.util.element_properties

"""

# Standard library modules.

# Third party modules.

# Local modules.

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

def get_symbol(z):
    """
    Returns the element's symbol.

    :arg z: atomic number
    """
    try:
        return _SYMBOLS[z - 1]
    except IndexError:
        return ValueError, "Unknown atomic number: %i." % z

def get_atomic_number(symbol):
    """
    Returns the atomic number for the specified symbol.
    This function is case insensitive.

    :arg symbol: symbol of the element (e.g. ``C``)
    """
    try:
        return _SYMBOLS.index(symbol.capitalize()) + 1
    except ValueError:
        raise ValueError("Unknown symbol: %s" % symbol)
