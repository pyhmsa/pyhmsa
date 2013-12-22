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
except ImportError: # Python 2.7 # pragma: no cover
    from UserDict import UserDict

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.core.condition import _Condition
from pyhmsa.type.unit import validate_unit
from pyhmsa.type.numerical import extract_value

# Globals and constants variables.
_COMPOSITION_UNITS = frozenset(['atoms', 'mol%', 'vol%', 'wt%',
                                'mol_ppm', 'vol_ppm', 'wt_ppm',
                                'mol_ppb', 'vol_ppb', 'wt_ppb'])

class SpecimenPosition(_Condition):

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

    def set_x(self, value, unit='mm'):
        """
        Sets the x coordinate in the coordinate system of the instrument.
        
        :arg value: x coordinate
        :arg unit: unit
        """
        self._x = extract_value(value, unit)

    def get_x(self):
        """
        Returns the x coordinate in the coordinate system of the instrument.
        
        :return: x coordinate and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._x

    x = property(get_x, set_x,
                 doc='x coordinate in the coordinate system of the instrument')

    def set_y(self, value, unit='mm'):
        """
        Sets the y coordinate in the coordinate system of the instrument.
        
        :arg value: y coordinate
        :arg unit: unit
        """
        self._y = extract_value(value, unit)

    def get_y(self):
        """
        Returns the y coordinate in the coordinate system of the instrument.
        
        :return: y coordinate and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._y

    y = property(get_y, set_y,
                 doc='y coordinate in the coordinate system of the instrument')

    def set_z(self, value, unit='mm'):
        """
        Sets the z coordinate in the coordinate system of the instrument.
        
        :arg value: z coordinate
        :arg unit: unit
        """
        self._z = extract_value(value, unit)

    def get_z(self):
        """
        Returns the z coordinate in the coordinate system of the instrument.
        
        :return: z coordinate and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._z

    z = property(get_z, set_z,
                 doc='z coordinate in the coordinate system of the instrument')

    def set_r(self, value, unit=u'\u00b0'):
        """
        Sets the stage rotation.
        
        :arg value: rotation
        :arg unit: unit
        """
        self._r = extract_value(value, unit)

    set_rotation = set_r

    def get_r(self):
        """
        Returns the stage rotation.
        
        :return: stage rotation
        :rtype: :class:`.NumericalValue`
        """
        return self._r

    get_rotation = get_r

    r = property(get_r, set_r, doc='Stage rotation')

    rotation = r

    def set_t(self, value, unit=u'\u00b0'):
        """
        Sets the stage tilt.
        
        :arg value: tilt
        :arg unit: unit
        """
        self._t = extract_value(value, unit)

    set_tilt = set_t

    def get_t(self):
        """
        Returns the stage tilt.
        
        :return: stage tilt
        :rtype: :class:`.NumericalValue`
        """
        return self._t

    get_tilt = get_t

    t = property(get_t, set_t, doc='Stage tilt')

    tilt = t

class Composition(UserDict):

    def __init__(self, unit):
        """
        Defines the composition of a specimen.
        The composition is a :class:`dict` where the keys are atomic numbers
        and the values the amounts of an element.
        
        :arg unit: unit in which the composition is defined (required)
        """
        UserDict.__init__(self)

        validate_unit(unit)
        if unit not in _COMPOSITION_UNITS:
            raise ValueError('Invalid unit for composition')
        self._unit = unit
        
    def __setitem__(self, key, item):
        if key < 1:
            raise ValueError('Atomic number cannot be less than hydrogen')
        if key > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')
        UserDict.__setitem__(self, np.uint8(key), extract_value(item))
    
    def get_unit(self):
        """
        Returns unit.
        """
        return self._unit
    
    unit = property(get_unit, doc='Unit')

class Specimen(_Condition):

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

    def get_name(self):
        """
        Returns name.
        """
        return self._name

    def set_name(self, value):
        """
        Sets name.
        
        :arg value: name
        """
        if value is None:
            raise ValueError('Name is required')
        self._name = value

    name = property(get_name, set_name, doc='Name')

    def get_description(self):
        """
        Returns description.
        """
        return self._description

    def set_description(self, value):
        """
        Sets description.
        
        :arg value: description
        """
        self._description = value

    description = property(get_description, set_description, doc='Description')

    def get_origin(self):
        """
        Returns origin.
        """
        return self._origin

    def set_origin(self, value):
        """
        Sets origin.
        
        :arg value: origin
        """
        self._origin = value

    origin = property(get_origin, set_origin, doc='Origin')

    def get_formula(self):
        """
        Returns formula.
        """
        return self._formula

    def set_formula(self, value):
        """
        Sets formula.
        
        :arg value: formula
        """
        self._formula = value

    formula = property(get_formula, set_formula, doc='Formula')

    def get_composition(self):
        """
        Returns composition.
        """
        return self._composition

    def set_composition(self, value):
        """
        Sets composition.
        
        :arg value: composition
        """
        self._composition = value

    composition = property(get_composition, set_composition, doc='Composition')

    def get_temperature(self):
        """
        Returns temperature.
        
        :return: temperature and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._temperature

    def set_temperature(self, value, unit=u'\u00b0\u0043'):
        """
        Sets temperature.
        
        :arg value: temperature
        :arg unit: unit
        """
        self._temperature = extract_value(value, unit)

    temperature = property(get_temperature, set_temperature, doc='Temperature')

class SpecimenLayer(object):

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

    def get_name(self):
        """
        Returns name.
        """
        return self._name

    def set_name(self, value):
        """
        Sets name.
        
        :arg value: name
        """
        self._name = value

    name = property(get_name, set_name, doc='Name')

    def get_thickness(self):
        """
        Returns thickness.
        
        :return: thickness and its unit
        :rtype: :class:`.NumericalValue`
        """
        return self._thickness

    def set_thickness(self, value, unit='nm'):
        """
        Sets thickness.
        
        :arg value: thickness
        :arg unit: unit
        """
        self._thickness = extract_value(value, unit)

    def is_bulk(self):
        """
        Returns whether this layer is a bulk layer.
        """
        return not bool(self._thickness)

    thickness = property(get_thickness, set_thickness, doc='Thickness')

    def get_formula(self):
        """
        Returns formula.
        """
        return self._formula

    def set_formula(self, value):
        """
        Sets formula.
        
        :arg value: formula
        """
        self._formula = value

    formula = property(get_formula, set_formula, doc='Formula')

    def get_composition(self):
        """
        Returns composition.
        """
        return self._composition

    def set_composition(self, value):
        """
        Sets composition.
        
        :arg value: composition
        """
        self._composition = value

    composition = property(get_composition, set_composition, doc='Composition')

class SpecimenMultilayer(Specimen):

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
        self._layers = list(layers)

    def get_layers(self):
        """
        Returns a modifiable list of layers.
        Layers can be added, removed and modified using the normal Python
        method for a :class:`list` (e.g. :meth:`append`, :meth:`remove`, etc.).
        
        :return: layers
        :rtype: :class:`list`
        """
        return self._layers

    layers = property(get_layers, doc='Modifiable list of layers')
    
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
