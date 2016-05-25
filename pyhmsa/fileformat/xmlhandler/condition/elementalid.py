"""
XML handler for element id condition
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.elementalid import ElementalID, ElementalIDXray
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class ElementalIDXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(ElementalID, version)

    def convert(self, obj):
        element = super().convert(obj)
        element.find('Element').set('Symbol', obj.symbol) # manually add symbol
        return element

class ElementalIDXrayXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(ElementalIDXray, version)

    def convert(self, obj):
        element = super().convert(obj)
        element.find('Element').set('Symbol', obj.symbol) # manually add symbol
        return element
