"""
Composition XML handler
"""

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.composition import CompositionElemental
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class CompositionElementalXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(CompositionElemental, version)

    def parse(self, element):
        units = []
        tmpcomposition = {}
        subelements = element.findall('Element') + element.findall('Components/Element')
        for subelement in subelements:
            z = int(subelement.attrib['Z'])
            value = self._parse_numerical_attribute(subelement)
            units.append(value.unit)
            tmpcomposition.setdefault(z, value)

        # Check units
        units = set(units)
        if not units:
            return None
        if len(units) > 1:
            raise ValueError('Incompatible unit in composition')
        unit = list(units)[0]

        composition = CompositionElemental(unit)
        composition.update(tmpcomposition)
        return composition

    def convert(self, obj):
        element = etree.Element('Composition', {'Class': 'Elemental'})
        subelement = etree.SubElement(element, 'Components')

        attrib = type('MockAttribute', (object,), {'xmlname': 'Element'})
        for z, fraction in obj.items():
            subsubelement = self._convert_numerical_attribute(fraction, attrib)[0]
            subsubelement.set('Unit', obj.unit)
            subsubelement.set('Z', str(z))
            subelement.append(subsubelement)

        return element
