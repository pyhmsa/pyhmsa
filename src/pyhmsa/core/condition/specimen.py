#!/usr/bin/env python
"""
================================================================================
:mod:`specimen` -- Specimen condition
================================================================================

.. module:: specimen
   :synopsis: Specimen condition

.. inheritance-diagram:: pyhmsa.condition.specimen

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
try:
    from collections import UserDict
except ImportError: # pragma: no cover
    from UserDict import UserDict

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.core.condition import _Condition
from pyhmsa.type.numerical import convert_value
from pyhmsa.type.unit import validate_unit
from pyhmsa.util.parameter import \
    (Parameter, NumericalAttribute, TextAttribute, ObjectAttribute,
     FrozenAttribute)

# Globals and constants variables.
_COMPOSITION_UNITS = frozenset(['atoms', 'mol%', 'vol%', 'wt%',
                                'mol_ppm', 'vol_ppm', 'wt_ppm',
                                'mol_ppb', 'vol_ppb', 'wt_ppb'])

class SpecimenPosition(_Condition):

    x = NumericalAttribute('mm', False, 'X', 'x coordinate')
    y = NumericalAttribute('mm', False, 'Y', 'y coordinate')
    z = NumericalAttribute('mm', False, 'Z', 'z coordinate')
    r = NumericalAttribute(u'\u00b0', False, 'R', 'rotation')
    t = NumericalAttribute(u'\u00b0', False, 'T', 'tilt')

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

class Composition(UserDict):

    def __init__(self, unit, adict=None, **kwargs):
        """
        Defines the composition of a specimen.
        The composition is a :class:`dict` where the keys are atomic numbers
        and the values the amounts of an element.

        :arg unit: unit in which the composition is defined (required)
        """
        UserDict.__init__(self, adict, **kwargs)

        validate_unit(unit)
        if unit not in _COMPOSITION_UNITS:
            raise ValueError('Invalid unit for composition')
        self._unit = unit

    def __setitem__(self, key, item):
        if key < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if key > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        UserDict.__setitem__(self, np.uint8(key), convert_value(item))

    def get_unit(self):
        """
        Returns unit.
        """
        return self._unit

    unit = property(get_unit, doc='Unit')

class Specimen(_Condition):

    name = TextAttribute(True, 'Name', 'name')
    description = TextAttribute(False, 'Description', 'description')
    origin = TextAttribute(False, 'Origin', 'origin')
    formula = TextAttribute(False, 'Formula', 'formula')
    composition = ObjectAttribute(Composition, False, doc='composition')
    temperature = NumericalAttribute(u'\u00b0\u0043', False, 'Temperature', 'temperature')

    def __init__(self, name, description=None, origin=None, formula=None,
                  composition=None, temperature=None):
        """
        Defines a physical specimen, including the name, origin, composition,
        etc.

        :arg name: name (required)
        :arg description: description (optional)
        :arg origin: origin (optional)
        :arg formula: formula (optional)
        :arg composition: composition (optional)
        :arg temperature: temperature (optional)
        """
        _Condition.__init__(self)

        self.name = name
        self.description = description
        self.origin = origin
        self.formula = formula
        self.composition = composition
        self.temperature = temperature

class SpecimenLayer(Parameter):

    name = TextAttribute(False, doc='name')
    thickness = NumericalAttribute('nm', False, 'Thickness', 'thickness')
    formula = TextAttribute(False, 'Formula', 'formula')
    composition = ObjectAttribute(Composition, False, doc='composition')

    def __init__(self, name=None, thickness=None, formula=None, composition=None):
        """
        Defines a layer of a multi-layered specimen.

        :arg name: name (optional)
        :arg thickness: thickness, bulk layer if ``None`` (optional)
        :arg formula: formula
        :arg composition: composition
        """
        self.name = name
        self.thickness = thickness
        self.formula = formula
        self.composition = composition

    def is_bulk(self):
        """
        Returns whether this layer is a bulk layer.
        """
        return self.thickness is None

class SpecimenMultilayer(Specimen):
    
    layers = FrozenAttribute(list, doc='modifiable list of layers')

    def __init__(self, name, description=None, origin=None, formula=None,
                  composition=None, temperature=None, layers=None):
        """
        Defines a multi-layered physical specimen

        :arg name: name (required)
        :arg description: description (optional)
        :arg origin: origin (optional)
        :arg formula: formula (optional)
        :arg composition: composition (optional)
        :arg temperature: temperature (optional)
        :arg layers: layers (optional)
        """
        Specimen.__init__(self, name, description, origin, formula,
                          composition, temperature)

        if layers is None:
            layers = []
        self.layers.extend(layers)

    def append_layer(self, name=None, thickness=None, formula=None, composition=None):
        """
        Utility function to create a layer.

        :arg name: name (optional)
        :arg thickness: thickness, bulk layer if ``None`` (optional)
        :arg formula: formula
        :arg composition: composition

        :return: created layer
        :rtype: :class:`.SpecimenLayer`
        """
        layer = SpecimenLayer(name, thickness, formula, composition)
        self.layers.append(layer)
        return layer
