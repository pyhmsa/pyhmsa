""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class _ConditionXMLHandler(_XMLHandler):

    def __init__(self, clasz, version):
        super().__init__(version)
        self._class = clasz

    def can_parse(self, element):
        return element.tag == self._class.TEMPLATE and \
            element.get('Class') == self._class.CLASS

    def parse(self, element):
        return self._parse_parameter(element, self._class)

    def can_convert(self, obj):
        return type(obj) is self._class

    def convert(self, obj):
        tag = self._class.TEMPLATE
        attrib = {}
        if self._class.CLASS:
            attrib['Class'] = self._class.CLASS
        return self._convert_parameter(obj, tag, attrib)
