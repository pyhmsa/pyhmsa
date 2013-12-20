#!/usr/bin/env python
"""
================================================================================
:mod:`language` -- Language format
================================================================================

.. module:: language
   :synopsis: Language format

.. inheritance-diagram:: pyhmsa.format.language

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from collections import namedtuple

# Third party modules.

# Local modules.

# Globals and constants variables.

alt_str = namedtuple('alt_str', ['value', 'altvalue', 'lang'])
