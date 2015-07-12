"""
Base class for all conditions
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.util.parameter import Parameter

# Globals and constants variables.

class _Condition(Parameter):

    TEMPLATE = None
    CLASS = None
