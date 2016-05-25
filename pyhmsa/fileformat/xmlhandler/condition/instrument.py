"""
XML handler for instrument condition
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.instrument import Instrument
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class InstrumentXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(Instrument, version)
