#!/usr/bin/env python
"""
================================================================================
:mod:`condition` -- Base class for all conditions
================================================================================

.. module:: condition
   :synopsis: Base class for all conditions

.. inheritance-diagram:: pyhmsa.spec.condition.condition

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.util.parameter import Parameter

# Globals and constants variables.

class _Condition(Parameter):

    TEMPLATE = None
    CLASS = None
