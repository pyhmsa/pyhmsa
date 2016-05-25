"""
XML handler for calibrations
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.calibration import \
    (CalibrationConstant, CalibrationLinear,
     CalibrationPolynomial, CalibrationExplicit)
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

# Globals and constants variables.

class CalibrationConstantXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(CalibrationConstant, version)

class CalibrationLinearXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(CalibrationLinear, version)

class CalibrationPolynomialXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(CalibrationPolynomial, version)

class CalibrationExplicitXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(CalibrationExplicit, version)

