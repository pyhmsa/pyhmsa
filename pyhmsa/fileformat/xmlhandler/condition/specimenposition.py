"""
Specimen position XML handler
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class SpecimenPositionXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(SpecimenPosition, version)

