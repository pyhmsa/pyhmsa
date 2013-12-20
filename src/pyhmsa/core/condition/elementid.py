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
from pyhmsa.core.condition import _Condition, extract_numerical_value

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
    
    def __init__(self, z):
        """
        Defines and elemental identification, as may be useful for region of 
        interest images, XAFS spectral maps, and the like.
        
        :arg z: atomic number (required)
        """
        _Condition.__init__(self)

        self.z = z

    def get_z(self):
        """
        Returns the atomic number.
        """
        return self._z

    get_atomic_number = get_z

    def set_z(self, z):
        """
        Sets the atomic number.
        
        :arg z: atomic number
        """
        if z is None:
            raise ValueError('Atomic number is required')
        if z < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if z > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        self._z = int(z)

    set_atomic_number = set_z

    z = property(get_z, set_z, doc='Atomic number')
    atomic_number = z

    def get_symbol(self):
        """
        Returns the symbol.
        """
        return _SYMBOLS[self.z - 1]

    symbol = property(get_symbol, doc='Symbol')

class ElementIDXray(ElementID):
    
    def __init__(self, z, line, energy=None):
        """
        Defines and elemental identification based on an x-ray peak, as may be 
        useful for region of interest images and the like.
        
        :arg z: atomic number (required)
        :arg line: x-ray line (required)
        :arg energy: energy of x-ray line (optional)
        """
        ElementID.__init__(self, z)

        self.line = line
        self.energy = energy

    def get_line(self):
        """
        Returns x-ray line.
        """
        return self._line
    
    def set_line(self, value):
        """
        Sets x-ray line.
        
        :arg value: x-ray line
        """
        if value is None:
            raise ValueError('X-ray line is required')
        self._line = value

    line = property(get_line, set_line, doc='X-ray line')

    def get_energy(self):
        """
        Returns the energy of the x-ray line.
        
        :return: energy and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._energy
    
    def set_energy(self, value, unit='eV'):
        """
        Sets the energy of the x-ray line.
        
        :arg value: energy
        :arg unit: unit
        """
        self._energy = extract_numerical_value(value, unit)

    energy = property(get_energy, set_energy, doc='Energy of x-ray line')
