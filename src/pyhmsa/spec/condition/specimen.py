#!/usr/bin/env python
"""
================================================================================
:mod:`specimen` -- Specimen condition
================================================================================

.. module:: specimen
   :synopsis: Specimen condition

.. inheritance-diagram:: pyhmsa.condition.specimen

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.spec.condition.composition import _Composition
from pyhmsa.util.parameter import \
    (Parameter, NumericalAttribute, TextAttribute, ObjectAttribute,
     FrozenAttribute)

# Globals and constants variables.

class SpecimenPosition(_Condition):

    TEMPLATE = 'SpecimenPosition'

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

class Specimen(_Condition):

    TEMPLATE = 'Specimen'

    name = TextAttribute(True, 'Name', 'name')
    description = TextAttribute(False, 'Description', 'description')
    origin = TextAttribute(False, 'Origin', 'origin')
    formula = TextAttribute(False, 'Formula', 'formula')
    composition = ObjectAttribute(_Composition, False, doc='composition')
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
    composition = ObjectAttribute(_Composition, False, doc='composition')

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

    CLASS = 'Multilayer'

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
