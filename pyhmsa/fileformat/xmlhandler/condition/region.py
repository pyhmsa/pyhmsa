"""
XML handler for region condition
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.region import RegionOfInterest
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class RegionOfInterestXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(RegionOfInterest, version)

    def parse(self, element):
        obj = super().parse(element)

        subelement = element.find('StartChannel')
        if subelement is None:
            raise ValueError('Element StartChannel is missing')
        start = self._parse_numerical_attribute(subelement)

        subelement = element.find('EndChannel')
        if subelement is None:
            raise ValueError('Element EndChannel is missing')
        end = self._parse_numerical_attribute(subelement)

        obj.channels = (start, end)
        return obj

    def convert(self, obj):
        element = super().convert(obj)

        value = obj.start_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'StartChannel'})
        subelements = self._convert_numerical_attribute(value, attrib)
        element.extend(subelements)

        value = obj.end_channel
        attrib = type('MockAttribute', (object,), {'xmlname': 'EndChannel'})
        subelements = self._convert_numerical_attribute(value, attrib)
        element.extend(subelements)

        return element
