"""
Specimen XML handler
"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimen import \
    Specimen, SpecimenMultilayer, SpecimenLayer
from pyhmsa.spec.condition.composition import CompositionElemental
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler
from pyhmsa.fileformat.xmlhandler.condition.composition import CompositionElementalXMLHandler

# Globals and constants variables.

class _SpecimenXMLHandler(_ConditionXMLHandler):

    def __init__(self, clasz, version):
        super().__init__(clasz, version)
        self._handler_composition = CompositionElementalXMLHandler(version)

    def _parse_composition(self, element):
        subelement = element.find('Composition')
        if subelement is None:
            return CompositionElemental("wt%")
        return self._handler_composition.parse(subelement)

    def parse(self, element):
        obj = super().parse(element)
        obj.composition = self._parse_composition(element)
        return obj

    def _convert_composition(self, obj):
        if obj.composition is None:
            return []
        return [self._handler_composition.convert(obj.composition)]

    def convert(self, obj):
        element = super().convert(obj)
        element.extend(self._convert_composition(obj))
        return element

class SpecimenXMLHandler(_SpecimenXMLHandler):

    def __init__(self, version):
        super().__init__(Specimen, version)

class _SpecimenLayerXMLHandler(_XMLHandler):

    def __init__(self, version):
        super().__init__(version)
        self._handler_composition = CompositionElementalXMLHandler(version)

    def can_parse(self, element):
        return element.tag == 'Layer'

    def _parse_composition(self, element):
        subelement = element.find('Composition')
        if subelement is None:
            return CompositionElemental("wt%")
        return self._handler_composition.parse(subelement)

    def parse(self, element):
        obj = self._parse_parameter(element, SpecimenLayer)
        obj.name = element.get('Name')
        obj.composition = self._parse_composition(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is Specimen

    def _convert_composition(self, obj):
        if obj.composition is None:
            return []
        return [self._handler_composition.convert(obj.composition)]

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Layer')
        if obj.name is not None:
            element.set('Name', obj.name)
        element.extend(self._convert_composition(obj))
        return element

class SpecimenMultilayerXMLHandler(_SpecimenXMLHandler):

    def __init__(self, version):
        super().__init__(SpecimenMultilayer, version)
        self._handler_layer = _SpecimenLayerXMLHandler(version)

    def parse(self, element):
        obj = super().parse(element)

        for subelement in element.findall('Layers/Layer'):
            layer = self._handler_layer.parse(subelement)
            obj.layers.append(layer)

        return obj

    def convert(self, obj):
        element = super().convert(obj)

        subelement = etree.Element('Layers')
        for layer in obj.layers:
            subsubelement = self._handler_layer.convert(layer)
            subelement.append(subsubelement)
        element.append(subelement)

        return element
