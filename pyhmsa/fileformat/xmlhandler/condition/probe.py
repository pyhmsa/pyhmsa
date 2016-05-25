"""
XML handler for probe condition
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.probe import ProbeEM, ProbeTEM
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class ProbeEMXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(ProbeEM, version)

class ProbeTEMXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(ProbeTEM, version)

