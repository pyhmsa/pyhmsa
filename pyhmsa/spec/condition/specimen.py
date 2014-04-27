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

class Specimen(_Condition):

    TEMPLATE = 'Specimen'

    name = TextAttribute(True, 'Name', 'name')
    description = TextAttribute(False, 'Description', 'description')
    origin = TextAttribute(False, 'Origin', 'origin')
    formula = TextAttribute(False, 'Formula', 'formula')
    composition = ObjectAttribute(_Composition, False, doc='composition')
    temperature = NumericalAttribute('degreesC', False, 'Temperature', 'temperature')

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
